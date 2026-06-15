#!/usr/bin/env bash
#
# End-to-end test harness / curl collection for the Drone GCS backend.
# Asserts the expected HTTP status (and key fields) of every endpoint, prints
# [PASS]/[FAIL] per step, and exits non-zero if anything fails.
#
# Usage:
#   ./api.sh                              # run against the default base
#   BASE=http://localhost:8082/api/v1 ./api.sh
#
# Requires the backend running (mvn spring-boot:run) and Redis up.
# `jq` is optional (used to pretty-extract fields; sed fallback otherwise).

set -uo pipefail   # NOTE: no -e — the harness must keep going after a failed assertion.

BASE="${BASE:-http://localhost:8081/api/v1}"
SIM_BASE="${BASE%/v1}/simulation"
GCS_USER="${GCS_USER:-operator1}"
GCS_PASS="${GCS_PASS:-password123}"
DRONE="${DRONE:-drone-1}"
SIM_DRONE="${SIM_DRONE:-drone-901}"

PASS=0; FAIL=0
TOKEN=""; AUTH=()

have_jq() { command -v jq >/dev/null 2>&1; }
hr()   { printf '\n\033[1;34m== %s ==\033[0m\n' "$1"; }
pass() { printf '  \033[1;32m[PASS]\033[0m %s\n' "$1"; PASS=$((PASS+1)); }
fail() { printf '  \033[1;31m[FAIL]\033[0m %s\n' "$1"; FAIL=$((FAIL+1)); }

# field <json> <key> -> value (jq if available, else naive sed for string/number)
field() {
  if have_jq; then printf '%s' "$1" | jq -r ".$2 // empty" 2>/dev/null
  else printf '%s' "$1" | sed -n "s/.*\"$2\":\"\{0,1\}\([^\",}]*\)\"\{0,1\}.*/\1/p" | head -1; fi
}

# req METHOD URL [BODY] [--noauth]  -> sets CODE, BODY
req() {
  local method="$1" url="$2" body="${3:-}" mode="${4:-auth}"
  local hdr=(); [ "$mode" = "auth" ] && hdr=("${AUTH[@]}")
  local out
  if [ -n "$body" ]; then
    out=$(curl -s -w $'\n%{http_code}' -X "$method" "$url" "${hdr[@]}" \
          -H 'Content-Type: application/json' -d "$body")
  else
    out=$(curl -s -w $'\n%{http_code}' -X "$method" "$url" "${hdr[@]}")
  fi
  CODE=$(printf '%s' "$out" | tail -n1)
  BODY=$(printf '%s' "$out" | sed '$d')
}

# assert_code LABEL EXPECTED
assert_code() { [ "$CODE" = "$2" ] && pass "$1 ($CODE)" || fail "$1 (expected $2, got $CODE) -> ${BODY:0:160}"; }

# ─────────────────────────────────────────────────────────────────────────────
hr "Health (public)"
req GET "$BASE/health" "" noauth
assert_code "GET /health" 200

hr "Register (public)"
req POST "$BASE/auth/register" \
  "{\"username\":\"$GCS_USER\",\"email\":\"$GCS_USER@example.com\",\"password\":\"$GCS_PASS\",\"role\":\"OPERATOR\"}" noauth
if [ "$CODE" = "201" ]; then pass "register ($CODE)"; TOKEN=$(field "$BODY" token)
elif [ "$CODE" = "400" ]; then pass "register (user already exists — ok on re-run)"
else fail "register (expected 201/400, got $CODE) -> ${BODY:0:160}"; fi

hr "Login (public) — capture JWT"
req POST "$BASE/auth/login" "{\"username\":\"$GCS_USER\",\"password\":\"$GCS_PASS\"}" noauth
assert_code "POST /auth/login" 200
TOKEN=$(field "$BODY" token)
[ -n "$TOKEN" ] && pass "JWT captured (len ${#TOKEN})" || fail "JWT missing from login response"
AUTH=(-H "Authorization: Bearer $TOKEN")

hr "Auth & security"
req GET "$BASE/auth/me"; assert_code "GET /auth/me" 200
req GET "$BASE/drones" "" noauth; assert_code "GET /drones without token -> rejected" 403

hr "Drone latest-state (Redis, mock simulator)"
req GET "$BASE/drones/state"; assert_code "GET /drones/state" 200

hr "Command router"
req POST "$BASE/commands" "{\"droneId\":\"$DRONE\",\"type\":\"TAKEOFF\",\"altitudeMeters\":50}"
assert_code "POST /commands TAKEOFF" 202
CID=$(field "$BODY" commandId)
[ -n "$CID" ] && pass "commandId captured" || fail "commandId missing"
[ -n "$(field "$BODY" clientRequestId)" ] && pass "clientRequestId present" || fail "clientRequestId missing (stale build?)"

req POST "$BASE/commands" "{\"droneId\":\"$DRONE\",\"type\":\"GOTO_WAYPOINT\"}"
assert_code "POST /commands waypoint w/o coords -> rejected" 400
req POST "$BASE/commands/$DRONE/takeoff?altitudeMeters=50"; assert_code "POST takeoff helper" 202
req POST "$BASE/commands/$DRONE/waypoint?latitude=51.51&longitude=-0.12&altitudeMeters=40"; assert_code "POST waypoint helper" 202

sleep 2
req GET "$BASE/commands/status/$CID"
assert_code "GET /commands/status/{id}" 200
echo "$BODY" | grep -q "ACKNOWLEDGED" && pass "command ACKNOWLEDGED" || fail "command not acknowledged -> $BODY"
req GET "$BASE/commands/$DRONE/queue"; assert_code "GET outstanding queue" 200

hr "Telemetry persistence"
req GET "$BASE/telemetry/$DRONE/recent"; assert_code "GET /telemetry/{id}/recent" 200
req GET "$BASE/telemetry/$DRONE/history?page=0&size=5"; assert_code "GET /telemetry/{id}/history" 200

hr "Missions (droneIds required)"
req POST "$BASE/drones" "{\"name\":\"Falcon-1\",\"model\":\"PX4 X500\",\"serialNumber\":\"SN-API-1\"}"
assert_code "POST /drones" 200
DRONE_DB_ID=$(field "$BODY" id)
req POST "$BASE/missions" "{\"name\":\"No Drones\"}"
assert_code "POST /missions without droneIds -> rejected" 400
req POST "$BASE/missions" "{\"name\":\"Survey Alpha\",\"droneIds\":[\"$DRONE_DB_ID\"]}"
assert_code "POST /missions with droneIds" 200

hr "Full-pipeline simulation"
req POST "$SIM_BASE/start" "{\"droneId\":\"$SIM_DRONE\",\"rateHz\":10,\"phaseSeconds\":3}"
assert_code "POST /api/simulation/start" 202
RUN_ID=$(field "$BODY" runId)
[ -n "$RUN_ID" ] && pass "runId captured" || fail "runId missing (simulation feature absent?)"

# strict-validation check: bad rateHz must be rejected with 400
req POST "$SIM_BASE/start" "{\"rateHz\":0}"
assert_code "POST /api/simulation/start invalid rateHz -> rejected" 400

if [ -n "$RUN_ID" ]; then
  hr "Poll simulation (ARM->TAKEOFF->WAYPOINT->RTL->LAND->DISARM)"
  STATE=""
  for _ in $(seq 1 15); do
    sleep 2
    req GET "$SIM_BASE/$RUN_ID"
    STATE=$(field "$BODY" state); PHASE=$(field "$BODY" currentPhase)
    SAMPLES=$(have_jq && echo "$BODY" | jq -r '.telemetrySamples' || echo '?')
    echo "    state=$STATE phase=$PHASE samples=$SAMPLES"
    case "$STATE" in COMPLETED|STOPPED|FAILED) break;; esac
  done
  [ "$STATE" = "COMPLETED" ] && pass "simulation COMPLETED" || fail "simulation ended in state=$STATE"

  hr "Persistence check (flight log saved to DB)"
  req GET "$BASE/telemetry/$SIM_DRONE/history?size=1000"
  TOTAL=$(have_jq && echo "$BODY" | jq -r '.totalElements' || echo "$BODY" | sed -n 's/.*"totalElements":\([0-9]*\).*/\1/p')
  if [ "${TOTAL:-0}" -gt 0 ] 2>/dev/null; then pass "persisted $TOTAL telemetry rows for $SIM_DRONE"
  else fail "no telemetry persisted for $SIM_DRONE (totalElements=$TOTAL)"; fi
fi

# ─────────────────────────────────────────────────────────────────────────────
hr "SUMMARY"
printf '  passed: %d   failed: %d\n' "$PASS" "$FAIL"
if [ "$FAIL" -eq 0 ]; then
  printf '\033[1;32m  ALL TESTS PASSED\033[0m\n'; exit 0
else
  printf '\033[1;31m  %d TEST(S) FAILED\033[0m\n' "$FAIL"; exit 1
fi

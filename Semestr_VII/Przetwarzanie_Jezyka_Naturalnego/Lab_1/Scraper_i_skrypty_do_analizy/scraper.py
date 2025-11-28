from __future__ import annotations
import argparse, csv, json, random, re, sys, time
from typing import Dict, List, Optional, Iterable, Tuple
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Co scarapujemy
BASE = "https://mediamarkt.pl"
CATEGORY = "https://mediamarkt.pl/pl/category/komputery-stacjonarne-aio-25871.html"

# Headery do udawania przeglądarki
COMMON_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
    "upgrade-insecure-requests": "1",
    "sec-ch-ua": '"Chromium";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
}


# Tworzenie sesji przeglądarki
def make_session():

    # Probujemy curl-cffi z impersonacją (dokładniejsza niż requests)
    try:
        from curl_cffi import requests as cffi_requests

        for fp in ["chrome124", "edge101", "safari15_3", "firefox110"]:
            try:
                s = cffi_requests.Session(impersonate=fp)
                s.headers.update(COMMON_HEADERS)
                s._impersonation = fp
                return s
            except Exception:
                continue
        s = cffi_requests.Session()
        s.headers.update(COMMON_HEADERS)
        s._impersonation = "generic"
        return s

    # Gdy nie ma curl-cffi, bierzemy requests
    except Exception:
        import requests as rq

        s = rq.Session()
        s.headers.update(COMMON_HEADERS)
        s._impersonation = "requests"
        return s


# Globalna sesja
SESSION = make_session()


# Pobieranie strony
def get_soup(
    url: str, referer: Optional[str] = None, retries: int = 4, backoff: float = 1.6
) -> BeautifulSoup:
    last_exc = None
    for i in range(retries):
        try:
            headers = dict(COMMON_HEADERS)
            if referer:
                headers["referer"] = referer
            resp = SESSION.get(url, headers=headers, timeout=30, allow_redirects=True)
            if getattr(resp, "status_code", 200) in (403, 429, 503):
                time.sleep((backoff**i) + random.uniform(0.2, 0.8))
                continue
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "lxml")
        except Exception as e:
            last_exc = e
            time.sleep((backoff**i) + random.uniform(0.3, 1.0))
    raise RuntimeError(f"Failed to fetch {url}: {last_exc}")


# Tworzenie losowych opóźnień
def polite_delay(a: float = 1.0, b: float = 2.0) -> None:
    time.sleep(random.uniform(a, b))


# Iterowanie po stronach kategorii
def iterate_category_by_pages(category_url: str, pages: int) -> Iterable[str]:
    for n in range(1, pages + 1):
        url = category_url if n == 1 else f"{category_url}?page={n}"
        soup = get_soup(url, referer=BASE)
        product_urls = products_on_category_page(soup, url)
        if not product_urls:
            break
        for u in product_urls:
            yield u
        polite_delay(1.0, 2.0)


# Pomocnicza funkcja, jeśli tekst jest pusty, zwraca None
def text_or_none(x) -> Optional[str]:
    s = (x or "").strip()
    return s or None


# Konwersja polskich znaków na ascii w kluczach
_PL_MAP = str.maketrans(
    {
        "ą": "a",
        "ć": "c",
        "ę": "e",
        "ł": "l",
        "ń": "n",
        "ó": "o",
        "ś": "s",
        "ź": "z",
        "ż": "z",
        "Ą": "A",
        "Ć": "C",
        "Ę": "E",
        "Ł": "L",
        "Ń": "N",
        "Ó": "O",
        "Ś": "S",
        "Ź": "Z",
        "Ż": "Z",
    }
)


# Normalizacja kluczy specyfikacji
def normalize_key(label: str) -> str:
    k = label.strip().translate(_PL_MAP).lower()
    k = re.sub(r"\s+", "_", k)
    k = re.sub(r"[^a-z0-9_]", "", k)
    return f"spec_{k}"


def _parse_price_number(s: str) -> Optional[float]:
    if not s:
        return None
    ss = s.replace("\u00a0", " ").strip()
    ss = re.sub(_HYPHENS, "", ss)
    ss = re.sub(r"(?<=\d)[\s\u00A0](?=\d)", "", ss)
    for pat in _PRICE_PATTERNS:
        m = re.search(pat, ss, flags=re.I)
        if m:
            num = m.group(1)
            num = num.replace(" ", "").replace("\u00a0", "").replace(".", "")
            num = num.replace(",", ".")
            try:
                return float(num)
            except ValueError:
                pass
    m = re.search(r"(\d[\d\s]*[,\.]\d{2}|\d[\d\s]*)", ss)
    if m:
        num = m.group(1).replace(" ", "").replace("\u00a0", "")
        if "," in num and "." in num:
            num = num.replace(".", "")
        num = num.replace(",", ".")
        try:
            return float(num)
        except ValueError:
            return None
    return None


def _extract_price_static(soup, jsonld) -> Tuple[Optional[float], Optional[str]]:
    raw = soup.get_text(" ", strip=True)
    val = _parse_price_number(raw)
    return (val, raw if val is not None else None)


def _extract_price_dynamic_with_playwright(
    url: str, timeout_ms: int = 15000
) -> Tuple[Optional[float], Optional[str]]:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                locale="pl-PL",
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/126.0.0.0 Safari/537.36"
                ),
            )
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
            page.wait_for_timeout(1200)

            candidate_selectors = [
                '[class*="price"]',
                '[data-testid*="price"]',
                '[itemprop="price"]',
                "[data-price]",
                "[data-product-price]",
                'meta[itemprop="price"]',
            ]
            text_chunks = []

            for sel in candidate_selectors:
                els = page.query_selector_all(sel)
                for el in els:
                    try:
                        txt = (el.get_attribute("content") or "").strip()
                        if not txt:
                            txt = el.inner_text().strip()
                        if txt:
                            text_chunks.append(txt)
                    except Exception:
                        pass

            if not text_chunks:
                body_text = page.locator("body").inner_text(timeout=timeout_ms)
                text_chunks.append(body_text)

            browser.close()

        for chunk in text_chunks:
            val = _parse_price_number(chunk)
            if val is not None:
                return val, chunk

    except Exception:
        pass

    return None, None


def extract_itemlist_product_urls(soup: BeautifulSoup) -> List[str]:
    urls: List[str] = []
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "")
        except Exception:
            continue
        items = data if isinstance(data, list) else [data]
        for obj in items:
            if isinstance(obj, dict) and obj.get("@type") in (
                "ItemList",
                "CollectionPage",
                "SearchResultsPage",
            ):
                for el in obj.get("itemListElement", []):
                    if isinstance(el, dict):
                        u = el.get("url") or (el.get("item") or {}).get("@id")
                        if u:
                            urls.append(u)
    abs_urls = []
    for u in urls:
        au = u if u.startswith("http") else urljoin(BASE, u)
        if urlparse(au).netloc.endswith("mediamarkt.pl"):
            abs_urls.append(au)
    seen, out = set(), []
    for u in abs_urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def extract_product_links_fallback(soup: BeautifulSoup, page_url: str) -> List[str]:
    links: List[str] = []
    for a in soup.select(
        'a[href*="/pl/product/"], a[href*="/pl/products/"], a[href*="/product"]'
    ):
        href = a.get("href", "").strip()
        if not href or href.startswith("#"):
            continue
        if any(k in href for k in ["?sort", "?page=", "facet=", "filter="]):
            continue
        links.append(urljoin(page_url, href))
    seen, out = set(), []
    for u in links:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def products_on_category_page(soup: BeautifulSoup, page_url: str) -> List[str]:
    return extract_itemlist_product_urls(soup) or extract_product_links_fallback(
        soup, page_url
    )


# Parsowanie ceny z tekstu
PRICE_NODE_SELECTORS = [
    'meta[itemprop="price"]',
    '[itemprop="price"]',
    "[data-product-price]",
    "[data-price]",
    '[data-testid*="price"]',
    '.price, .product-price, .current-price, .c-price__value, .a-price__value, [class*="price"]',
]

_HYPHENS = r"[\-\u2010\u2011\u2012\u2013\u2014\u2212]"  # -, ‐, ‒, –, —
_CURRENCY = r"(?:z\s*ł|PLN)"
_PRICE_PATTERNS = [
    rf"(\d[\d\s\.]*[,\.]\d{{2}})\s*{_CURRENCY}",
    rf"(\d[\d\s\.]*)\s*{_CURRENCY}",
    rf"{_CURRENCY}\s*(\d[\d\s\.]*[,\.]\d{{2}})",
    rf"{_CURRENCY}\s*(\d[\d\s\.]*)",
]


def parse_decimal_from_text(s: str) -> Optional[float]:
    if not s:
        return None
    ss = s.replace("\u00a0", " ").strip()
    ss = re.sub(_HYPHENS, "", ss)
    ss = re.sub(r"(?<=\d)[\s\u00A0](?=\d)", "", ss)
    return _parse_price_number(ss)


def extract_price(
    soup, jsonld, url_for_fallback: Optional[str] = None
) -> Tuple[Optional[float], Optional[str]]:
    val, raw = _extract_price_static(soup, jsonld)
    if val is not None:
        return val, raw
    if url_for_fallback:
        return _extract_price_dynamic_with_playwright(url_for_fallback)
    return None, None


SPEC_ALIASES = {
    # CPU
    "spec_procesor": "spec_procesor",
    "spec_model_procesora": "spec_procesor",
    "spec_rodzaj_procesora": "spec_procesor",
    # CPU brand
    "spec_marka_procesora": "spec_marka_procesora",
    "spec_producent_procesora": "spec_marka_procesora",
    # RAM amount
    "spec_pamiec_ram": "spec_pami_ram",
    "spec_pami_ram": "spec_pami_ram",
    "spec_wielkosc_pamieci_ram": "spec_pami_ram",
    # RAM config
    "spec_konfiguracja_pamieci_ram": "spec_pami_ram_konfiguracja",
    "spec_pamiec_ram_konfiguracja": "spec_pami_ram_konfiguracja",
    # GPU
    "spec_karta_graficzna": "spec_karta_graficzna",
    "spec_model_karty_graficznej": "spec_karta_graficzna",
    # Disk / storage
    "spec_dysk": "spec_dysk",
    "spec_typ_dysku": "spec_dysk",
    "spec_rodzaj_dysku": "spec_dysk",
    # Disk capacity #1
    "spec_pojemnosc_dysku": "spec_pojemno_dysku_1",
    "spec_pojemnosc_dysku_1": "spec_pojemno_dysku_1",
    "spec_pojemnosc_dysku_ssd": "spec_pojemno_dysku_1",
    # OS
    "spec_system_operacyjny": "spec_system_operacyjny",
    # Product type
    "spec_typ_produktu": "spec_typ_produktu",
    # Cores
    "spec_liczba_rdzeni": "spec_liczba_rdzeni",
    "spec_liczba_rdzeni_procesora": "spec_liczba_rdzeni",
}

TARGET_COLUMNS = [
    "product_url",
    "name",
    "price",
    "spec_procesor",
    "spec_marka_procesora",
    "spec_pami_ram",
    "spec_karta_graficzna",
    "spec_dysk",
    "spec_pojemno_dysku_1",
    "spec_system_operacyjny",
    "spec_typ_produktu",
    "spec_liczba_rdzeni",
    "spec_pami_ram_konfiguracja",
]


def extract_specs_to_targets(soup: BeautifulSoup) -> Dict[str, Optional[str]]:
    collected: Dict[str, str] = {}

    for table in soup.select("table, .table, .specs, .product-specs"):
        for tr in table.select("tr"):
            th = tr.find(["th", "td"])
            tds = tr.find_all("td")
            if th and tds:
                key = normalize_key(th.get_text(" ", strip=True))
                val = " ".join(td.get_text(" ", strip=True) for td in tds if td)
                if key and val and key not in collected:
                    collected[key] = val

    for dl in soup.select("dl"):
        dts, dds = dl.find_all("dt"), dl.find_all("dd")
        if len(dts) == len(dds):
            for dt, dd in zip(dts, dds):
                key = normalize_key(dt.get_text(" ", strip=True))
                val = dd.get_text(" ", strip=True)
                if key and val and key not in collected:
                    collected[key] = val

    for row in soup.select('[class*="spec"], [class*="param"], [data-qa*="spec"]'):
        labels = [n for n in row.find_all(["div", "span"], string=True)]
        if len(labels) >= 2:
            key = normalize_key(labels[0].get_text(" ", strip=True))
            val = labels[-1].get_text(" ", strip=True)
            if key and val and key not in collected:
                collected[key] = val

    out: Dict[str, Optional[str]] = {
        k: None for k in TARGET_COLUMNS if k.startswith("spec_")
    }
    for raw_key, val in collected.items():
        if raw_key in SPEC_ALIASES:
            final_key = SPEC_ALIASES[raw_key]
            if out.get(final_key) in (None, ""):
                out[final_key] = val

    if out.get("spec_pojemno_dysku_1") is None:
        for k, v in collected.items():
            if k.startswith("spec_pojemnosc_dysku") and v:
                out["spec_pojemno_dysku_1"] = v
                break

    return out


def parse_first_jsonld_product(soup: BeautifulSoup) -> Dict:
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "")
        except Exception:
            continue
        items = data if isinstance(data, list) else [data]
        for obj in items:
            if not isinstance(obj, dict):
                continue
            t = obj.get("@type")
            if t == "Product":
                return obj
            if t in ("WebPage", "ItemPage") and isinstance(obj.get("mainEntity"), dict):
                me = obj["mainEntity"]
                if me.get("@type") == "Product":
                    return me
    return {}


def extract_product(url: str) -> Dict[str, Optional[str]]:
    soup = get_soup(url, referer=CATEGORY)
    jsonld = parse_first_jsonld_product(soup)

    name = None
    if jsonld:
        name = text_or_none(jsonld.get("name"))
    if not name:
        h1 = soup.find("h1")
        if h1:
            name = h1.get_text(" ", strip=True)

    price_val, _price_text = extract_price(soup, jsonld)

    specs = extract_specs_to_targets(soup)

    row: Dict[str, Optional[str] | float] = {
        "product_url": url,
        "name": name,
        "price": price_val,
        "spec_procesor": specs.get("spec_procesor"),
        "spec_marka_procesora": specs.get("spec_marka_procesora"),
        "spec_pami_ram": specs.get("spec_pami_ram"),
        "spec_karta_graficzna": specs.get("spec_karta_graficzna"),
        "spec_dysk": specs.get("spec_dysk"),
        "spec_pojemno_dysku_1": specs.get("spec_pojemno_dysku_1"),
        "spec_system_operacyjny": specs.get("spec_system_operacyjny"),
        "spec_typ_produktu": specs.get("spec_typ_produktu"),
        "spec_liczba_rdzeni": specs.get("spec_liczba_rdzeni"),
        "spec_pami_ram_konfiguracja": specs.get("spec_pami_ram_konfiguracja"),
    }
    return row


# Zapis do CSV
def write_csv(rows: List[Dict[str, Optional[str]]], out_path: str) -> None:
    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=TARGET_COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in TARGET_COLUMNS})


# Główna funkcja
def main(out_csv: str, pages: int) -> None:
    all_rows: List[Dict[str, Optional[str]]] = []
    seen = set()
    print(f"HTTP backend: {getattr(SESSION, '_impersonation', 'unknown')}")
    for purl in iterate_category_by_pages(CATEGORY, pages):
        if purl in seen:
            continue
        seen.add(purl)
        try:
            row = extract_product(purl)
            all_rows.append(row)
            print(f"[OK] {purl}")
        except Exception as e:
            print(f"[FAIL] {purl} ({e})", file=sys.stderr)
        polite_delay(1.0, 2.0)

    if not all_rows:
        print("No products scraped.", file=sys.stderr)
    write_csv(all_rows, out_csv)
    print(f"\nSaved {len(all_rows)} rows to {out_csv}")


# Argumenty i uruchomienie
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=15)
    parser.add_argument("--out", type=str, default="mediamarkt_desktops.csv")
    args = parser.parse_args()
    main(args.out, args.pages)

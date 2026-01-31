-- ZADANIE I
CREATE OR REPLACE FUNCTION suma_ksiazek (p_id_gat NUMBER)
RETURN NUMBER
IS
    suma NUMBER := 0;
BEGIN
    SELECT SUM(CENA)
    INTO suma
    FROM KSIAZKA
    WHERE ID_GAT = p_id_gat;
    
    RETURN suma;
END suma_ksiazek;

SELECT suma_ksiazek(3) AS suma FROM DUAL;

-- ZADANIE II
CREATE OR REPLACE FUNCTION cena_ksiazki (p_id_ksiazki NUMBER)
RETURN NUMBER
IS
    cena_brutto NUMBER := 0;
    cena_netto NUMBER := 0;
    ilosc_ksiazek NUMBER := 0;
BEGIN
    
    SELECT COUNT(*)
    INTO ilosc_ksiazek
    FROM KSIAZKA
    WHERE ID_KS = p_id_ksiazki;
    
    IF ilosc_ksiazki = 0 THEN
        RAISE_APPLICATION_ERROR(-20001,"Brak takiej ksiazki");
    END IF;
    
    IF ilosc_ksiazki > 1 THEN
        RAISE_APPLICATION_ERROR(-20001,"Du¿a iloœæ podanej ksiazki");
    END IF;
    
    SELECT CENA
    INTO cena_brutto
    FROM KSIAZKA
    WHERE ID_KS = p_id_ksiazki;
    
    cena_netto := cena_brutto * 0.92;
    
    RETURN cena_netto;
END cena_ksiazki;

SELECT cena_ksiazki(3) AS cena_netto FROM DUAL;

-- ZADANIE III
CREATE OR REPLACE PROCEDURE modyfikuj_cene_ksiazki (p_id_ksiazka NUMBER) IS
    v_cena KSIAZKA.CENA%TYPE;
BEGIN
    SELECT CENA INTO v_cena
    FROM KSIAZKA
    WHERE ID_KS = p_id_ksiazka;

    IF v_cena >= 25 THEN
        v_cena := v_cena * 1.10;
    ELSE
        v_cena := v_cena * 1.15;
    END IF;

    UPDATE KSIAZKA
    SET CENA = v_cena
    WHERE ID_KS = p_id_ksiazka;
    
    COMMIT;
END modyfikuj_cene_ksiazki;

BEGIN
    modyfikuj_cene_ksiazki(5);
END;

-- ZADANIE IV
-- DO SPRAWDZENIA
CREATE OR REPLACE PROCEDURE najstarsze_wydawnictwo IS
    v_nazwa_wydawnictwa WYDAWNICTWO.W_NAZWA%TYPE;
    v_tytul_ksiazki KSIAZKA.TYTUL%TYPE;
    v_nazwisko_autora AUTOR.NAZWISKO%TYPE;
    v_liczba_ksiazek INTEGER;
BEGIN
    -- Znalezienie liczby ksi¹¿ek o najstarszej dacie
    SELECT COUNT(*)
    INTO v_liczba_ksiazek
    FROM KSIAZKA
    WHERE DATA_WYD = (SELECT MIN(DATA_WYD) FROM KSIAZKA);

    -- Sprawdzenie, czy jest wiêcej ni¿ jedna ksi¹¿ka o najstarszej dacie
    IF v_liczba_ksiazek > 1 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Istnieje wiêcej ni¿ jedna ksi¹¿ka o najstarszej dacie wydania.');
    ELSE
        -- Pobranie szczegó³ów: nazwy wydawnictwa, tytu³u ksi¹¿ki i nazwiska autora
        SELECT W.W_NAZWA, K.TYTUL, A.NAZWISKO
        INTO v_nazwa_wydawnictwa, v_tytul_ksiazki, v_nazwisko_autora
        FROM KSIAZKA K
        JOIN WYDAWNICTWO W ON K.ID_WYD = W.ID_WYD
        JOIN AUTOR_TYTUL AUT ON K.ID_KS = AUT.ID_KS
        JOIN AUTOR A ON AUT.ID_AUT = A.ID_AUT
        WHERE K.DATA_WYD = (SELECT MIN(DATA_WYD) FROM KSIAZKA);

        DBMS_OUTPUT.PUT_LINE('Nazwa wydawnictwa: ' || v_nazwa_wydawnictwa);
        DBMS_OUTPUT.PUT_LINE('Tytu³ ksi¹¿ki: ' || v_tytul_ksiazki);
        DBMS_OUTPUT.PUT_LINE('Nazwisko autora: ' || v_nazwisko_autora);
    END IF;
END najstarsze_wydawnictwo;

-- ZADANIE V
--CREATE OR REPLACE PACKAGE ksiazki_pakiet AS
--    -- Funkcja do obliczenia liczby formatów ksi¹¿ek danego autora
--    FUNCTION liczba_formatow_autora(nazwisko IN VARCHAR2, imie IN VARCHAR2) RETURN NUMBER;
--
--    -- Procedura wyœwietlaj¹ca tytu³y ksi¹¿ek i nazwiska czytelników dla wydawnictwa z najmniejsz¹ liczb¹ ksi¹¿ek
--    PROCEDURE ksiazki_i_czytelnicy_najmniejszego_wydawnictwa;
--END ksiazki_pakiet;
--/

CREATE OR REPLACE PACKAGE BODY ksiazki_pakiet AS

    -- Funkcja do obliczenia liczby formatów ksi¹¿ek danego autora
    FUNCTION liczba_formatow_autora(nazwisko IN VARCHAR2, imie IN VARCHAR2) RETURN NUMBER IS
        v_liczba_formatow NUMBER;
    BEGIN
        SELECT COUNT(DISTINCT K.ID_FOR)
        INTO v_liczba_formatow
        FROM KSIAZKA K
        JOIN AUTOR_TYTUL AUT ON AUT.ID_KS = K.ID_KS
        JOIN AUTOR A ON AUT.ID_AUT = A.ID_AUT
        WHERE A.NAZWISKO = nazwisko AND A.IMIE = imie;

        RETURN v_liczba_formatow;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RETURN 0; -- Zwracamy 0, jeœli autor nie zosta³ znaleziony
    END liczba_formatow_autora;

    -- Procedura wyœwietlaj¹ca tytu³y ksi¹¿ek i nazwiska czytelników dla wydawnictwa z najmniejsz¹ liczb¹ ksi¹¿ek
    PROCEDURE ksiazki_i_czytelnicy_najmniejszego_wydawnictwa IS
        v_min_liczba NUMBER;
    BEGIN
        -- Znalezienie minimalnej liczby ksi¹¿ek wydanych przez wydawnictwo
        SELECT MIN(liczba_ksiazek)
        INTO v_min_liczba
        FROM (
            SELECT COUNT(*) AS liczba_ksiazek
            FROM KSIAZKA
            GROUP BY ID_WYD
        );

        -- Wyœwietlenie tytu³ów ksi¹¿ek i nazwisk czytelników dla wydawnictwa z najmniejsz¹ liczb¹ ksi¹¿ek
        FOR rec IN (
            SELECT K.TYTUL, C.NAZWISKO AS NAZWISKO_CZYTELNIKA
            FROM KSIAZKA K
            JOIN WYDAWNICTWO W ON K.ID_WYD = W.ID_WYD
            JOIN WYPOZYCZENIA WY ON WY.ID_KS = K.ID_KS
            JOIN CZYTELNIK C ON WY.ID_CZYT = C.ID_CZYT
            WHERE W.ID_WYD IN (
                SELECT ID_WYD
                FROM (
                    SELECT ID_WYD, COUNT(*) AS liczba_ksiazek
                    FROM KSIAZKA
                    GROUP BY ID_WYD
                    HAVING COUNT(*) = v_min_liczba
                )
            )
        ) LOOP
            DBMS_OUTPUT.PUT_LINE('Tytu³ ksi¹¿ki: ' || rec.TYTUL || ', Nazwisko czytelnika: ' || rec.NAZWISKO_CZYTELNIKA);
        END LOOP;
    END ksiazki_i_czytelnicy_najmniejszego_wydawnictwa;

END ksiazki_pakiet;
/

-- Wywo³anie funkcji
--DECLARE
--    liczba_formatow NUMBER;
--BEGIN
--    liczba_formatow := ksiazki_pakiet.liczba_formatow_autora('Nowak', 'Jan');
--    DBMS_OUTPUT.PUT_LINE('Liczba formatów: ' || liczba_formatow);
--END;
--/
--
---- Wywo³anie procedury
--BEGIN
--    ksiazki_pakiet.ksiazki_i_czytelnicy_najmniejszego_wydawnictwa;
--END;
--/







-- ZADANIE I
SET SERVEROUTPUT ON;

DECLARE
    v_min_wypozyczen NUMBER;
    v_liczba_czytelnikow NUMBER;
    czytelnik_info VARCHAR2(200);
BEGIN
    SELECT MIN(liczba_wypozyczen)
    INTO v_min_wypozyczen
    FROM (
    SELECT COUNT(w.id_czyt) AS liczba_wypozyczen
    FROM wypozyczenia w
    GROUP BY w.id_czyt
    );
    
    SELECT COUNT(*)
    INTO v_liczba_czytelnikow
    FROM czytelnik c
    JOIN wypozyczenia w ON c.id_czyt = w.id_czyt
    GROUP BY c.imie, c.nazwisko
    HAVING COUNT(w.id_czyt) = v_min_wypozyczen;
    
    IF v_liczba_czytelnikow > 1 THEN
    RAISE TOO_MANY_ROWS;
    END IF;
    
    SELECT c.imie || ' ' || c.nazwisko || ' ma najmniejsz¹ liczbê wypo¿yczeñ: ' || v_min_wypozyczen
    INTO czytelnik_info
    FROM czytelnik c
    JOIN wypozyczenia w ON c.id_czyt = w.id_czyt
    GROUP BY c.imie, c.nazwisko
    HAVING COUNT(w.id_czyt) = v_min_wypozyczen;
    
    DBMS_OUTPUT.PUT_LINE(czytelnik_info);
    
EXCEPTION
    WHEN TOO_MANY_ROWS THEN
    DBMS_OUTPUT.PUT_LINE('B³¹d: Wiêcej ni¿ jeden czytelnik ma najmniejsz¹ liczbê wypo¿yczeñ.');
    WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Wyst¹pi³ nieoczekiwany b³¹d: ' || SQLERRM);
END;

-- ZADANIE II
DECLARE
    max_price NUMBER;
    books_count NUMBER;
    genre VARCHAR(20);
BEGIN
    SELECT MAX(k.cena)
    INTO max_price
    FROM ksiazka k;
    
    SELECT COUNT(*)
    INTO books_count
    FROM ksiazka k
    WHERE k.cena = max_price;
    
    IF books_count > 1 THEN
        RAISE TOO_MANY_ROWS;
    END IF;
    
    SELECT g.g_nazwa
    INTO genre
    FROM gatunek g
    JOIN ksiazka k ON g.id_gat = k.id_gat
    WHERE k.cena = max_price;
    
    DBMS_OUTPUT.PUT_LINE('Gatunek z najdrozsza ksiazka to: ' || genre || ' i kosztuje: ' || max_price);

EXCEPTION
    WHEN TOO_MANY_ROWS THEN
        DBMS_OUTPUT.PUT_LINE('Blad: wiecej ni¿ jedna ksiazka' || books_count);
END;

-- Zadanie III
CREATE OR REPLACE TRIGGER trg_autor_insert
AFTER INSERT ON AUTOR
FOR EACH ROW
BEGIN
    INSERT INTO AUTOR_LOG (ID_AUT, NAZWISKO, IMIE, KRAJ, LOG_OPERATION)
    VALUES (:NEW.ID_AUT, :NEW.NAZWISKO, :NEW.IMIE, :NEW.KRAJ, 'INSERT');
END;

INSERT INTO AUTOR (ID_AUT, NAZWISKO, IMIE, KRAJ)
VALUES (16, 'Nowak', 'Jan', 'Polska');
SELECT * FROM AUTOR_LOG;
SHOW ERRORS TRIGGER TRG_AUTOR_INSERT;
DROP TRIGGER trg_autor_insert;

-- ZADANIE IV
CREATE OR REPLACE TRIGGER trg_autor_dorian_check
BEFORE INSERT ON AUTOR
FOR EACH ROW
BEGIN
    IF :NEW.NAZWISKO = 'Dorian' THEN
        RAISE_APPLICATION_ERROR(-20001, 'Nie mo¿na wstawiæ rekordu z nazwiskiem "Dorian".');
    END IF;
END;

INSERT INTO AUTOR (ID_AUT, NAZWISKO, IMIE, KRAJ)
VALUES (17, 'Dorian', 'Jan', 'Polska');
INSERT INTO AUTOR (ID_AUT, NAZWISKO, IMIE, KRAJ)
VALUES (18, 'Kowalski', 'Jan', 'Polska');
-- ZADANIE V
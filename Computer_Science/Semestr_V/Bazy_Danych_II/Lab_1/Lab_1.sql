-- Zadanie I
SELECT c.IMIE || ' ' || c.NAZWISKO AS DANE_CZYTELNIKA,
COUNT(DISTINCT g.g_nazwa) AS ILOSC 
FROM CZYTELNIK c
INNER JOIN WYPOZYCZENIA w ON w.id_czyt = c.id_czyt
INNER JOIN KSIAZKA k ON k.id_ks = w.id_ks
INNER JOIN GATUNEK g ON g.id_gat = k.id_gat
GROUP BY c.IMIE || ' ' || c.NAZWISKO
ORDER BY ILOSC DESC;

-- Zadanie II
SELECT COUNT(*) AS ILOSC FROM KSIAZKA
WHERE ID_WYD = (SELECT ID_WYD FROM KSIAZKA
WHERE DATA_WYD = (SELECT MIN(DATA_WYD) FROM KSIAZKA));

-- Zadanie III
SELECT F.F_NAZWA AS FORMAT_NAME, COUNT(W.ID_KS) AS BORROW_COUNT
FROM WYPOZYCZENIA W
JOIN KSIAZKA K ON W.ID_KS = K.ID_KS
JOIN FORMAT F ON K.ID_FOR = F.ID_FOR
WHERE W.DATA_WYP >= ADD_MONTHS(SYSDATE, -3)
GROUP BY F.F_NAZWA
ORDER BY BORROW_COUNT DESC
FETCH FIRST 1 ROWS ONLY;

-- Zadanie IV
SELECT GENRE_NAME
FROM GenreBorrowCount
WHERE BORROW_COUNT > (SELECT AVG_BORROW_COUNT FROM AverageBorrowCount);
SELECT G.G_NAZWA AS GENRE_NAME, COUNT(K.ID_KS) AS BOOK_COUNT, SUM(K.CENA) AS TOTAL_PRICE
FROM KSIAZKA K
JOIN GATUNEK G ON K.ID_GAT = G.ID_GAT
GROUP BY G.G_NAZWA
ORDER BY G.G_NAZWA;

-- Zadanie V
WITH GenreBorrowCount AS (
    SELECT G.G_NAZWA AS GENRE_NAME, COUNT(W.ID_KS) AS BORROW_COUNT
    FROM WYPOZYCZENIA W
    JOIN KSIAZKA K ON W.ID_KS = K.ID_KS
    JOIN GATUNEK G ON K.ID_GAT = G.ID_GAT
    GROUP BY G.G_NAZWA
),
AverageBorrowCount AS (
    SELECT AVG(BORROW_COUNT) AS AVG_BORROW_COUNT
    FROM GenreBorrowCount
)
SELECT GENRE_NAME
FROM GenreBorrowCount
WHERE BORROW_COUNT > (SELECT AVG_BORROW_COUNT FROM AverageBorrowCount);

-- Zadanie VI
SELECT DISTINCT A.*
FROM AUTOR A
JOIN AUTOR_TYTUL AT ON A.ID_AUT = AT.ID_AUT
JOIN KSIAZKA K ON AT.ID_KS = K.ID_KS
WHERE K.ID_GAT = (
        SELECT ID_GAT FROM KSIAZKA
        WHERE L_STRON = (SELECT MIN(L_STRON) FROM KSIAZKA));
        
-- Zadanie VII
DECLARE
    n NUMBER;
    result NUMBER := 1;
BEGIN
    n := &n;
    FOR i IN 1..n LOOP
        result := result * i;
    END LOOP;

    DBMS_OUTPUT.PUT_LINE('Silnia z ' || n || ' to ' || result);
END;

-- Zadanie VIII
DECLARE
    TYPE student_record IS RECORD (
        id        CZYTELNIK.ID_CZYT%TYPE,
        last_name CZYTELNIK.NAZWISKO%TYPE,
        city      CZYTELNIK.MIASTO%TYPE,
        phone     CZYTELNIK.TELEFON%TYPE
    );
    student student_record;
BEGIN
    SELECT ID_CZYT, NAZWISKO, MIASTO, TELEFON
    INTO student.id, student.last_name, student.city, student.phone
    FROM CZYTELNIK
    WHERE ROWNUM = 1;
    DBMS_OUTPUT.PUT_LINE('ID: ' || student.id);
    DBMS_OUTPUT.PUT_LINE('Last Name: ' || student.last_name);
    DBMS_OUTPUT.PUT_LINE('City: ' || student.city);
    DBMS_OUTPUT.PUT_LINE('Phone: ' || student.phone);
END;

-- Zadanie IX
DECLARE
    a NUMBER;
    b NUMBER;
    temp NUMBER;
BEGIN
    a := &a;
    b := &b;

    IF a < 0 THEN
        a := -a;
    END IF;
    IF b < 0 THEN
        b := -b;
    END IF;

    WHILE b != 0 LOOP
        temp := b;
        b := MOD(a, b);
        a := temp;
    END LOOP;
    DBMS_OUTPUT.PUT_LINE(' NWD: ' || a);
END;

-- Zadanie X
DECLARE
    n NUMBER;
    a NUMBER := 0;
    b NUMBER := 1;
    temp NUMBER;
BEGIN
    n := &n;
    DBMS_OUTPUT.PUT_LINE(a);
    IF n > 1 THEN
        DBMS_OUTPUT.PUT_LINE(b);
    END IF;

    FOR i IN 3..n LOOP
        temp := a + b;
        DBMS_OUTPUT.PUT_LINE(temp);
        a := b;
        b := temp;
    END LOOP;
END;
-- ZADANIE I
-- Wariant I
DECLARE
    TYPE AutorRecord IS RECORD (
        ID_AUT AUTOR.ID_AUT%TYPE,
        NAZWISKO AUTOR.NAZWISKO%TYPE,
        IMIE AUTOR.IMIE%TYPE,
        KRAJ AUTOR.KRAJ%TYPE
    );
    autor_rec AutorRecord;
    CURSOR c_autor IS
        SELECT ID_AUT, NAZWISKO, IMIE, KRAJ FROM AUTOR;
BEGIN
    OPEN c_autor;
    LOOP
        FETCH c_autor INTO autor_rec;
        EXIT WHEN c_autor%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE('ID: ' || autor_rec.ID_AUT || ', Nazwisko: ' || autor_rec.NAZWISKO || ', Imiê: ' || autor_rec.IMIE || ', Kraj: ' || autor_rec.KRAJ);
    END LOOP;
    CLOSE c_autor;
END;

-- Wariant II
DECLARE
    autor_rec AUTOR%ROWTYPE;
    CURSOR c_autor IS
        SELECT * FROM AUTOR;
BEGIN
    OPEN c_autor;
    LOOP
        FETCH c_autor INTO autor_rec;
        EXIT WHEN c_autor%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE('ID: ' || autor_rec.ID_AUT || ', Nazwisko: ' || autor_rec.NAZWISKO || ', Imiê: ' || autor_rec.IMIE || ', Kraj: ' || autor_rec.KRAJ);
    END LOOP;
    CLOSE c_autor;
END;

-- Wariant III
BEGIN
    FOR autor_rec IN (SELECT * FROM AUTOR) LOOP
        DBMS_OUTPUT.PUT_LINE('ID: ' || autor_rec.ID_AUT || ', Nazwisko: ' || autor_rec.NAZWISKO || ', Imiê: ' || autor_rec.IMIE || ', Kraj: ' || autor_rec.KRAJ);
    END LOOP;
END;

-- ZADANIE II
DECLARE
  CURSOR czytelnicy_cursor IS
    SELECT imie, nazwisko, miasto
    FROM czytelnik
    ORDER BY nazwisko DESC;  

  imie czytelnik.imie%TYPE;
  nazwisko czytelnik.nazwisko%TYPE;
  miasto czytelnik.miasto%TYPE;

BEGIN
  OPEN czytelnicy_cursor;
  LOOP
    FETCH czytelnicy_cursor INTO imie, nazwisko, miasto;
    EXIT WHEN czytelnicy_cursor%NOTFOUND;  
    DBMS_OUTPUT.PUT_LINE(INITCAP(imie) || ' *******' || UPPER(nazwisko) || ' ********' || INITCAP(miasto));
  END LOOP;
  CLOSE czytelnicy_cursor;
END;

-- ZADANIE III
SELECT
    c.IMIE || ' ' || c.NAZWISKO AS CZYTELNIK,
    TO_CHAR(w.DATA_WYP, 'DD') AS DZIEÑ,
    UPPER(TO_CHAR(w.DATA_WYP, 'MONTH', 'NLS_DATE_LANGUAGE=ENGLISH')) AS MIESI¥C,
    k.TYTUL AS TYTUL_KSIAZKI,
    f.F_NAZWA AS FORMAT
FROM WYPOZYCZENIA w
JOIN CZYTELNIK c ON w.ID_CZYT = c.ID_CZYT
JOIN KSIAZKA k ON w.ID_KS = k.ID_KS
JOIN FORMAT f ON k.ID_FOR = f.ID_FOR;

-- ZADANIE IV
DECLARE
    CURSOR c_ksiazki (min_cena NUMBER) IS
        SELECT DISTINCT k.tytul, a.nazwisko AS autor_nazwisko, w.w_nazwa AS wydawnictwo, wyp.data_zwr, k.cena
        FROM ksiazka k
        JOIN autor_tytul at ON k.id_ks = at.id_ks
        JOIN autor a ON at.id_aut = a.id_aut
        JOIN wydawnictwo w ON k.id_wyd = w.id_wyd
        JOIN wypozyczenia wyp ON k.id_ks = wyp.id_ks
        WHERE k.cena >= min_cena AND wyp.data_zwr > SYSDATE
        ORDER BY k.cena DESC;

    v_min_cena NUMBER;
    v_ksiazki_rec c_ksiazki%ROWTYPE;
BEGIN
    v_min_cena := &Cena;
    OPEN c_ksiazki(v_min_cena);
    LOOP
        FETCH c_ksiazki INTO v_ksiazki_rec;
        EXIT WHEN c_ksiazki%NOTFOUND OR c_ksiazki%ROWCOUNT > 3;

        DBMS_OUTPUT.PUT_LINE('Tytu³: ' || v_ksiazki_rec.tytul);
        DBMS_OUTPUT.PUT_LINE('Autor: ' || v_ksiazki_rec.autor_nazwisko);
        DBMS_OUTPUT.PUT_LINE('Wydawnictwo: ' || v_ksiazki_rec.wydawnictwo);
        DBMS_OUTPUT.PUT_LINE('Data zwrotu: ' || TO_CHAR(v_ksiazki_rec.data_zwr, 'YYYY-MM-DD'));
        DBMS_OUTPUT.PUT_LINE('-----------------------------');
    END LOOP;
    CLOSE c_ksiazki;
END;

-- ZADANIE V
-- Wariant I
DECLARE
  CURSOR c_books_by_format IS
    SELECT F_NAZWA, COUNT(*) AS book_count
    FROM KSIAZKA k
    JOIN FORMAT f ON k.ID_FOR = f.ID_FOR
    GROUP BY f.F_NAZWA;
  v_format_name VARCHAR2(30);
  v_book_count NUMBER;
BEGIN
  OPEN c_books_by_format;
  LOOP
    FETCH c_books_by_format INTO v_format_name, v_book_count;
    EXIT WHEN c_books_by_format%NOTFOUND;
    DBMS_OUTPUT.PUT_LINE('Format: ' || v_format_name || ' - Liczba ksi¹¿ek: ' || v_book_count);
  END LOOP;
  CLOSE c_books_by_format;
END;

-- Wariant II
DECLARE
  p_format_name VARCHAR2(30) := 'EBOOK';
  CURSOR c_books_by_format IS
    SELECT F_NAZWA, COUNT(*) AS book_count
    FROM KSIAZKA k
    JOIN FORMAT f ON k.ID_FOR = f.ID_FOR
    WHERE f.F_NAZWA = p_format_name
    GROUP BY f.F_NAZWA;
  v_format_name VARCHAR2(30);
  v_book_count NUMBER;
BEGIN
  OPEN c_books_by_format;
  FETCH c_books_by_format INTO v_format_name, v_book_count;
  IF c_books_by_format%FOUND THEN
    DBMS_OUTPUT.PUT_LINE('Format: ' || v_format_name || ' - Liczba ksi¹¿ek: ' || v_book_count);
  ELSE
    DBMS_OUTPUT.PUT_LINE('Brak ksi¹¿ek w formacie: ' || p_format_name);
  END IF;
  CLOSE c_books_by_format;
END;

-- ZADANIE VI
-- Wariant I
DECLARE
    CURSOR c_ksiazki IS
        SELECT k.id_ks, k.cena, w.w_nazwa
        FROM ksiazka k
        JOIN wydawnictwo w ON k.id_wyd = w.id_wyd;

    v_now_ksiazki_rec c_ksiazki%ROWTYPE;
BEGIN
    OPEN c_ksiazki;
    LOOP
        FETCH c_ksiazki INTO v_now_ksiazki_rec;
        EXIT WHEN c_ksiazki%NOTFOUND;

        IF v_now_ksiazki_rec.w_nazwa = 'Litera' THEN
            UPDATE ksiazka
            SET cena = cena * 1.10
            WHERE CURRENT OF c_ksiazki;
            DBMS_OUTPUT.PUT_LINE('Zaktualizowano cenê ksi¹¿ki (ID: ' || v_now_ksiazki_rec.id_ks || ') na ' || v_now_ksiazki_rec.cena * 1.10);
        ELSE
            UPDATE ksiazka
            SET cena = cena * 1.05
            WHERE CURRENT OF c_ksiazki;
            DBMS_OUTPUT.PUT_LINE('Zaktualizowano cenê ksi¹¿ki (ID: ' || v_now_ksiazki_rec.id_ks || ') na ' || v_now_ksiazki_rec.cena * 1.05);
        END IF;
    END LOOP;

    CLOSE c_ksiazki;
    DBMS_OUTPUT.PUT_LINE('Ceny ksi¹¿ek zosta³y zaktualizowane.');
END;

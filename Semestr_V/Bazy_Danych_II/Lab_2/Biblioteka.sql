-- SKRYPT TWORZACY OBIEKTY DO CWICZEN

CREATE TABLE GATUNEK (
     ID_GAT   NUMBER(4)   CONSTRAINT PK_ID_GAT PRIMARY KEY,
     G_NAZWA     VARCHAR2(30) 
     );

CREATE TABLE WYDAWNICTWO (
     ID_WYD   NUMBER(4)   CONSTRAINT PK_ID_WYD PRIMARY KEY,
     W_NAZWA     VARCHAR2(30) 
     );

CREATE TABLE AUTOR(
     ID_AUT   NUMBER(4)   CONSTRAINT PK_ID_AUT PRIMARY KEY,
     NAZWISKO     VARCHAR2(30),
     IMIE	  VARCHAR2(30),
     KRAJ VARCHAR2(30)
     );


CREATE TABLE FORMAT (
     ID_FOR   NUMBER(4)   CONSTRAINT PK_ID_FOR PRIMARY KEY,
     F_NAZWA     VARCHAR2(30) 
     );

CREATE TABLE CZYTELNIK ( 
     ID_CZYT     NUMBER(4)   CONSTRAINT PK_ID_CZYT PRIMARY KEY,
     NAZWISKO    VARCHAR2(15),
     IMIE        VARCHAR2(15),
     KOD_POCZTOWY  VARCHAR2(6), 
     MIASTO VARCHAR2(25),
     ULICA       VARCHAR2(25),
     TELEFON	 VARCHAR2(20)
);

CREATE TABLE KSIAZKA( 
     ID_KS     NUMBER(4)   CONSTRAINT PK_ID_KS PRIMARY KEY,
     TYTUL    VARCHAR2(100),
     CENA     NUMBER(5,2),
     ID_GAT   NUMBER(4) CONSTRAINT FK_ID_GAT REFERENCES GATUNEK(ID_GAT),
     ID_WYD   NUMBER(4) CONSTRAINT FK_ID_WYD REFERENCES WYDAWNICTWO(ID_WYD),
     ID_FOR   NUMBER(4) CONSTRAINT FK_ID_FOR REFERENCES FORMAT(ID_FOR),    
     DATA_WYD DATE,
     L_STRON  NUMBER(4)
);

CREATE TABLE AUTOR_TYTUL(
     ID_AUT   NUMBER(4)   CONSTRAINT FK_ID_AUTOR REFERENCES AUTOR(ID_AUT),
     ID_KS   NUMBER(4)	  CONSTRAINT FK_ID_KSI REFERENCES KSIAZKA(ID_KS)
     );

CREATE TABLE WYPOZYCZENIA (
     ID_WYP   NUMBER(4) CONSTRAINT PK_ID_WYP PRIMARY KEY,
     ID_KS   NUMBER(4) CONSTRAINT FK_ID_KS REFERENCES KSIAZKA(ID_KS),
     ID_CZYT   NUMBER(4) CONSTRAINT FK_ID_CZYT REFERENCES CZYTELNIK(ID_CZYT),
     DATA_WYP DATE,
     DATA_ZWR DATE
  
);


-- WSTAWIANIE DANYCH
INSERT INTO WYDAWNICTWO Values (1,  'PWN');
INSERT INTO WYDAWNICTWO Values (2,  'Litera');
INSERT INTO WYDAWNICTWO Values (3,  'Helion');
INSERT INTO WYDAWNICTWO Values (4,  'Flamarion');
INSERT INTO WYDAWNICTWO Values (5,  'Znak');
INSERT INTO WYDAWNICTWO Values (6,  'Proza');
INSERT INTO WYDAWNICTWO Values (7,  'Sowa');
INSERT INTO WYDAWNICTWO Values (8,  'Muza');


INSERT INTO GATUNEK Values (1,  'Poezja');
INSERT INTO GATUNEK Values (2,  'Dramat');
INSERT INTO GATUNEK Values (3,  'Krymina?');
INSERT INTO GATUNEK Values (4,  'Horror');
INSERT INTO GATUNEK Values (5,  'Fantastyka');
INSERT INTO GATUNEK Values (6,  'Podr?e');
INSERT INTO GATUNEK Values (7,  'Poradnik');
INSERT INTO GATUNEK Values (8,  'Dzienniki');

INSERT INTO AUTOR Values (1,  'Mickiewicz','Adam', 'Polska');
INSERT INTO AUTOR Values (2,  'S?owacki','Juliusz', 'Polska');
INSERT INTO AUTOR Values (3,  'Aseron','Juan', 'Hiszpania');
INSERT INTO AUTOR Values (4,  'Tren','Jan', 'Polska');
INSERT INTO AUTOR Values (5,  'Kowal','Dariusz', 'Polska');
INSERT INTO AUTOR Values (6,  'Porter','Emma', 'USA');
INSERT INTO AUTOR Values (7,  'Christie','Agatha', 'Anglia');
INSERT INTO AUTOR Values (8,  'Monro','Manuela', 'Hiszpania');
INSERT INTO AUTOR Values (9,  'Smith','William','Anglia');
INSERT INTO AUTOR Values (10,  'Lindgren','Astrid','Szwecja');
INSERT INTO AUTOR Values (11,  'Goethe','Anna','Niemcy');
INSERT INTO AUTOR Values (12,  'Jao','Tiago','Portugalia');
INSERT INTO AUTOR Values (13,  'Luna','Amelia','Francja');
INSERT INTO AUTOR Values (14,  'Nilson','Emil','Szwecja');
INSERT INTO AUTOR Values (15,  'Bond','James','Anglia');

INSERT INTO FORMAT Values (1,  'EBOOK');
INSERT INTO FORMAT Values (2,  'PAPIER');
INSERT INTO FORMAT Values (3,  'AUDIOBOOK');



INSERT INTO CZYTELNIK VALUES (1,'KOWALSKI','PIOTR','31-234','WARSZAWA','DLUGA 8/12', '123456789');
INSERT INTO CZYTELNIK VALUES (2,'NOWAK','JAN','43-345','WROC?AW','NORWIDA 2/1','987654321');
INSERT INTO CZYTELNIK VALUES (3,'ADAMCZYK','PAWEL','55-123','SOPOT','KR?TKA 2','345677654');
INSERT INTO CZYTELNIK VALUES (4,'BRACKI','BOGDAN','32-422','GDYNIA','BA?TYCKA 67/4','876598457');
INSERT INTO CZYTELNIK VALUES (5,'LIPKA','JAKUB','33-100','KATOWICE','POLNA 9','322143215');
INSERT INTO CZYTELNIK VALUES (6,'NOWICKI','TOMASZ','42-422','KRAK?W','SZEWSKA 8/10','432756439');
INSERT INTO CZYTELNIK VALUES (7,'LIS','ANITA','77-345','KRAK?W','MIKO?AJSKA 20/10','874536932');
INSERT INTO CZYTELNIK VALUES (8,'DUDEK','AGATA','33-345','WARSZAWA','KOTLARSKA 9','564783457');
INSERT INTO CZYTELNIK VALUES (9,'GIL','KRYSTYNA','22-780','GDYNIA','WOLNA 77/44','985327548');
INSERT INTO CZYTELNIK VALUES (10,'S?OWIK','WERONIKA','87-456','KRAK?W','SZLAK 23/56','665766685');
INSERT INTO CZYTELNIK VALUES (11,'SOSNA','AMELIA','11-486','SOPOT','SOLNA 56','665333685');
INSERT INTO CZYTELNIK VALUES (12,'SIKORA','WIKTOR','87-456','KATOWICE','WARSZAWSKA 24','998766685');


INSERT INTO KSIAZKA VALUES (1,'PAN TADEUSZ',30.00,1,2,1,to_date('2024-01-16','YYYY-MM-DD'),400);
INSERT INTO KSIAZKA  VALUES (2,'KORDIAN',25.80,2,2,2,to_date('2023-01-25','YYYY-MM-DD'),200);
INSERT INTO KSIAZKA  VALUES (3,'DZIADY', 20.00, 2,2,1,to_date('2024-01-30','YYYY-MM-DD'), 155);
INSERT INTO KSIAZKA  VALUES (4,'LOKOMOTYWA',15.25,3,4,3,to_date('2023-11-30','YYYY-MM-DD'),15 );
INSERT INTO KSIAZKA  VALUES (5,'POLLYANNA' ,40.00,7,2,2,to_date('2024-08-03','YYYY-MM-DD'),226 );
INSERT INTO KSIAZKA  VALUES (6,'POLANA',34.44,7,2,2,to_date('2024-02-16','YYYY-MM-DD'),245);
INSERT INTO KSIAZKA  VALUES (7,'ZMIERZCH',50.55,3,2,1,to_date('2019-05-15','YYYY-MM-DD'),345);
INSERT INTO KSIAZKA  VALUES (8,'TAJEMNICA ZAMKU',25.50,7,2,1,to_date('2021-01-26','YYYY-MM-DD'),258);
INSERT INTO KSIAZKA  VALUES (9,'SZKOCJA',44.00,4,6,3,to_date('2022-09-16','YYYY-MM-DD'),120);
INSERT INTO KSIAZKA  VALUES (10,'HRABIA',14.00,3,8,3,to_date('2023-03-16','YYYY-MM-DD'),10);
INSERT INTO KSIAZKA VALUES (11,'SQL',130.00,1,4,1,to_date('2022-07-16','YYYY-MM-DD'),400);
INSERT INTO KSIAZKA  VALUES (12,'PROGRAMOWANIE',65.50,2,2,2,to_date('2019-01-25','YYYY-MM-DD'),220);
INSERT INTO KSIAZKA  VALUES (13,'LISTY DOMOWE', 20.99, 2,2,1,to_date('2018-01-30','YYYY-MM-DD'), 55);
INSERT INTO KSIAZKA  VALUES (14,'LOKACJA MIASTA',72.00,3,4,3,to_date('2020-11-30','YYYY-MM-DD'),150 );
INSERT INTO KSIAZKA  VALUES (15,'PLAN ROCZNY',40.00,7,2,2,to_date('2022-08-03','YYYY-MM-DD'),239 );
INSERT INTO KSIAZKA  VALUES (16,'MORZE CZERWONE',39.99,7,2,2,to_date('2021-03-06','YYYY-MM-DD'),220);
INSERT INTO KSIAZKA  VALUES (17,'NIEZNAJOMY',59.00,5,1,2,to_date('2020-05-15','YYYY-MM-DD'),300);
INSERT INTO KSIAZKA  VALUES (18,'OGRODNIK',55.00,7,7,1,to_date('2023-04-16','YYYY-MM-DD'),310);
INSERT INTO KSIAZKA  VALUES (19,'ZAPISKI',25.50,8,2,1,to_date('2021-06-26','YYYY-MM-DD'),258);
INSERT INTO KSIAZKA  VALUES (20,'NOWY DOM',49.99,2,7,3,to_date('2022-04-04','YYYY-MM-DD'),999);



INSERT INTO AUTOR_TYTUL VALUES (1,1);
INSERT INTO AUTOR_TYTUL VALUES (2,1);
INSERT INTO AUTOR_TYTUL VALUES (2,2);
INSERT INTO AUTOR_TYTUL VALUES (3,3);
INSERT INTO AUTOR_TYTUL VALUES (4,4);
INSERT INTO AUTOR_TYTUL VALUES (6,6);
INSERT INTO AUTOR_TYTUL VALUES (7,6);
INSERT INTO AUTOR_TYTUL VALUES (3,9);
INSERT INTO AUTOR_TYTUL VALUES (4,10);
INSERT INTO AUTOR_TYTUL VALUES (10,7);
INSERT INTO AUTOR_TYTUL VALUES (10,8);
INSERT INTO AUTOR_TYTUL VALUES (13,8);
INSERT INTO AUTOR_TYTUL VALUES (11,11);
INSERT INTO AUTOR_TYTUL VALUES (1,13);
INSERT INTO AUTOR_TYTUL VALUES (12,12);
INSERT INTO AUTOR_TYTUL VALUES (13,18);
INSERT INTO AUTOR_TYTUL VALUES (14,20);
INSERT INTO AUTOR_TYTUL VALUES (15,17);
INSERT INTO AUTOR_TYTUL VALUES (11,7);
INSERT INTO AUTOR_TYTUL VALUES (14,15);
INSERT INTO AUTOR_TYTUL VALUES (10,4);
INSERT INTO AUTOR_TYTUL VALUES (10,19);
INSERT INTO AUTOR_TYTUL VALUES (1,13);
INSERT INTO AUTOR_TYTUL VALUES (3,10);
INSERT INTO AUTOR_TYTUL VALUES (15,16);
INSERT INTO AUTOR_TYTUL VALUES (5,17);



INSERT INTO WYPOZYCZENIA VALUES (1,1,1,to_date('2024-01-16','YYYY-MM-DD'),to_date('2024-02-15','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (2,11,3,to_date('2024-02-08','YYYY-MM-DD'),to_date('2024-04-17','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (3,4,2,to_date('2024-09-10','YYYY-MM-DD'),to_date('2025-01-11','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (4,4,5,to_date('2023-12-30','YYYY-MM-DD'),to_date('2024-01-14','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (5,6,1,to_date('2024-01-10','YYYY-MM-DD'),to_date('2024-01-29','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (6,6,3,to_date('2023-11-27','YYYY-MM-DD'),to_date('2024-02-05','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (7,2,5,to_date('2024-01-11','YYYY-MM-DD'),to_date('2024-07-02','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (8,17,3,to_date('2023-11-02','YYYY-MM-DD'),to_date('2024-01-30','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (9,6,7,to_date('2024-02-15','YYYY-MM-DD'),to_date('2024-06-01','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (10,1,6,to_date('2024-02-16','YYYY-MM-DD'),to_date('2024-10-01','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (11,1,1,to_date('2024-01-16','YYYY-MM-DD'),to_date('2024-06-15','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (12,3,3,to_date('2023-04-08','YYYY-MM-DD'),to_date('2023-04-17','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (13,14,12,to_date('2023-03-10','YYYY-MM-DD'),to_date('2023-04-11','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (14,14,5, to_date('2023-12-30','YYYY-MM-DD'),to_date('2024-01-14','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (15,16,1,to_date('2024-01-10','YYYY-MM-DD'),to_date('2024-08-29','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (16,6,3, to_date('2023-11-27','YYYY-MM-DD'),to_date('2024-02-05','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (17,2,5, to_date('2024-01-04','YYYY-MM-DD'),to_date('2024-01-22','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (18,1,6, to_date('2023-09-02','YYYY-MM-DD'),to_date('2023-09-30','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (19,6,7, to_date('2023-07-15','YYYY-MM-DD'),to_date('2023-09-01','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (20,1,6, to_date('2024-11-16','YYYY-MM-DD'),to_date('2024-12-01','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (21,1,11, to_date('2024-01-16','YYYY-MM-DD'),to_date('2024-02-15','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (22,1,1, to_date('2024-04-08','YYYY-MM-DD'),to_date('2024-04-17','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (23,14,12, to_date('2024-09-10','YYYY-MM-DD'),to_date('2024-11-19','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (24,4,5,to_date('2023-12-30','YYYY-MM-DD'),to_date('2024-01-14','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (25,6,11,to_date('2024-01-10','YYYY-MM-DD'),to_date('2024-05-29','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (26,6,3, to_date('2023-11-27','YYYY-MM-DD'),to_date('2024-02-05','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (27,2,5,to_date('2024-01-01','YYYY-MM-DD'),to_date('2024-01-04','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (28,1,6, to_date('2024-11-02','YYYY-MM-DD'),to_date('2024-12-30','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (29,4,7, to_date('2023-02-15','YYYY-MM-DD'),to_date('2023-02-24','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (30,1,9, to_date('2023-02-16','YYYY-MM-DD'),to_date('2023-12-01','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (31,1,6, to_date('2024-01-16','YYYY-MM-DD'),to_date('2024-02-15','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (32,1,3,to_date('2024-02-28','YYYY-MM-DD'),to_date('2024-04-17','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (33,4,2, to_date('2022-09-10','YYYY-MM-DD'),to_date('2022-11-11','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (34,4,12, to_date('2023-02-26','YYYY-MM-DD'),to_date('2023-08-14','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (35,6,5, to_date('2023-01-10','YYYY-MM-DD'),to_date('2023-06-29','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (36,5,9, to_date('2024-08-27','YYYY-MM-DD'),to_date('2024-09-05','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (37,2,4, to_date('2024-02-01','YYYY-MM-DD'),to_date('2024-02-09','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (38,1,6, to_date('2024-01-09','YYYY-MM-DD'),to_date('2024-03-30','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (39,6,7, to_date('2024-01-15','YYYY-MM-DD'),to_date('2024-08-01','YYYY-MM-DD'));
INSERT INTO WYPOZYCZENIA VALUES (40,1,4, to_date('2024-02-16','YYYY-MM-DD'),to_date('2024-12-01','YYYY-MM-DD'));

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
BEGIN
  FOR czytelnik_wynik IN (
    SELECT c.imie, c.nazwisko, 
           TO_CHAR(w.data_wypozyczenia, 'DD') AS dzien,
           TO_CHAR(w.data_wypozyczenia, 'MONTH', 'NLS_DATE_LANGUAGE=ENGLISH') AS miesiac,
           k.tytul, k.format
    FROM wypozyczenia w
    INNER JOIN czytelnicy c ON w.czytelnik_id = c.id  -- Zmiana na w³aœciw¹ nazwê kolumny
    INNER JOIN ksiazki k ON w.ksiazka_id = k.id       -- Zmiana na w³aœciw¹ nazwê kolumny
  )
  LOOP
    DBMS_OUTPUT.PUT_LINE(czytelnik_wynik.imie || ' ' || czytelnik_wynik.nazwisko || ' ' || 
                         czytelnik_wynik.dzien || ' ' || TRIM(czytelnik_wynik.miesiac) || ' ' || 
                         czytelnik_wynik.tytul || ' ' || czytelnik_wynik.format);
  END LOOP;
END;

-- ZADADNIE IV
DECLARE
  v_cena_minimalna NUMBER := :cena_uzytkownika; -- cena podana przez u¿ytkownika
  CURSOR c_ksiazki(cena_min NUMBER) IS
    SELECT k.TYTUL, a.NAZWISKO, w.W_NAZWA, wyp.DATA_ZWR, k.CENA
    FROM KSIAZKA k
    JOIN AUTOR_TYTUL at ON k.ID_KS = at.ID_KS
    JOIN AUTOR a ON at.ID_AUT = a.ID_AUT
    JOIN WYDAWNICTWO w ON k.ID_WYD = w.ID_WYD
    JOIN WYPOZYCZENIA wyp ON k.ID_KS = wyp.ID_KS
    WHERE k.CENA >= cena_min
    ORDER BY k.CENA DESC;

  v_ksiazki_row c_ksiazki%ROWTYPE; -- zmienna do przechowywania bie¿¹cego rekordu z kursora
BEGIN
  OPEN c_ksiazki(v_cena_minimalna);
  LOOP
    FETCH c_ksiazki INTO v_ksiazki_row;
    EXIT WHEN c_ksiazki%NOTFOUND OR c_ksiazki%ROWCOUNT > 3; -- limit wyników do 3 najdro¿szych ksi¹¿ek

    -- Wyœwietlenie danych o wypo¿yczonej ksi¹¿ce
    DBMS_OUTPUT.PUT_LINE('Tytu³: ' || v_ksiazki_row.TYTUL);
    DBMS_OUTPUT.PUT_LINE('Autor: ' || v_ksiazki_row.NAZWISKO);
    DBMS_OUTPUT.PUT_LINE('Wydawnictwo: ' || v_ksiazki_row.W_NAZWA);
    DBMS_OUTPUT.PUT_LINE('Data zwrotu: ' || TO_CHAR(v_ksiazki_row.DATA_ZWR, 'YYYY-MM-DD'));
    DBMS_OUTPUT.PUT_LINE('Cena: ' || v_ksiazki_row.CENA);
    DBMS_OUTPUT.PUT_LINE('-------------------------');
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
  -- Kursor pobieraj¹cy ksi¹¿ki i ich ceny
  CURSOR c_books IS
    SELECT ID_KSI, CENA, WYDAWNICTWO
    FROM KSIAZKA k
    JOIN WYDAWNICTWO w ON k.ID_WYD = w.ID_WYD
    FOR UPDATE OF CENA;
    
  -- Zmienne pomocnicze
  v_new_price NUMBER;
BEGIN
  -- Otwórz kursor
  OPEN c_books;
  
  -- Pêtla przetwarzaj¹ca ka¿dy rekord z kursora
  LOOP
    FETCH c_books INTO v_id_ksi, v_price, v_publisher;
    
    -- Zakoñczenie pêtli, jeœli nie ma wiêcej rekordów
    EXIT WHEN c_books%NOTFOUND;
    
    -- Jeœli wydawnictwo to "Litera", podnieœ cenê o 10%, w przeciwnym przypadku o 5%
    IF v_publisher = 'Litera' THEN
      v_new_price := v_price * 1.10;  -- 10% wzrost
    ELSE
      v_new_price := v_price * 1.05;  -- 5% wzrost
    END IF;
    
    -- Zaktualizuj cenê ksi¹¿ki przy u¿yciu klauzuli WHERE CURRENT OF
    UPDATE KSIAZKA
    SET CENA = v_new_price
    WHERE CURRENT OF c_books;
  END LOOP;
  
  -- Zamkniêcie kursora
  CLOSE c_books;
  
  COMMIT;  -- Zatwierdzenie zmian
END;

-- Wariant II
DECLARE
  -- Zmienna do przechowywania nowej ceny
  v_new_price NUMBER;
  
  -- Kursor pobieraj¹cy ksi¹¿ki i ich ceny
  CURSOR c_books IS
    SELECT ID_KSI, CENA, WYDAWNICTWO
    FROM KSIAZKA k
    JOIN WYDAWNICTWO w ON k.ID_WYD = w.ID_WYD;
    
BEGIN
  -- Otwórz kursor
  OPEN c_books;
  
  -- Pêtla przetwarzaj¹ca ka¿dy rekord z kursora
  LOOP
    FETCH c_books INTO v_id_ksi, v_price, v_publisher;
    
    -- Zakoñczenie pêtli, jeœli nie ma wiêcej rekordów
    EXIT WHEN c_books%NOTFOUND;
    
    -- Jeœli wydawnictwo to "Litera", podnieœ cenê o 10%, w przeciwnym przypadku o 5%
    IF v_publisher = 'Litera' THEN
      v_new_price := v_price * 1.10;  -- 10% wzrost
    ELSE
      v_new_price := v_price * 1.05;  -- 5% wzrost
    END IF;
    
    -- Zaktualizowanie ceny ksi¹¿ki z u¿yciem klauzuli RETURNING INTO
    UPDATE KSIAZKA
    SET CENA = v_new_price
    WHERE ID_KSI = v_id_ksi
    RETURNING CENA INTO v_new_price;  -- Przechowujemy zaktualizowan¹ cenê w zmiennej

    -- Wyœwietlenie zaktualizowanej ceny
    DBMS_OUTPUT.PUT_LINE('Nowa cena ksi¹¿ki ID ' || v_id_ksi || ' to: ' || v_new_price);
  END LOOP;
  
  -- Zamkniêcie kursora
  CLOSE c_books;
  
  COMMIT;  -- Zatwierdzenie zmian
END;
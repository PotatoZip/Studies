if __name__ == '__main__':
    pass
else:
    def right(text, n):
        print(" " * (n - len(text)) + text)

    def left(text, n):
        print(text + " " * (n - len(text)))

    def center(text, n):
        left_margin = (n - len(text)) // 2
        right_margin = n - left_margin - len(text)
        print(" " * left_margin + text + " " * right_margin)

    print("Moduł 'text' definiuje funkcje center, left, right i służy do:")
    print("Wypisania tekstu wyrównanego do lewej, do prawej lub wycentrowanego.")
    print("Dodatkowo ten moduł zawiera:", dir())
    print()
    
    print("Prezentacja funkcji w tym module:")
    print()
    print("Funkcja 'center':")
    print(center.__doc__)
    print()
    print("Funkcja 'left':")
    print(left.__doc__)
    print()
    print("Funkcja 'right':")
    print(right.__doc__)
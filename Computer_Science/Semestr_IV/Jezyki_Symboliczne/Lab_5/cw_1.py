def solution():
    answer = input("Czy swieci slonce?\n")
    if answer.lower() == "tak":
        print("Co tu robisz?\n")
    elif answer.lower() == "nie":
        print("Pracuj dalej!\n")
    else:
        print("Przepraszam, nie rozumiem.\n")

solution()
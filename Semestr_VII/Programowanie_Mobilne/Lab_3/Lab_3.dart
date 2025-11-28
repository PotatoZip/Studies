import 'package:test/test.dart';

// Zadanie 1
String formatName({
  required String firstName,
  required String lastName,
  bool uppercase = false,
}) {
  if (uppercase) {
    return '${firstName.toUpperCase()} ${lastName.toUpperCase()}';
  } else {
    return '$firstName $lastName';
  }
}

// Zadanie 2
class BankAccount {
  String owner;
  double balance;

  BankAccount(this.owner, this.balance) {
    this.balance = 0;
  }

  void deposit(double amount) {
    if (amount <= 0) {
      print('Kwota wpłaty musi być > 0');
      return;
    }
    balance += amount;
  }

  void withdraw(double amount) {
    if (amount <= 0) {
      print('Kwota wypłaty musi być > 0');
      return;
    }
    if (amount > balance) {
      print('Brak wystarczających środków na koncie');
      return;
    }
    balance -= amount;
  }

  String summary() {
    return 'Konto właściciela: $owner — saldo: ${balance.toStringAsFixed(2)}';
  }
}

// Zadanie 3
List<int> evenSquaresSorted(List<int> numbers) {
  final result = numbers.where((n) => n.isEven).map((n) => n * n).toList();
  result.sort();
  return result;
}

// Zadanie 4
bool isAdult(int age) => age >= 18;

void main() {
  // Zadanie 1
  print(formatName(firstName: "Wiktor", lastName: "Zmiendak"));
  print(formatName(firstName: "Wiktor", lastName: "Zmiendak", uppercase: true));

  // Zadanie 2
  BankAccount account = BankAccount("Wiktor Zmiendak", 0);
  account.deposit(1000);
  account.withdraw(300);
  print(account.summary());

  // Zadanie 3
  List<int> numbers = [1, 2, 3, 4, 5, 6];
  print(evenSquaresSorted(numbers));

  // Zadanie 4
  group("isAdult", () {
    test("returns false for age below 18", () {
      expect(isAdult(17), equals(false));
      expect(isAdult(0), equals(false));
      expect(isAdult(-5), equals(false));
    });

    test("returns true for age 18 or older", () {
      expect(isAdult(18), equals(true));
      expect(isAdult(19), equals(true));
      expect(isAdult(100), equals(true));
    });
  });
}

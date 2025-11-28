import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Lab_4',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Coś trzeba zrobić?'),
        backgroundColor: Colors.blue,
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              'Wiktor',
              style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 6),
            Image.asset('assets/images/peon.png'),
            const SizedBox(height: 16),
            const Text(
              '~Praca Praca',
              style: TextStyle(fontFamily: 'Roboto', fontSize: 30),
            ),
            const SizedBox(height: 24),
            const MyCounter(),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          print('Gotów do pracy!');
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}

class MyCounter extends StatefulWidget {
  const MyCounter({super.key});

  @override
  State<MyCounter> createState() => _MyCounterState();
}

class _MyCounterState extends State<MyCounter> {
  int licznik = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Zebrane drewno: $licznik', style: const TextStyle(fontSize: 20)),
        const SizedBox(height: 8),
        ElevatedButton(
          onPressed: () {
            setState(() {
              licznik++;
            });
          },
          child: const Text('Kliknij mnie!'),
        ),
      ],
    );
  }
}

import 'package:flutter/material.dart';

class SecondScreen extends StatelessWidget {
  final String? name;

  const SecondScreen({super.key, this.name});

  @override
  Widget build(BuildContext context) {
    final greeting = name != null ? 'Cześć, $name!' : 'To jest drugi ekran';

    return Scaffold(
      appBar: AppBar(title: const Text('Drugi ekran')),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(greeting, style: const TextStyle(fontSize: 22)),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Wróć'),
            ),
          ],
        ),
      ),
    );
  }
}

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'firebase_options.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  await FirebaseAuth.instance.signInAnonymously();
  final prefs = await SharedPreferences.getInstance();
  final isDark = prefs.getBool('darkMode') ?? false;
  runApp(MyApp(initialDarkMode: isDark));
}

class MyApp extends StatefulWidget {
  final bool initialDarkMode;
  const MyApp({super.key, this.initialDarkMode = false});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  late bool _isDark;

  @override
  void initState() {
    super.initState();
    _isDark = widget.initialDarkMode;
  }

  Future<void> _setDark(bool v) async {
    setState(() => _isDark = v);
    final p = await SharedPreferences.getInstance();
    await p.setBool('darkMode', v);
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Todo App',
      theme: ThemeData.light(),
      darkTheme: ThemeData.dark(),
      themeMode: _isDark ? ThemeMode.dark : ThemeMode.light,
      home: TodoHome(onToggleDark: _setDark, isDark: _isDark),
    );
  }
}

class TodoHome extends StatefulWidget {
  final ValueChanged<bool> onToggleDark;
  final bool isDark;
  const TodoHome({super.key, required this.onToggleDark, required this.isDark});

  @override
  State<TodoHome> createState() => _TodoHomeState();
}

class _TodoHomeState extends State<TodoHome> {
  final CollectionReference tasksRef = FirebaseFirestore.instance.collection(
    'tasks',
  );

  final TextEditingController _titleController = TextEditingController();

  @override
  void dispose() {
    _titleController.dispose();
    super.dispose();
  }

  Future<void> _showAddDialog() async {
    _titleController.clear();
    final key = GlobalKey<FormState>();
    await showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (c) => Padding(
        padding: EdgeInsets.only(
          bottom: MediaQuery.of(c).viewInsets.bottom,
          left: 16,
          right: 16,
          top: 16,
        ),
        child: Form(
          key: key,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextFormField(
                controller: _titleController,
                decoration: const InputDecoration(labelText: 'Tytuł'),
                validator: (v) =>
                    (v == null || v.trim().isEmpty) ? 'Wpisz tytuł' : null,
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  TextButton(
                    onPressed: () => Navigator.of(c).pop(),
                    child: const Text('Anuluj'),
                  ),
                  ElevatedButton(
                    onPressed: () async {
                      if (!(key.currentState?.validate() ?? false)) return;
                      final title = _titleController.text.trim();
                      await tasksRef.add({
                        'title': title,
                        'createdAt': FieldValue.serverTimestamp(),
                        'date': Timestamp.fromDate(DateTime.now()),
                        'completed': false,
                      });
                      if (mounted) Navigator.of(c).pop();
                    },
                    child: const Text('Dodaj'),
                  ),
                ],
              ),
              const SizedBox(height: 12),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _showEditDialog(DocumentSnapshot doc) async {
    final data = doc.data() as Map<String, dynamic>;
    final editController = TextEditingController(text: data['title'] ?? '');
    final key = GlobalKey<FormState>();
    await showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (c) => Padding(
        padding: EdgeInsets.only(
          bottom: MediaQuery.of(c).viewInsets.bottom,
          left: 16,
          right: 16,
          top: 16,
        ),
        child: Form(
          key: key,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextFormField(
                controller: editController,
                decoration: const InputDecoration(labelText: 'Tytuł'),
                validator: (v) =>
                    (v == null || v.trim().isEmpty) ? 'Wpisz tytuł' : null,
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  TextButton(
                    onPressed: () => Navigator.of(c).pop(),
                    child: const Text('Anuluj'),
                  ),
                  ElevatedButton(
                    onPressed: () async {
                      if (!(key.currentState?.validate() ?? false)) return;
                      final title = editController.text.trim();
                      await doc.reference.update({'title': title});
                      if (mounted) Navigator.of(c).pop();
                    },
                    child: const Text('Zapisz'),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Moje Zadania'),
        centerTitle: true,
        actions: [
          IconButton(
            icon: Icon(widget.isDark ? Icons.dark_mode : Icons.light_mode),
            onPressed: () => widget.onToggleDark(!widget.isDark),
          ),
        ],
      ),
      body: StreamBuilder<QuerySnapshot>(
        stream: tasksRef.orderBy('date', descending: false).snapshots(),
        builder: (context, snap) {
          if (snap.hasError) return Center(child: Text('Błąd: ${snap.error}'));
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final docs = snap.data?.docs ?? [];
          if (docs.isEmpty) return const Center(child: Text('Brak zadań'));
          return ListView.builder(
            padding: const EdgeInsets.all(8),
            itemCount: docs.length,
            itemBuilder: (c, i) {
              final doc = docs[i];
              final data = doc.data() as Map<String, dynamic>;
              final title = data['title'] ?? '';
              return Dismissible(
                key: ValueKey(doc.id),
                direction: DismissDirection.endToStart,
                background: Container(
                  color: Colors.red,
                  alignment: Alignment.centerRight,
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  child: const Icon(Icons.delete, color: Colors.white),
                ),
                confirmDismiss: (dir) async {
                  final should = await showDialog<bool>(
                    context: context,
                    builder: (d) => AlertDialog(
                      title: const Text('Usuń zadanie?'),
                      actions: [
                        TextButton(
                          onPressed: () => Navigator.of(d).pop(false),
                          child: const Text('Anuluj'),
                        ),
                        TextButton(
                          onPressed: () => Navigator.of(d).pop(true),
                          child: const Text('Usuń'),
                        ),
                      ],
                    ),
                  );
                  if (should != true) return false;
                  final removed = data;
                  await doc.reference.delete();
                  if (mounted)
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: const Text('Zadanie usunięte'),
                        action: SnackBarAction(
                          label: 'Cofnij',
                          onPressed: () async => await tasksRef.add(removed),
                        ),
                      ),
                    );
                  return true;
                },
                child: Card(
                  child: ListTile(
                    onTap: () => _showEditDialog(doc),
                    title: Text(title),
                    subtitle: Text(
                      (data['date'] as Timestamp?)?.toDate().toString() ?? '',
                    ),
                    trailing: Checkbox(
                      value: data['completed'] ?? false,
                      onChanged: (v) async {
                        await doc.reference.update({'completed': v ?? false});
                      },
                    ),
                  ),
                ),
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddDialog,
        child: const Icon(Icons.add),
      ),
    );
  }
}

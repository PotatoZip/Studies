import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: const Lab07Home(),
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.indigo),
    );
  }
}

final List<String> obrazki = [
  'https://picsum.photos/id/1015/400/300',
  'https://picsum.photos/id/1025/400/300',
  'https://picsum.photos/id/1035/400/300',
  'https://picsum.photos/id/1045/400/300',
  'https://picsum.photos/id/1055/400/300',
  'https://picsum.photos/id/1065/400/300',
];

final List<Map<String, dynamic>> produkty = [
  {'title': 'Siekiera PRO', 'price:pln': 89.90},
  {'title': 'Piła ręczna', 'price:pln': 59.50},
  {'title': 'Rękawice robocze', 'price:pln': 19.99},
  {'title': 'Okulary ochronne', 'price:pln': 24.90},
  {'title': 'Taczka ogrodowa', 'price:pln': 199.00},
  {'title': 'Miarka stalowa 5m', 'price:pln': 14.99},
  {'title': 'Wkrętarka 12V', 'price:pln': 289.00},
  {'title': 'Zestaw bitów 32el', 'price:pln': 39.99},
  {'title': 'Młotek 500g', 'price:pln': 27.49},
  {'title': 'Nóż segmentowy', 'price:pln': 8.99},
];

String formatPLN(num v) => '${v.toStringAsFixed(2)} zł';

class Lab07Home extends StatefulWidget {
  const Lab07Home({super.key});

  @override
  State<Lab07Home> createState() => _Lab07HomeState();
}

class _Lab07HomeState extends State<Lab07Home> {
  String _title = 'Lab 07 – Listy i układy';

  void _onScroll(bool przewinieto) {
    final newTitle = przewinieto ? 'Przewinięto' : 'Lab 07 – Listy i układy';
    if (newTitle != _title) {
      setState(() => _title = newTitle);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(_title)),
      body: NotificationListener<ScrollNotification>(
        onNotification: (notification) {
          final scrolled = notification.metrics.pixels > 0;
          _onScroll(scrolled);
          return false;
        },
        child: ListView(
          padding: const EdgeInsets.all(12),
          children: [
            Text(
              'Sekcja mieszana (Zadanie 4)',
              style: Theme.of(
                context,
              ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              'Liczba produktów: ${produkty.length}',
              style: const TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 12),
            const Text('Karuzela promocyjna'),
            const SizedBox(height: 8),
            const PromoCarousel(),
            const SizedBox(height: 16),
            const Text('Wszystkie produkty'),
            const SizedBox(height: 8),
            SizedBox(
              height: 420,
              child: const ProductsList(useInternalScroll: true),
            ),
            const SizedBox(height: 24),
            const Text('Mini galeria'),
            const SizedBox(height: 8),
            SizedBox(height: 360, child: const MiniGallery()),

            const SizedBox(height: 32),
            const Divider(),
            Text(
              'Podgląd osobnych zadań',
              style: Theme.of(
                context,
              ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            const Text('Zadanie 1: Karty z produktami'),
            const SizedBox(height: 8),
            SizedBox(
              height: 420,
              child: const ProductsList(useInternalScroll: true),
            ),
            const SizedBox(height: 16),
            const Text('Zadanie 2: Karuzela promocyjna'),
            const SizedBox(height: 8),
            const PromoCarousel(),
            const SizedBox(height: 16),
            const Text('Zadanie 3: Mini galeria w siatce'),
            const SizedBox(height: 8),
            SizedBox(height: 360, child: const MiniGallery()),
          ],
        ),
      ),
    );
  }
}

class ProductsList extends StatelessWidget {
  const ProductsList({super.key, this.useInternalScroll = false});

  final bool useInternalScroll;

  @override
  Widget build(BuildContext context) {
    final listView = ListView.builder(
      padding: const EdgeInsets.all(8),
      itemCount: produkty.length,
      physics: useInternalScroll
          ? const BouncingScrollPhysics()
          : const NeverScrollableScrollPhysics(),
      itemBuilder: (context, index) {
        final p = produkty[index];
        final title = p['title'] as String;
        final price = p['price:pln'] as num;

        return Card(
          elevation: 1,
          child: ListTile(
            leading: const Icon(Icons.shopping_cart_outlined),
            title: Text(title),
            subtitle: const Text('Podtytuł'),
            trailing: Text(formatPLN(price)),
            onTap: () {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text('Wybrano: $title – ${formatPLN(price)}'),
                ),
              );
            },
          ),
        );
      },
    );

    if (useInternalScroll) return listView;

    return ScrollConfiguration(
      behavior: const _NoGlowBehavior(),
      child: listView,
    );
  }
}

class _NoGlowBehavior extends ScrollBehavior {
  const _NoGlowBehavior();
  @override
  Widget buildViewportChrome(
    BuildContext context,
    Widget child,
    AxisDirection axisDirection,
  ) => child;
}

class PromoCarousel extends StatelessWidget {
  const PromoCarousel({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 160,
      child: ListView.separated(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.all(8),
        itemCount: 3,
        separatorBuilder: (_, __) => const SizedBox(width: 12),
        itemBuilder: (context, i) {
          final imgUrl = obrazki[i % obrazki.length];
          return GestureDetector(
            onTap: () {
              ScaffoldMessenger.of(
                context,
              ).showSnackBar(SnackBar(content: Text('Slajd #${i + 1}')));
            },
            child: Container(
              width: 240,
              decoration: BoxDecoration(
                boxShadow: [
                  BoxShadow(
                    blurRadius: 10,
                    spreadRadius: 1,
                    offset: const Offset(0, 6),
                    color: Colors.black.withOpacity(0.15),
                  ),
                ],
                borderRadius: BorderRadius.circular(16),
              ),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(16),
                child: Image.network(
                  imgUrl,
                  fit: BoxFit.cover,
                  loadingBuilder: (c, w, progress) {
                    if (progress == null) return w;
                    return const Center(child: CircularProgressIndicator());
                  },
                  errorBuilder: (c, e, s) => Container(
                    color: Colors.grey.shade300,
                    alignment: Alignment.center,
                    child: const Text('Błąd obrazu'),
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}

class MiniGallery extends StatelessWidget {
  const MiniGallery({super.key});

  @override
  Widget build(BuildContext context) {
    return GridView.builder(
      padding: const EdgeInsets.all(8),
      itemCount: 12,
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 3,
        crossAxisSpacing: 8,
        mainAxisSpacing: 8,
      ),
      itemBuilder: (context, i) {
        final img = obrazki[i % obrazki.length];
        return _GalleryTile(imageUrl: img, index: i);
      },
    );
  }
}

class _GalleryTile extends StatefulWidget {
  const _GalleryTile({required this.imageUrl, required this.index});

  final String imageUrl;
  final int index;

  @override
  State<_GalleryTile> createState() => _GalleryTileState();
}

class _GalleryTileState extends State<_GalleryTile> {
  bool liked = false;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () => ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Kafelek #${widget.index}'))),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(12),
        child: Stack(
          fit: StackFit.expand,
          children: [
            Image.network(
              widget.imageUrl,
              fit: BoxFit.cover,
              loadingBuilder: (c, w, p) {
                if (p == null) return w;
                return const Center(child: CircularProgressIndicator());
              },
              errorBuilder: (c, e, s) => Container(
                color: Colors.grey.shade300,
                alignment: Alignment.center,
                child: const Text('Błąd'),
              ),
            ),
            Positioned(
              right: 6,
              bottom: 6,
              child: StatefulBuilder(
                builder: (context, setLocal) {
                  return Material(
                    color: Colors.black45,
                    borderRadius: BorderRadius.circular(20),
                    child: InkWell(
                      borderRadius: BorderRadius.circular(20),
                      onTap: () {
                        setLocal(() => liked = !liked);
                      },
                      child: Padding(
                        padding: const EdgeInsets.all(6.0),
                        child: Icon(
                          liked ? Icons.favorite : Icons.favorite_border,
                          size: 20,
                          color: liked ? Colors.redAccent : Colors.white,
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

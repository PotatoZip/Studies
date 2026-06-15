import { useMemo, useState } from 'react';
import Card from '../components/ui/Card';

function GaleryPage() {
  const [activeCategory, setActiveCategory] = useState('Wszystkie');
  const [searchTerm, setSearchTerm] = useState('');

  const categories = ['Wszystkie', 'Drogi', 'Oświetlenie', 'Zieleń miejska'];

  const galleryCards = [
    {
      id: 1,
      category: 'Drogi',
      title: 'Naprawa nawierzchni',
      location: 'ul. Marszałkowska 12, Warszawa',
      date: '12.03.2024',
      description:
        'Zgłoszenie dotyczyło głębokich ubytków utrudniających przejazd. Służby miejskie dokonały pełnej wymiany warstwy ścieralnej na odcinku 50 metrów.',
      before:
        'https://lh3.googleusercontent.com/aida-public/AB6AXuB-MjLoAJPWK5WxenMK3dvGOBgHBbGe7_evWWuTFcCIZItEWP5PGngy2fb0B-WpPWq_rskqv8FnNEciIq8Z1R7NzIVCIDZsx3OecvESrwhVKITlSo7NnihlCi6t28z2UevZMTyJzYHCC9e6rb38IguyI8h6Ad0gTrGPv4u-3j4EDBERHzEbNljxeyQJO9uKeahbB6hWPOHUn3thJDDGnKf-66uA5q_8S-ZkVAuSSOP9yyUdy8O6AOpLP7uubYbgfzx4oYBur3Zxs60',
      after:
        'https://lh3.googleusercontent.com/aida-public/AB6AXuBYKHcjFVlrplQygElHD-_Q3Q9PEiyovwkEZ4Jf7FgzrH5PHMaOWJFbwJISLXFXT7nzBWr4Woo_ovKu0u0XbiuyJn-YiRM8sE6JtW_2_zu5dZB6tPOq6gQWDWaVgfcendC9M9PuG2GD7ZHqyBvy7HoFuxhSt3Jk9WNs96g_UC8TQ5SX1ul_O1R2Rem8prEBRhfvdyFpSJK3KgSbd_MV3SIRylG2eg4n6v2Z7v9u7pN0nE0TGL1WQ0QPdGVMykXroebYKBJNeBOUl50'
    },
    {
      id: 2,
      category: 'Oświetlenie',
      title: 'Nowe oświetlenie',
      location: 'Park Kultury, Sektor B',
      date: '28.02.2024',
      description:
        'Wymiana starych opraw sodowych na nowoczesne oświetlenie LED zwiększyło bezpieczeństwo mieszkańców korzystających z parku po zmroku.',
      before:
        'https://lh3.googleusercontent.com/aida-public/AB6AXuAj2lVfZMrfjzqKqx8PcYFKncxGYbleBequFS8qO1CZjldIx1qMHRZIWixHl5gupN8lqwY2Tuam5QG14qeB4SMx187OMP89sKrQe8LRPTh3rZ1Q6fjQHRx-Qg_TfM9R5WxAUqBEd8FSJ8IpPbNEovh9Av632DO-mdBI9Qc5ZZ30MJ-CJltxf5Rrs7e3ONSzg4gdiB3aEXW1gLnRmqMkQnupPcWzaEv32cYvPIIOxASDcnsw-dkTOzVjSWyVi3e2rdu7BvJn6x9aWgo',
      after:
        'https://lh3.googleusercontent.com/aida-public/AB6AXuC_oMEroUrz7n4fDwb0yKpJ0ruCq-rxOVyeD7D0GNYPljlShn0frkPPQL28kENs9qpgyj-8owNpNaN1n33rIYcmRwW5YpiFHSVYiTnGGZxrjvXRfV5Vh1sgNBUsEJgrF0q-sh2oUa-jN3uVuY7_1Um8F2jEm7K86CfOBZPlSw-i1Ui_ZMoUWUq87JoNk4WpOABZx_86JZPgm4mJcPtkx1yQ-kn85aAnMdCnGkZs5N0pXq3n98DXfZ5TwU74Sjem_0_BjQ7q-y8vyEA'
    },
    {
      id: 3,
      category: 'Zieleń miejska',
      title: 'Renowacja skweru',
      location: 'Skwer Kościuszki, Centrum',
      date: '15.03.2024',
      description:
        'Zniszczone ławki i kosze na śmieci zostały zastąpione nowymi elementami małej architektury, poprawiając estetykę centralnego skweru.',
      before:
        'https://lh3.googleusercontent.com/aida-public/AB6AXuBC0sOiI9zRr34r0pJEdgXrtfMXCF0kE7OshCezaUfI-wJnGnttWwnx4G1YdUpvjmDecQs_QYEjdUS8X0W3T0vhRy1o5lE3dPAgJjofeQE3qCbMcGHMIVJEISS1CdXAWxmbC6H3hSK3mt0xPVqswxCJaKnakD4wwdotpcInw2OdoCawWoi9XC2LMNiBKGpNuiEbxMZ6ma5h8YQDriYj9uFKgbwRK8aJmOl6WfsT8-MBWdUGvCRA3ja4qvuAHBduqdOmY6nBufJaVQs',
      after:
        'https://lh3.googleusercontent.com/aida-public/AB6AXuAjuxXizWsb3APwE18PC9iN0YzCizH4tbDj4Kewcr4RVLHLXkcUHhUdF4STXqDhf85IF7ABDCvK0LtosPkE8huvxaPF7_cyCjMfu2YmDvpJmz2rNQAOYh4keriZ7FFkcWNdzDvbDU_Htxbzo-pcJJStJI42_iuAqcwVScdq07Koqe3WmhpDFPHl_V9ZLWNQQ1GQtMBMTb0G3OwQfNgsen-jULt-zxJ7uZ3dzRC8WzpE6BDrCEgV3MxYbXQUHYIutTtvoscKKF72Aeg'
    },
    {
      id: 4,
      category: 'Zieleń miejska',
      title: 'Rewitalizacja przejścia',
      location: 'Przejście podziemne, ul. Główna',
      date: '10.03.2024',
      description:
        'Nieestetyczne bazgroły zostały zastąpione przez mural wykonany przez lokalnych artystów, co nadało miejscu unikalny charakter.',
      before:
        'https://lh3.googleusercontent.com/aida-public/AB6AXuDrvDQKFJ_kS9Y5NpT_zZe32exhhLdgosVKxih0C9ZDXneyJAqvRTQ8Ok_HOHchbegzhn2tTbcjoftPuWfBhEsDDC-Gx0A-4Z3QiPxKvwIH19Vnm5WL_VybyiPhPOVXj9QGNPxqAihRjLLuaxKp-QYenrvNb9Bzj6y6KBVCm5jwyann0ggtAMTzXP-yVk6CWGoF665xJUkdgkoGTmD7HtK7RhtM6cIUwJBAFYJei2t6QGbmnz51iq2BEqnuMB6NBiyqcgKxwXYclyI',
      after:
        'https://lh3.googleusercontent.com/aida-public/AB6AXuBfNGmSE0SKKok34-4mTlLiLbskh4z1KndFjNUASkJJuhk9mVo6NRItnzp5pkAXEv3WaKX6JKg6diCJSbYSO3bP6_qNl7Z2k3YZZ7KUSbc75A6j_SYzuGNVxZlRcKwERtcWNZVeTXDd1ZgRfG1W-BTG-DXf6-_xDpcRJaaoy0DlaywgZX5uux99y13FQHt5WM1USZtHpF6lH-b8PzBfwS8o26nvOlJ4EGBLMHPBNyXrczWbEN12xqa9b7_k4uqs7kRTika6apd75H4'
    }
  ];

  const filteredCards = useMemo(() => {
    return galleryCards.filter((card) => {
      const matchesCategory =
        activeCategory === 'Wszystkie' || card.category === activeCategory;
      const query = searchTerm.trim().toLowerCase();
      const matchesSearch =
        query.length === 0 ||
        card.location.toLowerCase().includes(query) ||
        card.title.toLowerCase().includes(query) ||
        card.description.toLowerCase().includes(query);
      return matchesCategory && matchesSearch;
    });
  }, [activeCategory, searchTerm, galleryCards]);

  return (
    <div className="w-full max-w-[1180px] mx-auto px-4 py-8">
      <section className="text-center py-12">
        <h1 className="text-4xl font-headline font-extrabold text-primary mb-4">Galeria Zmian</h1>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto">
          Każde zgłoszenie to realna zmiana w naszej przestrzeni. Zobacz, jak wspólnie naprawiamy
          nasze miasto i dbamy o wspólne dobro.
        </p>
      </section>

      <section className="flex flex-col md:flex-row justify-between items-center bg-white p-4 rounded-2xl shadow-sm border border-slate-200 mb-8 gap-4">
        <div className="flex flex-wrap gap-2">
          {categories.map((category) => (
            <button
              key={category}
              type="button"
              className={`px-4 py-2 rounded-full font-bold text-sm transition-colors ${
                category === activeCategory
                  ? 'bg-primary text-white'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
              onClick={() => setActiveCategory(category)}
            >
              {category}
            </button>
          ))}
        </div>

        <div className="relative w-full md:w-auto min-w-[250px]">
          <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">search</span>
          <input
            type="text"
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
            placeholder="Szukaj lokalizacji..."
            aria-label="Szukaj lokalizacji"
            className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:border-primary focus:ring-1 focus:ring-primary outline-none"
          />
        </div>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {filteredCards.map((card) => (
          <Card className="flex flex-col h-full" key={card.id}>
            <div className="flex h-48 relative border-b border-slate-200">
              <div className="w-1/2 relative h-full">
                <span className="absolute top-2 left-2 bg-black/60 text-white text-[10px] font-bold px-2 py-1 rounded">Przed</span>
                <img src={card.before} alt={`Przed: ${card.title}`} className="w-full h-full object-cover" />
              </div>
              <div className="w-1/2 relative h-full">
                <span className="absolute top-2 left-2 bg-green-600/90 text-white text-[10px] font-bold px-2 py-1 rounded">Po</span>
                <img src={card.after} alt={`Po: ${card.title}`} className="w-full h-full object-cover" />
              </div>
            </div>
            <div className="p-6 flex flex-col flex-grow">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold text-slate-800">{card.title}</h3>
                  <div className="flex items-center text-slate-500 text-sm mt-1 gap-1">
                    <span className="material-symbols-outlined text-sm">location_on</span>
                    <span>{card.location}</span>
                  </div>
                </div>
                <div className="flex flex-col items-end">
                  <span className="bg-green-100 text-green-800 text-[10px] font-bold px-2 py-1 rounded uppercase tracking-wider mb-1">Ukończono</span>
                  <span className="text-xs text-slate-500">{card.date}</span>
                </div>
              </div>
              <p className="text-slate-600 text-sm leading-relaxed">{card.description}</p>
            </div>
          </Card>
        ))}
      </section>
    </div>
  );
}

export default GaleryPage;

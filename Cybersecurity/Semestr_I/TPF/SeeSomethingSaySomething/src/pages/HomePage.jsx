import { useRef } from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/ui/Button';

function HomePage() {
  const galleryRef = useRef(null);

  const scrollGallery = (direction) => {
    if (!galleryRef.current) return;
    const scrollAmount = window.innerWidth < 768 ? 320 : 500;
    const gap = 32;
    galleryRef.current.scrollBy({
      left: direction === 'left' ? -(scrollAmount + gap) : scrollAmount + gap,
      behavior: 'smooth'
    });
  };

  return (
    <div className="bg-background font-body text-on-surface antialiased">
      <style>{`
        .text-gradient {
          background: linear-gradient(135deg, #001d44 0%, #00326b 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        .hide-scrollbar::-webkit-scrollbar {
          display: none;
        }
        .hide-scrollbar {
          -ms-overflow-style: none;
          scrollbar-width: none;
        }
        .material-symbols-fill {
          font-variation-settings: 'FILL' 1;
        }
      `}</style>

     
      <section className="relative flex items-center px-6 lg:px-12 pt-4 pb-12 overflow-hidden lg:pt-8 lg:pb-24">
        <div className="grid lg:grid-cols-2 gap-12 items-center w-full max-w-[1440px] mx-auto">
          <div className="z-10 space-y-8">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-secondary-fixed text-on-secondary-fixed text-xs font-bold uppercase tracking-wider">
              <span className="material-symbols-outlined material-symbols-fill text-sm">
                bolt
              </span>
              Najprostszy sposób na naprawę okolicy
            </div>
            <h1 className="font-headline text-5xl md:text-7xl font-extrabold text-on-surface leading-[1.1] tracking-tight">
              Zmień swoje miasto<br />
              <span className="text-gradient">jednym kliknięciem.</span>
            </h1>
            <p className="text-on-surface-variant text-lg md:text-xl max-w-xl leading-relaxed">
              Widzisz problem? Zrób zdjęcie. See Something? Say Something!
              zajmie się resztą, łącząc Cię bezpośrednio z odpowiednimi służbami mieście.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <Link to="/send-request">
                <Button className="px-10 py-4 text-lg shadow-xl shadow-primary/20 hover:shadow-2xl group">
                  <span className="material-symbols-outlined group-hover:scale-110 transition-transform">
                    add_circle
                  </span>
                  Zgłoś usterkę
                </Button>
              </Link>
            </div>
          </div>
          <div className="relative lg:block hidden">
            <div className="relative rounded-[2.5rem] overflow-hidden shadow-2xl border-8 border-white">
              <img
                alt="Modern clean city square"
                className="w-full h-[600px] object-cover"
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuBq9VmdVJxQ9lgUKgCAJ486t17fPMD3RKU2SYMO6TkVUrTAf3rJqcSwAfO9WuPy6SQp7XTGpz0fx8BL5p7B10EW28xjP8Qk2w1Csbnz1MwJHIGF_iexJQS1PEbGDqpxOUv9EaqLLgia4EDoGvf-i96P1R5ijx-AbfbyDTbMKsbPmwTBmct4JfjhwTtoCixM-_lbncMHOf7EVBqILKPVwmtgIqFBHLfRFJIW_ZRSTg044kS3q1feS4B8OQhBgmPLiTYXRsQZ9EW-Dv4"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />
            </div>
         
            <div className="absolute -bottom-6 -left-6 bg-white p-6 rounded-3xl shadow-2xl border border-outline-variant/10 flex items-center gap-4 animate-bounce">
              <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center text-green-700">
                <span className="material-symbols-outlined material-symbols-fill">verified</span>
              </div>
              <div>
                <p className="text-xs font-bold text-slate-500 uppercase m-0">
                  Ostatnio naprawiono
                </p>
                <p className="font-headline font-bold text-on-surface m-0">
                  Naprawa oświetlenia: 100%
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

   
      <section className="bg-white py-24 px-6 lg:px-12 border-y border-outline-variant/10">
        <div className="max-w-[1440px] mx-auto grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
          <div className="space-y-3">
            <p className="text-6xl font-black font-headline text-primary tracking-tighter m-0">
              15,420
            </p>
            <p className="text-on-surface-variant font-semibold text-sm uppercase tracking-wider m-0">
              Wszystkich zgłoszeń
            </p>
          </div>
          <div className="space-y-3 md:border-x border-outline-variant/20 px-4">
            <p className="text-6xl font-black font-headline text-primary tracking-tighter m-0">
              92%
            </p>
            <p className="text-on-surface-variant font-semibold text-sm uppercase tracking-wider m-0">
              Zrealizowanych spraw
            </p>
          </div>
          <div className="space-y-3">
            <p className="text-6xl font-black font-headline text-secondary tracking-tighter m-0">
              48h
            </p>
            <p className="text-on-surface-variant font-semibold text-sm uppercase tracking-wider m-0">
              Średni czas reakcji
            </p>
          </div>
        </div>
      </section>

      
      <section className="py-32 px-6 lg:px-12 max-w-[1440px] mx-auto">
        <div className="mb-20 text-center max-w-2xl mx-auto">
          <h2 className="font-headline text-4xl font-extrabold mb-6">
            Wystarczy parę sekund
          </h2>
          <p className="text-on-surface-variant text-lg">
            Zaprojektowaliśmy ten proces tak, aby był maksymalnie prosty. Ty zgłaszasz, my działamy.
          </p>
        </div>
        <div className="grid md:grid-cols-3 gap-12">
          <div className="text-center space-y-6">
            <div className="w-20 h-20 rounded-full bg-primary/5 mx-auto flex items-center justify-center">
              <span className="material-symbols-outlined text-4xl text-primary">photo_camera</span>
            </div>
            <h3 className="font-headline font-bold text-2xl m-0">Zrób zdjęcie</h3>
            <p className="text-on-surface-variant m-0">
              Widzisz usterkę? Wyjmij telefon i uwiecznij ją.
            </p>
          </div>
          <div className="text-center space-y-6">
            <div className="w-20 h-20 rounded-full bg-primary/5 mx-auto flex items-center justify-center relative">
              <span className="material-symbols-outlined text-4xl text-primary">send</span>
              <div className="absolute -right-4 top-1/2 -translate-y-1/2 hidden md:block">
                <span className="material-symbols-outlined text-outline-variant">trending_flat</span>
              </div>
            </div>
            <h3 className="font-headline font-bold text-2xl m-0">Wyślij zgłoszenie</h3>
            <p className="text-on-surface-variant m-0">
              Jednym kliknięciem prześlij informację do systemu.
            </p>
          </div>
          <div className="text-center space-y-6">
            <div className="w-20 h-20 rounded-full bg-secondary/10 mx-auto flex items-center justify-center">
              <span className="material-symbols-outlined text-4xl text-secondary">task_alt</span>
            </div>
            <h3 className="font-headline font-bold text-2xl m-0">Gotowe!</h3>
            <p className="text-on-surface-variant m-0">
              Służby miejskie są już w drodze do Twojej lokalizacji.
            </p>
          </div>
        </div>
      </section>

     
      <section id="gallery" className="bg-surface-container-low py-32 overflow-hidden">
        <div className="max-w-[1440px] mx-auto px-6 lg:px-12 mb-16 flex flex-col md:flex-row justify-between items-end gap-6">
          <div className="max-w-xl">
            <h2 className="font-headline text-4xl font-extrabold mb-4">Galeria Zmian</h2>
            <p className="text-on-surface-variant text-lg m-0">
              Zobacz konkretne efekty zgłoszeń naszych użytkowników. Twoja okolica może wyglądać tak samo.
            </p>
          </div>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => scrollGallery('left')}
              className="w-12 h-12 rounded-full border border-outline-variant flex items-center justify-center hover:bg-white transition-all outline-none"
            >
              <span className="material-symbols-outlined">chevron_left</span>
            </button>
            <button
              type="button"
              onClick={() => scrollGallery('right')}
              className="w-12 h-12 rounded-full border border-outline-variant flex items-center justify-center hover:bg-white transition-all outline-none"
            >
              <span className="material-symbols-outlined">chevron_right</span>
            </button>
          </div>
        </div>

        <div
          ref={galleryRef}
          className="flex gap-8 overflow-x-auto px-6 lg:px-12 hide-scrollbar pb-12 max-w-[1440px] mx-auto"
        >
     
          <div className="min-w-[320px] md:min-w-[500px] bg-white rounded-3xl overflow-hidden shadow-sm flex flex-col group border border-outline-variant/5 transition-all hover:shadow-xl">
            <div className="grid grid-cols-2 h-64">
              <div className="relative overflow-hidden">
                <img alt="Before" className="w-full h-full object-cover grayscale opacity-80" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAe00HecS-VXz3wBUiG7Jx6xZiKvN1LHOWwo1SgYq-IGjcwC5jRUgEQvdoYTi5mFcVPwsYJV51wXOF_WHsbSG-oiV7lULZ-TAs3_TvHkAo6XMmVA3aH1dvjEyy-0tXsmpntmdGXuPCVGMkskqBvsvAli2SjeIDzllgrkF_FGlRazBHT1f-LNhBNM8Oms_N9tClbfAranaHgpwBJOycl29EvIb1w5sYZ0ULtDwrZe1mm46cHJSsFMsGN26Rhx6OHd5PXWDQabUMQcjU" />
                <div className="absolute bottom-2 left-2 bg-black/50 backdrop-blur-md text-white text-[10px] px-2 py-0.5 rounded-full uppercase font-bold tracking-widest">Przed</div>
              </div>
              <div className="relative overflow-hidden">
                <img alt="After" className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAe00HecS-VXz3wBUiG7Jx6xZiKvN1LHOWwo1SgYq-IGjcwC5jRUgEQvdoYTi5mFcVPwsYJV51wXOF_WHsbSG-oiV7lULZ-TAs3_TvHkAo6XMmVA3aH1dvjEyy-0tXsmpntmdGXuPCVGMkskqBvsvAli2SjeIDzllgrkF_FGlRazBHT1f-LNhBNM8Oms_N9tClbfAranaHgpwBJOycl29EvIb1w5sYZ0ULtDwrZe1mm46cHJSsFMsGN26Rhx6OHd5PXWDQabUMQcjU" />
                <div className="absolute bottom-2 left-2 bg-primary/80 backdrop-blur-md text-white text-[10px] px-2 py-0.5 rounded-full uppercase font-bold tracking-widest">Po</div>
              </div>
            </div>
            <div className="p-6">
              <h4 className="font-headline font-bold text-xl mb-1 m-0">Naprawa nawierzchni</h4>
              <p className="text-on-surface-variant text-sm flex items-center gap-1 m-0"><span className="material-symbols-outlined text-base">location_on</span>ul. Warszawska 12 • 3 dni temu</p>
            </div>
          </div>

          <div className="min-w-[320px] md:min-w-[500px] bg-white rounded-3xl overflow-hidden shadow-sm flex flex-col group border border-outline-variant/5 transition-all hover:shadow-xl">
            <div className="grid grid-cols-2 h-64">
              <div className="relative overflow-hidden border-r border-white/20">
                <img alt="Before" className="w-full h-full object-cover grayscale opacity-80" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCcD7ZpKOnlZBZsJfiUfJi-yrGvVrtPwfOLPaoQL1L1ZwZT9Dcb3LMHDbDqvFfM79s-HLZsCyhT_s6mRpQLTdDBu3DHTf_dvCwfX4xeoild4wtQbtwYyuAvc178nrKAwXI2CDEEUWVEMdjqH_FKuZ12g9G_SCiH1gIDzOuzeOiC_9T7YGY9s0RInUWYS4-9Uw9UJ_22akaNdgmYRt74ngZBcQ6L-MNGXXaVZ6xPytLwd-nTxr_I-2fA4V6m0rj_PHXYxG0PSojO19M" />
                <div className="absolute bottom-2 left-2 bg-black/50 backdrop-blur-md text-white text-[10px] px-2 py-0.5 rounded-full uppercase font-bold tracking-widest">Przed</div>
              </div>
              <div className="relative overflow-hidden">
                <img alt="After" className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCcD7ZpKOnlZBZsJfiUfJi-yrGvVrtPwfOLPaoQL1L1ZwZT9Dcb3LMHDbDqvFfM79s-HLZsCyhT_s6mRpQLTdDBu3DHTf_dvCwfX4xeoild4wtQbtwYyuAvc178nrKAwXI2CDEEUWVEMdjqH_FKuZ12g9G_SCiH1gIDzOuzeOiC_9T7YGY9s0RInUWYS4-9Uw9UJ_22akaNdgmYRt74ngZBcQ6L-MNGXXaVZ6xPytLwd-nTxr_I-2fA4V6m0rj_PHXYxG0PSojO19M" />
                <div className="absolute bottom-2 left-2 bg-primary/80 backdrop-blur-md text-white text-[10px] px-2 py-0.5 rounded-full uppercase font-bold tracking-widest">Po</div>
              </div>
            </div>
            <div className="p-6">
              <h4 className="font-headline font-bold text-xl mb-1 m-0">Oświetlenie parku</h4>
              <p className="text-on-surface-variant text-sm flex items-center gap-1 m-0"><span className="material-symbols-outlined text-base">location_on</span>Park Śródmiejski • 12 godz. temu</p>
            </div>
          </div>

          <div className="min-w-[320px] md:min-w-[500px] bg-white rounded-3xl overflow-hidden shadow-sm flex flex-col group border border-outline-variant/5 transition-all hover:shadow-xl">
            <div className="grid grid-cols-2 h-64">
              <div className="relative overflow-hidden">
                <img alt="Before" className="w-full h-full object-cover grayscale opacity-80" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBMtBsu3v1kIGHn16ztvc0cQtaLae7cKV2wpfggUnXuYe183KqybSfRzfpG3Led249iDZvHfmh6MVADDo79-m2_DcoWUXQghFMEcuk1fZEq4Q8Zs1XLhEfZhLgmXDbCFgtYIXX0gNw6RpHNFwBhafUg3vqxUlS_YaYnQg-db_WaJPiCC7FGvuA25K__X01hTyxCsvaa1h4_SOgPqlj0uZz0LH6h4k6lt4xOu779QMMlHcDBEApgBJsJ-JQk0zj_2HA1JUi_fERD6Hw" />
                <div className="absolute bottom-2 left-2 bg-black/50 backdrop-blur-md text-white text-[10px] px-2 py-0.5 rounded-full uppercase font-bold tracking-widest">Przed</div>
              </div>
              <div className="relative overflow-hidden">
                <img alt="After" className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBMtBsu3v1kIGHn16ztvc0cQtaLae7cKV2wpfggUnXuYe183KqybSfRzfpG3Led249iDZvHfmh6MVADDo79-m2_DcoWUXQghFMEcuk1fZEq4Q8Zs1XLhEfZhLgmXDbCFgtYIXX0gNw6RpHNFwBhafUg3vqxUlS_YaYnQg-db_WaJPiCC7FGvuA25K__X01hTyxCsvaa1h4_SOgPqlj0uZz0LH6h4k6lt4xOu779QMMlHcDBEApgBJsJ-JQk0zj_2HA1JUi_fERD6Hw" />
                <div className="absolute bottom-2 left-2 bg-primary/80 backdrop-blur-md text-white text-[10px] px-2 py-0.5 rounded-full uppercase font-bold tracking-widest">Po</div>
              </div>
            </div>
            <div className="p-6">
              <h4 className="font-headline font-bold text-xl mb-1 m-0">Renowacja schodów</h4>
              <p className="text-on-surface-variant text-sm flex items-center gap-1 m-0"><span className="material-symbols-outlined text-base">location_on</span>Stare Miasto • 1 tydzień temu</p>
            </div>
          </div>
        </div>
      </section>

      
      <Link
        to="/send-request"
        className="md:hidden fixed bottom-6 right-6 w-16 h-16 bg-primary text-on-primary rounded-full shadow-2xl flex items-center justify-center z-[60] active:scale-95 transition-transform"
      >
        <span className="material-symbols-outlined material-symbols-fill text-3xl">add</span>
      </Link>
    </div>
  );
}

export default HomePage;

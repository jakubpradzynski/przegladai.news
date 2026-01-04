import React from 'react';
import { ShieldCheck, Zap, ArrowDown } from 'lucide-react';

interface HeroProps {
  onSubscribeClick: () => void;
}

export const Hero: React.FC<HeroProps> = ({ onSubscribeClick }) => {
  const scrollToArchive = (e: React.MouseEvent) => {
    e.preventDefault();
    const element = document.getElementById('archive');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="relative overflow-hidden min-h-[calc(100vh-4rem)] flex items-center py-20">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-8 items-center">
          
          {/* Left Column: Content */}
          <div className="max-w-2xl">
            
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-gray-900 tracking-tight leading-tight mb-6">
              Przegląd<span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">AI</span>
            </h1>
            
            <p className="text-lg sm:text-xl text-gray-600 mb-8 leading-relaxed">
              Otrzymuj wartościowe, przefiltrowane materiały związane z AI - nowości, praktyki, narzędzia, finanse i wiele innych. Ja śledzę kilkadziesiąt źródeł (blogów firmowych, osobistych, newsletterów). Ty nie musisz. Możesz śledzić samą esencję i być na bieżąco z tym co dzieje się w świecie AI.
            </p>

            <div className="mb-10">
              <div className="flex flex-col sm:flex-row gap-3 mb-4">
                <button
                  onClick={onSubscribeClick}
                  className="px-8 py-4 rounded-xl font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-all shadow-lg hover:shadow-blue-500/25 flex items-center justify-center text-lg w-full sm:w-auto active:scale-95"
                >
                  Kliknij tutaj, aby zasubskrybować
                </button>
              </div>
              
              <button
                onClick={scrollToArchive}
                className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors pl-1 group bg-transparent border-none cursor-pointer"
              >
                Zobacz poprzednie wydania
                <ArrowDown size={16} className="ml-1 transition-transform group-hover:translate-y-1" />
              </button>
            </div>

            <div className="space-y-4 text-sm text-gray-500 bg-gray-50 p-5 rounded-xl border border-gray-100">
              <div className="flex items-start">
                <Zap className="w-5 h-5 text-amber-500 mr-3 flex-shrink-0 mt-0.5" />
                <p>
                  <strong className="text-gray-900 block mb-1">Częstotliwość:</strong> 
                  Celuję w jeden mail tygodniowo, ale nie jest to sztywna reguła. Chcę przede wszystkim zachować jakość newslettera.
                </p>
              </div>
              <div className="flex items-start">
                <ShieldCheck className="w-5 h-5 text-emerald-500 mr-3 flex-shrink-0 mt-0.5" />
                <p>
                  <strong className="text-gray-900 block mb-1">Perspektywa IT:</strong>
                  Newsletter jest pisany przez Engineering Managera, więc najlepiej wpisuje się w branże IT, ale każdy znajdzie tu konkretną wiedzę bez szumu informacyjnego.
                </p>
              </div>
            </div>
          </div>

          {/* Right Column: Visual/Decoration */}
          <div className="hidden lg:flex justify-center items-center relative">
            <div className="absolute top-0 right-0 -mr-20 -mt-20 w-72 h-72 bg-blue-100 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob"></div>
            <div className="absolute top-0 right-20 -mr-20 -mt-20 w-72 h-72 bg-indigo-100 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob animation-delay-2000"></div>
            <div className="absolute -bottom-8 left-20 w-72 h-72 bg-purple-100 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob animation-delay-4000"></div>
            
            <div className="relative bg-white/60 backdrop-blur-xl border border-white/50 p-8 rounded-3xl shadow-2xl max-w-sm transform rotate-3 hover:rotate-0 transition-all duration-500">
              <div className="flex items-center space-x-4 mb-6">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
                  <Zap size={24} />
                </div>
                <div>
                  <div className="h-2.5 w-24 bg-gray-200 rounded-full mb-2"></div>
                  <div className="h-2 w-16 bg-gray-100 rounded-full"></div>
                </div>
              </div>
              <div className="space-y-3">
                <div className="h-2 w-full bg-gray-100 rounded-full"></div>
                <div className="h-2 w-5/6 bg-gray-100 rounded-full"></div>
                <div className="h-2 w-4/6 bg-gray-100 rounded-full"></div>
              </div>
              <div className="mt-6 pt-6 border-t border-gray-100 flex justify-between items-center">
                <div className="h-8 w-20 bg-blue-50 rounded-lg flex items-center justify-center text-blue-600 text-xs font-bold">
                  AI NEWS
                </div>
                <div className="text-xs text-gray-400">10 min czytania</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
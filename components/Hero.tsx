import React from 'react';
import { Zap, ArrowDown, Mail, Sparkles, CheckCircle2 } from 'lucide-react';

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
              Bądź na bieżąco z AI.<br/>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Wyłapuj rynkowe okazje.</span>
            </h1>
            
            <p className="text-lg sm:text-xl text-gray-600 mb-6 leading-relaxed">
              Darmowy newsletter dla <strong>Managerów, Developerów i Przedsiębiorców (nie tylko) w branży IT</strong>. Nie pozwól, by rynek Cię wyprzedził. Co tydzień otrzymasz wyselekcjonowaną przez człowieka dawkę wiedzy i inspiracji. Wystarczy <strong>10 minut czytania</strong>, by poznać najnowsze narzędzia, zrozumieć trendy i dostrzec szanse na rozwój Twojego biznesu oraz kariery.
            </p>

            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-100 rounded-xl p-4 mb-8 flex items-start gap-3">
              <span className="text-2xl flex-shrink-0" role="img" aria-label="gift">🎁</span>
              <div>
                <strong className="text-gray-900 block mb-1">Bonus dla czytelników:</strong>
                <p className="text-gray-700 text-sm">Zapisz się do newslettera i odbierz dostęp do konta <strong>Todoist Pro na 2 miesiące za darmo!</strong> Link otrzymasz w następnym wydaniu newslettera.</p>
              </div>
            </div>

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
          </div>

          {/* Right Column: Visual/Decoration */}
          <div className="hidden lg:flex justify-center items-center relative min-h-[500px] w-full">
            {/* Background Blobs */}
            <div className="absolute top-1/2 right-1/4 -translate-y-1/2 translate-x-1/4 w-72 h-72 bg-blue-400/30 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob"></div>
            <div className="absolute top-1/2 right-1/2 -translate-y-1/2 translate-x-1/2 w-72 h-72 bg-indigo-400/30 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob" style={{ animationDelay: '2s' }}></div>
            <div className="absolute top-1/2 right-1/3 -translate-y-1/2 w-72 h-72 bg-purple-400/30 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob" style={{ animationDelay: '4s' }}></div>
            
            {/* Main Floating Container */}
            <div className="relative w-full max-w-sm animate-float">
              
              {/* Back Card (Decoration) */}
              <div className="absolute inset-0 bg-gradient-to-br from-blue-100 to-indigo-100 transform rotate-6 rounded-3xl shadow-lg opacity-70 transition-transform duration-500 hover:rotate-12"></div>
              
              {/* Front Card (Newsletter Mockup) */}
              <div 
                className="relative bg-white/95 backdrop-blur-xl border border-white p-8 rounded-3xl shadow-2xl transform -rotate-2 hover:rotate-0 hover:scale-105 transition-all duration-500 flex flex-col gap-6 cursor-pointer group"
                onClick={onSubscribeClick}
              >
                {/* Header */}
                <div className="flex items-center justify-between pb-4 border-b border-gray-100">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center text-white shadow-lg shadow-blue-500/30 group-hover:scale-110 transition-transform">
                      <Mail size={24} />
                    </div>
                    <div>
                      <div className="text-sm font-bold text-gray-900">Najnowsze wydanie</div>
                      <div className="text-xs text-gray-500">PrzeglądAI Newsletter</div>
                    </div>
                  </div>
                </div>
                
                {/* Body Mockup */}
                <div className="space-y-4">
                  <div className="h-4 w-3/4 bg-gray-200 rounded-full"></div>
                  <div className="space-y-2">
                    <div className="h-2 w-full bg-gray-100 rounded-full"></div>
                    <div className="h-2 w-5/6 bg-gray-100 rounded-full"></div>
                    <div className="h-2 w-4/6 bg-gray-100 rounded-full"></div>
                  </div>
                </div>

                {/* Features List */}
                <div className="bg-gray-50/80 rounded-2xl p-4 space-y-3 border border-gray-100">
                  <div className="flex items-start gap-3">
                    <CheckCircle2 size={18} className="text-blue-500 flex-shrink-0 mt-0.5" />
                    <span className="text-sm text-gray-700 font-medium">Tylko 10 minut czytania tygodniowo</span>
                  </div>
                  <div className="flex items-start gap-3">
                    <CheckCircle2 size={18} className="text-blue-500 flex-shrink-0 mt-0.5" />
                    <span className="text-sm text-gray-700 font-medium">Ludzka selekcja treści</span>
                  </div>
                  <div className="flex items-start gap-3">
                    <CheckCircle2 size={18} className="text-blue-500 flex-shrink-0 mt-0.5" />
                    <span className="text-sm text-gray-700 font-medium">Nowości, technologie, inspiracje</span>
                  </div>
                </div>

                {/* Call to action text inside the card */}
                <div className="pt-2 text-center">
                  <div className="inline-flex items-center justify-center gap-2 px-6 py-2.5 bg-blue-50 text-blue-700 font-semibold text-sm rounded-xl group-hover:bg-blue-600 group-hover:text-white transition-colors w-full">
                    Chcę to czytać! <Sparkles size={16} />
                  </div>
                </div>
              </div>

              {/* Floating notification badges */}
              <div className="absolute -top-6 -right-8 bg-white px-4 py-3 rounded-2xl shadow-xl border border-gray-100 animate-float" style={{ animationDelay: '1s' }}>
                <div className="flex items-center gap-2">
                  <span className="relative flex h-3 w-3">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                  </span>
                  <span className="text-xs font-bold text-gray-800 tracking-wide uppercase">100% Konkretów</span>
                </div>
              </div>

              <div className="absolute -bottom-6 -left-8 bg-white px-4 py-3 rounded-2xl shadow-xl border border-gray-100 animate-float" style={{ animationDelay: '2s' }}>
                <div className="flex items-center gap-2">
                  <span className="text-xl">🎁</span>
                  <span className="text-xs font-bold text-gray-800">Bonus Todoist Pro</span>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
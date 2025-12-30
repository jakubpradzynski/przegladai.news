import React from 'react';
import { Linkedin, Facebook, Globe, Instagram } from 'lucide-react';

export const Author: React.FC = () => {
  return (
    <section className="bg-white py-24 relative overflow-hidden">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-center justify-center gap-12 md:gap-20">
          
          {/* Avatar Section */}
          <div className="flex-shrink-0 relative group">
             {/* Decorative background glow */}
             <div className="absolute inset-0 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-full blur-2xl opacity-20 scale-110 group-hover:opacity-30 transition-opacity duration-500"></div>
             <img 
               src="https://jakubpradzynski.pl/images/me.jpg" 
               alt="Jakub Prądzyński" 
               className="w-48 h-48 md:w-64 md:h-64 rounded-full object-cover border-4 border-white shadow-2xl relative z-10 transition-transform duration-500 group-hover:scale-105"
             />
          </div>

          {/* Content Section */}
          <div className="max-w-2xl text-center md:text-left">
            <h2 className="text-3xl md:text-4xl font-extrabold text-gray-900 mb-2 tracking-tight">O autorze</h2>
            <h3 className="text-xl md:text-2xl text-blue-600 font-semibold mb-6">Jakub Prądzyński</h3>
            
            <div className="text-lg text-gray-600 mb-8 leading-relaxed space-y-4">
              <p>
                Engineering Manager w Allegro. Pasjonat technologii, który na co dzień łączy świat biznesu z inżynierią oprogramowania. 
              </p>
              <p>
                W newsletterze "PrzeglądAI" dzielę się wyselekcjonowaną wiedzą, pomagając odnaleźć się w gąszczu informacji o sztucznej inteligencji, bez zbędnego szumu.
              </p>
            </div>

            {/* Social Icons */}
            <div className="flex justify-center md:justify-start gap-4">
              <a href="https://www.linkedin.com/in/jakubpradzynski/" target="_blank" rel="noopener noreferrer" className="p-3 bg-gray-50 rounded-full text-gray-600 hover:text-white hover:bg-[#0077b5] hover:shadow-lg transition-all duration-300" aria-label="LinkedIn">
                <Linkedin size={24} />
              </a>
              <a href="https://x.com/PradzynskiJakub" target="_blank" rel="noopener noreferrer" className="p-3 bg-gray-50 rounded-full text-gray-600 hover:text-white hover:bg-black hover:shadow-lg transition-all duration-300 flex items-center justify-center" aria-label="X (Twitter)">
                <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" className="w-6 h-6">
                  <path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z" />
                </svg>
              </a>
              <a href="https://www.facebook.com/jakub.pradzynski" target="_blank" rel="noopener noreferrer" className="p-3 bg-gray-50 rounded-full text-gray-600 hover:text-white hover:bg-[#1877F2] hover:shadow-lg transition-all duration-300" aria-label="Facebook">
                <Facebook size={24} />
              </a>
              <a href="https://www.instagram.com/jakubpradzynski/" target="_blank" rel="noopener noreferrer" className="p-3 bg-gray-50 rounded-full text-gray-600 hover:text-white hover:bg-[#E4405F] hover:shadow-lg transition-all duration-300" aria-label="Instagram">
                <Instagram size={24} />
              </a>
              <a href="https://jakubpradzynski.pl" target="_blank" rel="noopener noreferrer" className="p-3 bg-gray-50 rounded-full text-gray-600 hover:text-white hover:bg-blue-600 hover:shadow-lg transition-all duration-300" aria-label="Strona WWW">
                <Globe size={24} />
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
import React from 'react';
import { Logo } from './Logo';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-gray-100 py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-6 md:gap-0">
        <div className="flex flex-col items-center md:items-start text-center md:text-left">
          <Logo />
          <p className="text-gray-500 text-sm mt-2">
            Twój przewodnik w świecie AI.
          </p>
        </div>
        <div className="flex flex-col items-center md:items-end space-y-2 text-sm text-gray-400 text-center md:text-right">
          <div>
            &copy; {new Date().getFullYear()} PrzeglądAI. Wszystkie prawa zastrzeżone.
          </div>
          <div>
            Created by <a href="https://hvb.software/" target="_blank" rel="noopener noreferrer" className="hover:text-blue-600 transition-colors">HVB.software</a>
          </div>
        </div>
      </div>
    </footer>
  );
};
import React from 'react';
import { Logo } from './Logo';

interface NavbarProps {
  onSubscribeClick: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onSubscribeClick }) => {
  return (
    <nav className="sticky top-0 z-40 w-full bg-white/80 backdrop-blur-md border-b border-gray-100 transition-all duration-300">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Logo className="!text-xl" />
        <div className="flex items-center gap-4">
          <button
            onClick={onSubscribeClick}
            className="px-5 py-2 rounded-lg font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-all text-sm shadow-md hover:shadow-blue-500/25 active:scale-95"
          >
            Subskrybuj
          </button>
        </div>
      </div>
    </nav>
  );
};
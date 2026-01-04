import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { Hero } from './components/Hero';
import { Archive } from './components/Archive';
import { Author } from './components/Author';
import { PostView } from './components/PostView';
import { Footer } from './components/Footer';
import { Navbar } from './components/Navbar';
import { SubscribeModal } from './components/SubscribeModal';

interface HomePageProps {
  onSubscribeClick: () => void;
}

const HomePage: React.FC<HomePageProps> = ({ onSubscribeClick }) => {
  const location = useLocation();

  useEffect(() => {
    if (location.state && (location.state as any).scrollTo === 'archive') {
      const element = document.getElementById('archive');
      if (element) {
        // Niewielkie opóźnienie, aby upewnić się, że DOM jest gotowy
        setTimeout(() => {
          element.scrollIntoView({ behavior: 'smooth' });
        }, 100);
      }
    }
  }, [location]);

  return (
    <>
      <Hero onSubscribeClick={onSubscribeClick} />
      <Archive />
      <Author />
    </>
  );
};

const App: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <Router>
      <div className="min-h-screen bg-white flex flex-col font-sans selection:bg-blue-100 selection:text-blue-900">
        <Navbar onSubscribeClick={() => setIsModalOpen(true)} />
        <SubscribeModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
        
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<HomePage onSubscribeClick={() => setIsModalOpen(true)} />} />
            <Route path="/:slug" element={<PostView />} />
          </Routes>
        </main>

        <Footer />
      </div>
    </Router>
  );
};

export default App;
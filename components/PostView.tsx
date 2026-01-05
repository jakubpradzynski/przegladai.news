import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { BLOG_POSTS } from '../constants';
import { ArrowLeft, Clock, Calendar, Share2 } from 'lucide-react';

const IframeResizer: React.FC<{ src: string; title: string }> = ({ src, title }) => {
  const [height, setHeight] = useState('100vh');

  const handleLoad = (e: React.SyntheticEvent<HTMLIFrameElement, Event>) => {
    const iframe = e.target as HTMLIFrameElement;
    if (iframe.contentWindow) {
      try {
        const doc = iframe.contentWindow.document;

        // Otwieraj wszystkie linki w nowej karcie
        const base = doc.createElement('base');
        base.target = '_blank';
        doc.head.appendChild(base);

        // Obserwuj zmiany w DOM iframe'a
        const resizeObserver = new ResizeObserver(() => {
          if (iframe.contentWindow?.document.body) {
            setHeight(`${iframe.contentWindow.document.body.scrollHeight}px`);
          }
        });
        
        resizeObserver.observe(doc.body);
        
        // Ustaw początkową wysokość
        setHeight(`${doc.body.scrollHeight}px`);
      } catch (error) {
        console.warn('Cannot access iframe content for resizing (CORS policy?)', error);
      }
    }
  };

  return (
    <iframe
      src={src}
      className="w-full border-none transition-all duration-200"
      style={{ height, overflow: 'hidden' }}
      title={title}
      onLoad={handleLoad}
      scrolling="no"
    />
  );
};

export const PostView: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  
  const post = BLOG_POSTS.find(p => p.slug === slug);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [slug]);

  const handleBack = (e: React.MouseEvent) => {
    e.preventDefault();
    navigate('/', { state: { scrollTo: 'archive' } });
  };

  if (!post) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center text-center px-4">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Nie znaleziono wydania</h2>
        <p className="text-gray-600 mb-8">Wygląda na to, że ten numer newslettera nie istnieje.</p>
        <button 
          onClick={() => navigate('/')} 
          className="text-blue-600 font-semibold hover:underline flex items-center"
        >
          <ArrowLeft size={20} className="mr-2" /> Wróć do strony głównej
        </button>
      </div>
    );
  }

  // Renderowanie dla wydania opartego na pliku HTML (newsletter)
  if (post.htmlUrl) {
    return (
      <div className="flex flex-col min-h-screen bg-gray-50">
        <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center shadow-sm flex-shrink-0 z-10 sticky top-0">
          <button 
            onClick={handleBack} 
            className="flex-shrink-0 flex items-center text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors"
          >
            <ArrowLeft size={16} className="mr-2" /> Wróć do archiwum
          </button>
        </div>
        
        <div className="bg-white border-b border-gray-200 px-4 py-5 flex-shrink-0">
          <div className="max-w-4xl mx-auto">
             <h1 className="text-xl sm:text-2xl font-extrabold text-gray-900 leading-tight">
               {post.title}
             </h1>
             <div className="flex items-center text-gray-500 text-sm mt-3">
               <Calendar size={14} className="mr-2" />
               {post.date}
             </div>
          </div>
        </div>

        <div className="flex-grow w-full">
           <IframeResizer src={post.htmlUrl} title={post.title} />
        </div>
      </div>
    );
  }

  // Renderowanie dla standardowego posta tekstowego (jeśli content istnieje)
  return (
    <article className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-20">
      <button 
        onClick={handleBack} 
        className="inline-flex items-center text-gray-500 hover:text-blue-600 transition-colors mb-8 group bg-transparent border-none cursor-pointer"
      >
        <ArrowLeft size={20} className="mr-2 transition-transform group-hover:-translate-x-1" />
        Wróć do listy
      </button>

      <header className="mb-10 text-center">
        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-gray-900 mb-6 leading-tight">
          {post.title}
        </h1>
        <div className="flex items-center justify-center text-gray-500 text-sm space-x-6">
          <div className="flex items-center">
            <Calendar size={16} className="mr-2" />
            {post.date}
          </div>
          <div className="flex items-center">
            <Clock size={16} className="mr-2" />
            5 min czytania
          </div>
        </div>
      </header>

      {post.imageUrl && (
        <div className="rounded-2xl overflow-hidden shadow-2xl mb-12 aspect-video relative">
          <img src={post.imageUrl} alt={post.title} className="w-full h-full object-cover" />
        </div>
      )}

      {post.content && (
        <div className="prose prose-lg prose-blue mx-auto text-gray-700">
          <div dangerouslySetInnerHTML={{ __html: post.content }} />
        </div>
      )}

      <div className="mt-12 pt-8 border-t border-gray-200 flex justify-between items-center">
        <div className="font-semibold text-gray-900">
          Udostępnij to wydanie:
        </div>
        <div className="flex space-x-4">
          <button className="p-2 rounded-full hover:bg-gray-100 text-gray-600 transition-colors">
            <Share2 size={20} />
          </button>
        </div>
      </div>
    </article>
  );
};
import React from 'react';
import { Link } from 'react-router-dom';
import { BLOG_POSTS } from '../constants';
import { Sparkles, Clock } from 'lucide-react';

export const Archive: React.FC = () => {
  return (
    <section className="bg-gray-50 py-24 relative overflow-hidden" id="archive">
      {/* Background decoration */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none opacity-30">
          <div className="absolute top-10 left-10 w-64 h-64 bg-blue-100 rounded-full mix-blend-multiply filter blur-3xl"></div>
          <div className="absolute bottom-10 right-10 w-64 h-64 bg-indigo-100 rounded-full mix-blend-multiply filter blur-3xl"></div>
      </div>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="inline-flex items-center justify-center p-2 bg-blue-50 rounded-full mb-4">
            <Sparkles size={16} className="text-blue-600 mr-2" />
            <span className="text-blue-800 text-sm font-semibold tracking-wide uppercase">Archiwum</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 mb-6 tracking-tight">
            Poprzednie wydania
          </h2>
          <p className="text-lg text-gray-600 leading-relaxed">
            Każdy numer to skondensowana dawka wiedzy. Przeglądaj archiwum, aby nadrobić zaległości w świecie AI.
          </p>
        </div>

        <div className="max-w-5xl mx-auto flex flex-col gap-3">
          {BLOG_POSTS.length > 0 ? (
            BLOG_POSTS.map((post) => (
              <Link 
                key={post.id} 
                to={`/${post.slug}`}
                className="group flex flex-col sm:flex-row sm:items-center bg-white border border-gray-200 rounded-lg p-5 hover:border-blue-500 hover:shadow-md transition-all duration-200"
              >
                <span className="text-sm font-mono text-gray-500 sm:w-32 flex-shrink-0 group-hover:text-blue-600 transition-colors mb-1 sm:mb-0">
                  {post.date}
                </span>
                <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-700 transition-colors">
                  {post.title}
                </h3>
              </Link>
            ))
          ) : (
            <div className="flex flex-col items-center justify-center py-16 px-4 bg-white border border-gray-100 rounded-2xl shadow-sm text-center">
              <div className="bg-blue-50 p-4 rounded-full mb-6">
                <Clock size={32} className="text-blue-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">
                Już wkrótce...
              </h3>
              <p className="text-gray-600 max-w-md mx-auto">
                Pierwsze wydanie newslettera jest właśnie przygotowywane. 
                Zapisz się powyżej, aby otrzymać je jako pierwszy!
              </p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};
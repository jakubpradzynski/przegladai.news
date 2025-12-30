import React from 'react';
import { Link } from 'react-router-dom';
import { BlogPost } from '../types';
import { ArrowRight, Calendar } from 'lucide-react';

interface Props {
  post: BlogPost;
}

export const NewsletterCard: React.FC<Props> = ({ post }) => {
  return (
    <Link 
      to={`/${post.slug}`}
      className="group flex flex-col bg-white border border-gray-100 rounded-2xl overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 h-full"
    >
      <div className="h-48 overflow-hidden relative">
        <div className="absolute inset-0 bg-gray-900 opacity-0 group-hover:opacity-10 transition-opacity z-10" />
        <img 
          src={post.imageUrl} 
          alt={post.title} 
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
        />
      </div>
      <div className="p-6 flex flex-col flex-grow">
        <div className="flex items-center text-xs text-gray-500 mb-3 space-x-2">
          <Calendar size={14} className="text-blue-500" />
          <time dateTime={post.date}>{post.date}</time>
        </div>
        <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors leading-tight">
          {post.title}
        </h3>
        <div className="flex items-center text-sm font-medium text-blue-600 mt-auto pt-4 border-t border-gray-50 group-hover:border-blue-50 transition-colors">
          Czytaj wydanie <ArrowRight size={16} className="ml-1 transition-transform group-hover:translate-x-1" />
        </div>
      </div>
    </Link>
  );
};
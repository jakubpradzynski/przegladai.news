import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useParams } from 'react-router-dom';

const SUBSTACK_BASE = 'https://przegladai.substack.com';

const RootRedirect: React.FC = () => {
  useEffect(() => {
    window.location.replace(SUBSTACK_BASE + '/');
  }, []);
  return null;
};

const SlugRedirect: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  useEffect(() => {
    window.location.replace(`${SUBSTACK_BASE}/p/${slug}`);
  }, [slug]);
  return null;
};

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<RootRedirect />} />
        <Route path="/:slug" element={<SlugRedirect />} />
      </Routes>
    </Router>
  );
};

export default App;
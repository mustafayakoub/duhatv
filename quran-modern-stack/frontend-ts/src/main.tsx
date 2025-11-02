import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Set document direction to RTL
document.documentElement.dir = 'rtl';
document.documentElement.lang = 'ar';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

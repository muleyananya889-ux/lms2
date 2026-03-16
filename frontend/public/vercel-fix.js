// Vercel deployment fix
// This script ensures the app works properly on Vercel

// Fix for Vercel routing
if (window.location.pathname !== '/' && !window.location.pathname.includes('/login') && !window.location.pathname.includes('/signup')) {
  // Ensure React Router works with Vercel's file-based routing
  window.history.replaceState({}, '', '/');
}

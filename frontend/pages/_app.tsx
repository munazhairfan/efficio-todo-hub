// pages/_app.tsx
// Main application component with authentication context
// Build trigger: 2026-01-08

import '../styles/globals.css'; // Assuming there's a global CSS file
import type { AppProps } from 'next/app';
import { AuthProvider } from '../components/auth/AuthProvider';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  );
}

export default MyApp;
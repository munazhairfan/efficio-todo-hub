/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // Optional: Allow external images if needed
  images: {
    // Remove unoptimized: true to allow Vercel to optimize images
  },
  trailingSlash: false, // Standard Next.js behavior
  // Ensure path aliases work properly in Vercel
  experimental: {
    esmExternals: 'loose', // Allow mixed ES modules and CommonJS
  },
};

module.exports = nextConfig;
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      // ─── Design Tokens ────────────────────────────────────────────────
      // All colors, fonts, and spacing defined here.
      // NEVER use hardcoded hex values in component files.
      colors: {
        // Canvas / surface
        canvas:  '#FDFDFD',
        surface: '#FFFFFF',

        // Text hierarchy
        ink: {
          DEFAULT: '#050505',
          muted:   '#52525B',
          ghost:   '#A1A1AA',
        },

        // Brand accent
        accent: {
          DEFAULT: '#002FA7',
          hover:   '#002280',
        },

        // Borders & dividers
        edge: '#E4E4E7',

        // Muted backgrounds
        wash: '#F4F4F5',

        // Semantic status
        status: {
          published: '#16a34a',
          draft:     '#ca8a04',
        },
      },

      fontFamily: {
        // Use `font-display` for headings, `font-body` for prose, `font-code` for mono
        display: ['Outfit', 'sans-serif'],
        body:    ['IBM Plex Sans', 'sans-serif'],
        code:    ['JetBrains Mono', 'monospace'],
      },

      fontSize: {
        'hero':  ['clamp(2.5rem, 6vw, 4rem)', { lineHeight: '1', letterSpacing: '-0.04em', fontWeight: '900' }],
        'h1':    ['clamp(2rem, 4vw, 3rem)',   { lineHeight: '1.1', letterSpacing: '-0.03em', fontWeight: '800' }],
        'h2':    ['1.5rem',  { lineHeight: '1.2', fontWeight: '700' }],
        'h3':    ['1.25rem', { lineHeight: '1.3', fontWeight: '600' }],
      },

      boxShadow: {
        card:  '0 4px 24px rgb(0 0 0 / 0.06)',
        hover: '0 8px 32px rgb(0 0 0 / 0.10)',
      },

      animation: {
        'fade-up': 'fadeUp 0.4s ease both',
        'spin-slow': 'spin 1.5s linear infinite',
      },
      keyframes: {
        fadeUp: {
          '0%':   { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
};

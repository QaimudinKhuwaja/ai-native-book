/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
    './docs/**/*.{md,mdx}',
    './blog/**/*.{md,mdx}',
  ],
  safelist: [
    'bg-white/opacity-10',
    'border-white/opacity-20',
    'bg-white/opacity-5',
  ],
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9f8',
          100: '#dcf1f0',
          200: '#b8e3e1',
          300: '#94d5d2',
          400: '#70c7c3',
          500: '#4bb9b4',
          600: '#389591',
          700: '#257e7a',
          800: '#155355',
          900: '#0d3332',
        },
      },
      keyframes: {
        'fade-in-down': {
          '0%': {
            opacity: '0',
            transform: 'translateY(-10px)',
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0)',
          },
        },
      },
      animation: {
        'fade-in-down': 'fade-in-down 0.3s ease-out',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};

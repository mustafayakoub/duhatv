/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // الألوان الذهبية لمشروع بصائر
        golden: {
          50: '#fefce8',
          100: '#fef9c3',
          200: '#fef08a',
          300: '#fde047',
          400: '#facc15',
          500: '#eab308',
          600: '#ca8a04',
          700: '#a16207',
          800: '#854d0e',
          900: '#713f12',
        },
        bronze: {
          50: '#faf8f5',
          100: '#f5f0e8',
          200: '#ebe2d1',
          300: '#dcc9aa',
          400: '#ccac7d',
          500: '#b8956a',
          600: '#9b7d57',
          700: '#7d6549',
          800: '#69543e',
          900: '#594836',
        },
      },
      fontFamily: {
        arabic: ['Amiri', 'Noto Naskh Arabic', 'Traditional Arabic', 'serif'],
        uthmanic: ['KFGQPC Uthmanic Script HAFS', 'Scheherazade New', 'serif'],
      },
    },
  },
  plugins: [],
}

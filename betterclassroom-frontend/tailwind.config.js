/** @type {import('tailwindcss').Config} */
export default {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  content: ["./src/**/*.{html,js}"],
  content: [],
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
}


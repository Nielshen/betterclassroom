/** @type {import('tailwindcss').Config} */
export default {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  content: ["./src/**/*.{html,js}"],
  content: [],
  theme: {
    extend: {},
  },
  daisyui: {
    themes: [
      {
        mytheme: {
          "primary": "#334152",
          "primary-content": "#FFFFFF",
          "secondary": "#FFFFFF",
          "secondary-content": "#161616",
          "accent": "#009B91",
          "accent-content": "#FFFFFF",
          "neutral": "#334152",
          "neutral-content": "#FFFFFF",
          "base-100": "#D9E5EC",
          "base-200": "#bdc7cd",
          "base-300": "#a1aaaf",
          "base-content": "#000000",
          "info": "#000000",
          "info-content": "#FFFFFF",
          "success": "#009B91",
          "success-content": "#FFFFFF",
          "warning": "#009B91",
          "warning-content": "#FFFFFF",
          "error": "#009B91",
          "error-content": "#FFFFFF",
        },
      },
    ],
  },
  plugins: [require('daisyui')],
}


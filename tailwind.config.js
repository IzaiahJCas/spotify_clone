/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      boxShadow: {
        "custom-shadow": "0 4px 6px rgba(89, 38, 233, 0.42)",
      },
      colors: {
        "background-grey": "rgb(43, 42, 42)",
        "background-grey-opacity": "rgb(33, 32, 32, 0.5)",
        "background-grey-text": "rgb(53, 52, 52)",
      },
    },
  },
  plugins: [],
};

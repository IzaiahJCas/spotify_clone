/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      boxShadow: {
        "custom-shadow": "0 4px 6px rgba(233, 30, 99, 0.5)",
      },
      colors: {
        "background-grey": "rgb(43, 42, 42)",
      },
    },
  },
  plugins: [],
};

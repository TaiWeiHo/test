/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'choco-dark': '#2c1e16', // 深巧克力色，用於文字和Logo
      },
      fontFamily: {
        sans: ['"Noto Sans TC"', 'Microsoft JhengHei', 'sans-serif'], // 設定通用字體
      }
    },
  },
  plugins: [],
}
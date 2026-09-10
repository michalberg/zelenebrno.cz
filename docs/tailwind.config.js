/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.html", "!./node_modules/**"],
  theme: {
    extend: {
      colors: {
        green: { DEFAULT: '#0BD26F', deep: '#06A856' },
        pink:  { DEFAULT: '#FFA6D1', hot:  '#FF7DBE' },
        ink:   '#000000',
        paper: '#FFFFFF',
        rule:  '#D9D9D9',
      },
      fontFamily: {
        sans:           ['Archivo', 'system-ui', 'sans-serif'],
        mono:           ['"JetBrains Mono"', 'monospace'],
        display:        ['"Tusker Grotesk"', '"Tusker Grotesk SemiBold"', 'Archivo', 'system-ui', 'sans-serif'],
        'display-bold': ['"Tusker Grotesk Bold"', 'Archivo', 'system-ui', 'sans-serif'],
        name:           ['"Urban Grotesk"', 'Archivo', 'system-ui', 'sans-serif'],
        svgd:           ['"SVGD"', 'Archivo', 'system-ui', 'sans-serif'],
      },
      maxWidth: { container: '1280px' },
      screens:  { 'wide': '1900px', 'nav': '1100px', 'xs':  '380px' },
      boxShadow: {
        card:       '0 14px 30px -18px rgba(0, 0, 0, 0.25)',
        'card-lg':  '0 18px 40px -20px rgba(0, 0, 0, 0.18)',
        btn:        '0 6px 18px -6px rgba(0, 0, 0, 0.25)',
        arrow:      '0 6px 18px -6px rgba(0, 0, 0, 0.3)',
        'arrow-lg': '0 6px 18px -6px rgba(0, 0, 0, 0.35)',
        faq:        '0 0 15px 0 rgba(0, 0, 0, 0.1)',
      },
    }
  },
}

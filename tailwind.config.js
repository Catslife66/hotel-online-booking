/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./templates/**/*.{html,js}", 
      "./templates/*.{html,js}",
      "./node_modules/flowbite/**/*.js",
    ],
    theme: {
      extend: {
        colors: {
          'dark-base': 'rgb(80, 109, 99)',
          'base': 'rgb(106, 160, 127)',
          'rose': 'rgb(163, 90, 118)',
          'roseLight': 'rgba(163, 90, 118, 0.1)',
        },
      },
    },
    plugins: [
      require('flowbite/plugin')
    ],
  }
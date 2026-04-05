import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  define: {
    // This safely fixes the Plotly.js "global is not defined" error in Vite
    global: 'window',
  },
})
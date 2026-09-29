import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  server: {
    host: '0.0.0.0',
    port: Number(process.env.ELEDETECTIVE_PORT || 5180),
    strictPort: true,
    proxy: {
      '/backend': { target: 'http://127.0.0.1:' + (process.env.ELEDETECTIVE_BACKEND_PORT || 5102), rewrite: path => path.replace(/^\/backend/, ''), timeout: 0, proxyTimeout: 0 },
      '/grid': { target: 'http://127.0.0.1:12121', rewrite: path => path.replace(/^\/grid/, ''), timeout: 0, proxyTimeout: 0 },
    },
    watch: {
      usePolling: true
    }
  },
  define: {
    global: 'window' // 将 `global` 映射到 `window`
  }
})

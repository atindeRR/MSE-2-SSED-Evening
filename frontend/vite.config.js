import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        // Isolate react/react-dom into their own chunk to avoid a Rollup
        // commonjs-resolver "code nested too deeply" error on react-dom/client.js
        // that affects react-dom >=18.3.x with Rollup >=4.x.
        manualChunks(id) {
          if (id.includes('node_modules/react') || id.includes('node_modules/react-dom')) {
            return 'vendor-react';
          }
        },
      },
    },
  },
});

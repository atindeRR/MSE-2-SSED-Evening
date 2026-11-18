import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  // Force Vite to pre-bundle react-dom/client via esbuild (which has no
  // parser-nesting depth limit).  Without this, Rollup's commonjs plugin
  // tries to parse the raw CJS file and hits its recursion-depth cap on
  // Rollup 4.24+ inside Docker.
  optimizeDeps: {
    include: ['react', 'react-dom', 'react-dom/client'],
  },
  build: {
    // Increase the commonjs transform depth limit and ensure the
    // pre-bundled ESM versions of react / react-dom are used in the
    // production Rollup pass as well.
    commonjsOptions: {
      include: [/node_modules/],
    },
  },
});

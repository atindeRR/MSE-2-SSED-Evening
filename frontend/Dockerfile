# ── Stage 1: build ──────────────────────────────────────────────────────────
# Build on the host's Node version pinned to match local dev environment.
# Vite 6 + react-dom 18 triggers a Rollup "code is nested too deeply" parse
# error inside Docker when the commonjs plugin tries to analyse react-dom/client.
# Work-around: build outside the container (npm run build on the host) and
# copy the resulting dist/ into the Nginx image.  The dist/ folder is
# intentionally NOT listed in .dockerignore so that the pre-built artefact
# is available to COPY below.

FROM nginx:1.27-alpine

# Remove default placeholder content
RUN rm -rf /usr/share/nginx/html/*

# Copy the pre-built Vite output produced by `npm run build` on the host
COPY dist/ /usr/share/nginx/html/

# Custom Nginx config: SPA fallback + reverse-proxy /api and /health to backend
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

FROM nginxinc/nginx-unprivileged:alpine

# Upgrade brotli-libs to fix CVE-2026-111497
USER root
RUN apk update && apk upgrade --no-cache brotli-libs
USER nginx

# Copy your web assets
COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
COPY script.js /usr/share/nginx/html/
COPY 1.png /usr/share/nginx/html/
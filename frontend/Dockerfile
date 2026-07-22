FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY frontend/nginx.conf /etc/nginx/conf.d/

# Copy static frontend files
COPY frontend/ /usr/share/nginx/html/

EXPOSE 80

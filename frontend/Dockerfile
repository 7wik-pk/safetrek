# Stage 1: Build the Vue app
FROM node:20-alpine AS build
WORKDIR /app

COPY . .

RUN npm install
RUN npm run build -- --mode development

# Stage 2: Serve with Nginx
FROM nginx:alpine
COPY --from=build /app/frontend-dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

FROM node:22-alpine AS build

WORKDIR /app

COPY package.json ./

# --- İŞTE EKSİK OLAN KISIM BURASI ---
# Bu iki satır olmazsa stil dosyaları oluşmaz!
COPY tailwind.config.js ./
COPY postcss.config.js ./
# ------------------------------------

COPY vite.config.mts ./
COPY index.html ./
COPY src ./src

RUN npm install && npm run build

FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
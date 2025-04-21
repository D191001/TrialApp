FROM node:16 as build

WORKDIR /app

# Устанавливаем зависимости
COPY package*.json ./
RUN npm ci

# Копируем исходники
COPY . .

# Собираем приложение
RUN npm run build

# Production образ
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]

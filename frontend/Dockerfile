FROM node:16 as build

WORKDIR /app

# Устанавливаем Vue CLI глобально
RUN npm install -g @vue/cli@5.0.8

# Копируем файлы package.json и устанавливаем зависимости
COPY package*.json ./
RUN npm install

# Копируем исходники
COPY . .

# Собираем приложение
RUN npm run build

# Готовим production образ
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]

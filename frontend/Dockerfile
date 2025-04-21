FROM node:16-alpine as build

WORKDIR /app

# Устанавливаем только production зависимости
COPY package*.json ./
RUN npm ci --only=production --no-audit

# Копируем исходники и собираем приложение
COPY . .
RUN npm run build

# Финальный образ
FROM node:16-alpine
WORKDIR /app
RUN npm install -g serve@14.2.1
COPY --from=build /app/dist ./dist
EXPOSE 8080
CMD ["serve", "-s", "dist", "-p", "8080"]

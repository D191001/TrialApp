FROM node:16-alpine

WORKDIR /app

ENV NODE_ENV=production
ENV CI=true

COPY package*.json ./

# Устанавливаем зависимости с флагами для CI
RUN npm ci --only=production --no-audit

COPY . .

USER node

EXPOSE 8080

CMD ["npm", "run", "serve"]

FROM node:16-alpine

WORKDIR /app

ENV NODE_ENV=production
ENV CI=true

COPY package*.json ./
RUN npm install --legacy-peer-deps --no-interactive

COPY . .

# Оптимизируем chown, применяем только к необходимым директориям
RUN chown -R node:node /app/node_modules /app/.cache 2>/dev/null || true

USER node

EXPOSE 8080

CMD ["npm", "run", "serve"]

FROM node:16-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:16-alpine
WORKDIR /app
COPY --from=build /app/dist ./dist
RUN npm install -g serve@14.2.1
EXPOSE 8080
CMD ["npx", "serve", "-s", "dist", "-l", "8080"]

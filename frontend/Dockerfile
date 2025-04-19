FROM node:16

WORKDIR /app

COPY package*.json ./
COPY ../requirements.txt .

RUN npm install

COPY . .

EXPOSE 8080

CMD ["npm", "run", "serve"]

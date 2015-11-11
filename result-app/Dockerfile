FROM node:0.10

ADD . /app

WORKDIR /app

RUN npm install

ENV PORT 8080
EXPOSE 8080

CMD ["node", "server.js"]

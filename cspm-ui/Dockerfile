FROM --platform=linux/amd64 node:25.2.1-alpine

COPY . .

WORKDIR /src

RUN npm ci
RUN npm run format
# RUN npm run lint
# RUN npm run test:unit
RUN npm run build

EXPOSE 3000

RUN npm install -g serve

CMD ["serve", "-s", "dist"]

# Etapa de construcción
FROM node:18 AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install && ls -l node_modules/.bin
ENV PATH="./node_modules/.bin:$PATH"  
RUN chmod -R 755 /app 
RUN chmod -R 755 /app/node_modules/.bin  
COPY . .
RUN npm run build

# Etapa de producción
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

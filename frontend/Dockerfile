# Build Stage
FROM node:20 AS build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend ./

# Accept API URL at build time
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# Production Stage
FROM nginx:stable-alpine
# Copy template to the templates directory for envsubst
COPY nginx/conf.d/default.conf.template /etc/nginx/templates/default.conf.template

# Copy built assets
COPY --from=build /app/frontend/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
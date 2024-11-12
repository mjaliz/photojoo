FROM node:21-alpine3.20 AS builder
# ENV NODE_ENV production
# Add a work directory
WORKDIR /app
# Cache and Install dependencies
COPY package.json package-lock.json ./
RUN npm install
# Copy app files
COPY . .
# Build the app
RUN npm run build
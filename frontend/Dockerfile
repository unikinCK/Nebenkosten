FROM node:20-alpine

WORKDIR /app

COPY frontend/package.json /app/package.json
COPY frontend/package-lock.json /app/package-lock.json

RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

COPY frontend /app

EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]

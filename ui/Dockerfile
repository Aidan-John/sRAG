FROM node:20-alpine as base

# Set the working directory

WORKDIR /app

# Install dependencies

COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* .npmrc* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
  else echo "Lockfile not found." && exit 1; \
  fi


# Copy the rest of the app

COPY . .

# Copy the Next.js configuration file
# This is necessary for hot reload

COPY next.config.ts ./next.config.ts

# Expose the app

EXPOSE 3000

# Start the app

CMD ["npm", "run", "dev"]

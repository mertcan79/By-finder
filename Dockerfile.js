# Use the official Node.js base image
FROM node:14

# Set the working directory
WORKDIR /byfinder

# Copy package.json and package-lock.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the app's source code
COPY . .

# Command to start the React app (modify as needed)
CMD ["npm", "start"]

# Build Docker image
docker build -t citydb-roofmats-ai .

# Run the Docker container
docker run -p 8080:80 -p 5000:5000 citydb-roofmats-ai

# Push to DockerHub
docker tag citydb-roofmats-ai sonhng/citydb-roofmats-ai:latest
docker login
docker push sonhng/citydb-roofmats-ai:latest
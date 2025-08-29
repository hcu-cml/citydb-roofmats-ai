# FOR LOCAL ARCHITECTURE

# Build Docker image
docker build -t citydb-roofmats-ai .

# Run the Docker container
docker run -p 8080:80 -p 5000:5000 citydb-roofmats-ai

# Push to DockerHub
docker tag citydb-roofmats-ai sonhng/citydb-roofmats-ai:latest
docker login
docker push sonhng/citydb-roofmats-ai:latest

# -----

# FOR MULTI-ARCHITECTURE

# Build and test using Apple Silicon
docker buildx build --platform linux/arm64 -t sonhng/citydb-roofmats-ai:linux-latest --load .
docker run -p 8080:80 -p 5000:5000 sonhng/citydb-roofmats-ai:linux-latest

# Verify image content
docker buildx imagetools inspect sonhng/citydb-roofmats-ai:linux-latest

# Pubish to DockerHub
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t sonhng/citydb-roofmats-ai:linux-latest \
  --push .

# ----

# FOR WINDOWS

# FOR LOCAL ARCHITECTURE

# Build Docker image
docker build -t citydb-roofmats-ai .

# Run the Docker container
docker run -p 8080:80 -p 5000:5000 citydb-roofmats-ai

# Push to DockerHub
docker tag citydb-roofmats-ai sonhng/citydb-roofmats-ai:windows-latest
docker login
docker push sonhng/citydb-roofmats-ai:windows-latest

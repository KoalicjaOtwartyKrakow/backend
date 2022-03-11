cp -r ../Database .
docker build -t test-postgres-kok -f Dockerfile.database .

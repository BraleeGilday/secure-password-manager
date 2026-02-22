# local script to create docker images
#!/bin/bash
set -e

source .env.prod

echo timeout: "$TIMEOUT"

echo "creating docker images"

docker compose -f docker-compose.prod.yml build frontend 
docker image prune -f
docker save -o spm_build.tar frontend:latest

echo "copying over docker images"

# scp -i "$PEM_PATH" spm_build.tar "$EC2_USER@$EC2_HOST"

rm -vf spm_build.tar

echo "images pushed!"
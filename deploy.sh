# local script to create docker images
#!/bin/bash
set -e

set -a
source .env.prod
set +a

echo "creating docker images"

docker compose -f docker-compose.prod.yml build  
docker image prune -f
docker save -o spm_build.tar spm-backend:latest spm-frontend:latest

echo "copying over docker images"

scp -i "$PEM_PATH" spm_build.tar "$EC2_USER@$EC2_HOST":~/

echo "clean up!"

rm -vf spm_build.tar

echo "images pushed!"
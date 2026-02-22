# for use in EC2 instance CLI
#!/bin/bash

docker load -i spm_build.tar

rm -vf spm_build.tar

docker image prune -f

echo "run 'docker compose -f docker-compose.prod.yml' up to start server"
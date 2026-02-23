# for use in EC2 instance CLI
#!/bin/bash
set -e

set -a
source .env.prod
set +a

echo "logging into AWS EC2"
ssh -i "$PEM_PATH" "$EC2_USER@$EC2_HOST" << EOF
    # make sure we actually log in...
    sleep 5 &

    echo "loading images"
    docker load -i spm_build.tar

    cd secure-password-manager
    echo "current directory: \$(pwd)"

    echo "starting server..."
    docker compose -f docker-compose.prod.yml up -d --remove-orphans

    echo "cleaning up..."
    rm -vf ~/spm_build.tar

    docker image prune -f
EOF

echo "job's done!"
echo "you can now view SPM"

# echo "run 'docker compose -f docker-compose.prod.yml' up to start server"
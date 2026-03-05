# secure-password-manager

The project's primary objectives and deliverables include:
- A fully functional web-based password manager that allows users to register, log in/out, and securely store their website credentials in an encrypted vault.
- Multi-factor authentication when the user logs in with their master password.
- A password suggestion feature that generates strong, unique passwords based on user input.
- Robust encryption and security mechanisms to protect user data in the vault.
- Secure hosting of the application in the cloud.
- Documentation and user guides for the application.

# docker for local development

## pre-requisites 
- docker desktop must be installed (or you need access to a VM)
- your .env file will need to be in the root directory
- add to your .env file:
- config.py should cover most of these, RDS/EC2 are not needed for local development

```
POSTGRES_USER=<string>
POSTGRES_PASSWORD=<string>
POSTGRES_DB = "spm_db"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_ENGINE = "postgresql+psycopg2"
```
## build local docker images
- run ```docker compose -f docker-compose.yml up --build --remove-orphans```
- ```-d``` flag will run docker in the background
- this will build the images and start the containers (in the foreground)
- access the application at ```localhost:3000```
- open new terminal
- run ```docker compose exec backend alembic upgrade head``` to initialize the database
- note the database will not persist across use in local dev once docker images are removed
- when finished run ```docker compose down``` to clean up/remove the images

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
```
POSTGRES_USER=<string>
POSTGRES_PASSWORD=<string>
POSTGRES_DB = "spm_db"
POSTGRES_HOST = "localhost"
POSTGRES_ENGINE = "postgresql+psycopg2"
```
## build docker images
- run ```docker compose up -build```
- this will build the images and start the containers
- access the application at localhost:3000

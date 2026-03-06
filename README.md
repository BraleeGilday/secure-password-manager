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
- ensure that you have docker desktop (or can run docker compose) and it is running
- clone the repository 
- navigate to the root directory ```cd secure-password-manager```
- create your .env file in the root directory and replace the values `<string>`:
    ```
    POSTGRES_USER=<string>
    POSTGRES_PASSWORD=<string>
    POSTGRES_DB = "spm_db"
    POSTGRES_HOST = "db"
    POSTGRES_PORT = "5432"
    POSTGRES_ENGINE = "postgresql+psycopg2"
    ```
- Note: config.py should cover most of these, RDS/EC2 are not needed for local development

## build local docker images

- run ```docker compose up --build --remove-orphans``` to start the containers (this will by default run docker-compose.yml)
- optionally run ```-d``` flag to run docker in the background
- setup the database (open new terminal if d flag was not set)
- a. on initial set up, create the migrations directory: ```docker compose run backend alembic init migrations```
you should now see a folder ```migrations``` navigate and update ```migrations/env.py``` by adding:
    ```
    # add to imports
    import models
    from database import POSTGRES_DB_URL

    # update target_metadata variable
    target_metadata = models.Base.metadata

    # below target_metadata add
    config.set_main_option("sqlalchemy.url", POSTGRES_DB_URL)
    ```
- b. run ``` docker compose exec backend alembic revision --autogenerate```
- Note: On subsequent uses, you should not need to setup migrations or autogenerate (steps a, b)
- c. run ```docker compose exec backend alembic upgrade head```
- Note: If you make changes to the backend/database, run this command during future development
- Open your web browser and navigate to ```localhost:3000``` to test out the site

## clean up
- Once finished, clean up the docker containers: 
    ```
    docker compose down
    docker image prune -f
    ```

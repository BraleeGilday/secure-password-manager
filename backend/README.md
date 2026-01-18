- generate secret key for .env: 
    ```
    #!/bin/bash 
    # generate .env script?
    openssl rand -hex 32
    ```

- navigate to backend:
    ```
    cd backend
    ```

- create virtual environment
    ```
    python3 -m venv <venv name>
    ```

- install dependencies:
    ```
    pip3 install -r requirements.txt
    ```

- Initialize alembic:
    ```
    alembic init migrations
    ```

- Update `alembic.ini`:
    ```
    sqlalchemy.url = sqlite:///./spm.db
    ```

- Update `alembic/env.py`:
    ```
    import models
    target_metadata = models.Base.metadata
    ```

- Generate and apply migrations:
    ```
    alembic revision -autogenerate
    alembic upgrade head
    ```

- start server:
    ```
    uvicorn main:app --reload
    ```

- to view APIs (once backend is running):
    ```
    go to URL http://127.0.0.1:8000/docs
    ```
# College Marketplace Backend API using FastAPI

### Demo link: tiny.cc/

![](https://media.discordapp.net/attachments/683899874034319360/1152318354825158666/Screenshot_2023-09-15_at_3.00.04_PM.png?width=1902&height=1124)

##  API Routes

This API provides 4 routes:

### 1. Listing Route

This route handles the retrieval, creation, deletion, and updating of listings.

### 2. Users Route

This route is used for user creation, searching users by ID, searching listings by user ID, and retrieving orders for a logged-in user.

### 3. Auth Route

This route manages user login and authentication.

### 4. Orders Route

This route is used to create new orders for an existing listing and change the status of a pending order.

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/Romansth/College-Marketplace-FASTAPI.git
   cd College-Marketplace-FASTAPI
   ```
   
2.  Create a virtual environment:
    ```bash 
    python3.9 -m venv <virtual_env_path>
    ```
3.  Activate the virtual environment:
    ```bash
    source  <virtual_env_path>/bin/activate
    ```

### Running Locally
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt  
    ```
    
2.  Start the API:
    ```python
    uvicorn app.main:app --reload
    ```
3.  Access the API documentation at:
    `http://127.0.0.1:8000/docs`
    
5.  Set up a PostgreSQL database and create a `.env` file in the root folder with the following content:
    
    `DATABASE_HOSTNAME=localhost DATABASE_PORT=5432 DATABASE_PASSWORD=your_database_password DATABASE_NAME=your_database_name DATABASE_USERNAME=your_database_username SECRET_KEY=09d25e094faa2556c818166b7a99f6f0f4c3b88e8d3e7 ALGORITHM=HS256 ACCESS_TOKEN_EXPIRE_MINUTES=60`
    
    Note: Replace the placeholder values with your actual database configuration.
    
6.  Use a secure, unique SECRET_KEY from the FastAPI documentation.
    
7.  To run tests with pytest: 
    ```python
    pytest
### Running Locally with Docker

1. Prerequisites:

- Docker: Follow the [installation instructions](https://docs.docker.com/install/#supported-platforms) if you don't have it installed.
- Docker Compose: Refer to the [official documentation](https://docs.docker.com/compose/install/) for installation guidance.

2. Build the Stack
```bash
docker-compose -f local.yml build
```

3. Run the Stack
```bash
docker-compose -f docker-compose-dev.yaml up
```

You can set environment variables manually in `docker-compose-dev.yaml` or point `.env` variables to the `docker-compose-dev.yaml` file.

*To run in detached (background) mode:*
```bash
docker-compose up -d
```

4.  Access the API documentation at:
    `http://127.0.0.1:80/docs`

## License 
This project is licensed under the MIT License.

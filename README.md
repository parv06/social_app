# Django Social Application

This is a Django application built with Python 3.10.



## Requirements

- Python 3.10
- Django 4.2.1

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/parv06/social_app.git


```shell cd social_app```
## Create and activate a virtual environment using below commands.
```python3.10 -m venv env``` &
```source env/bin/activate```



Install the required dependencies:

```pip install -r requirements.txt```
## Configure the database settings in the project's settings.py file.

### Apply the database migrations:

python manage.py migrate
Start the development server:

shell
python manage.py runserver
Open your web browser and visit http://localhost:8000/ to access the API.

Use the provided Postman collection to interact with the API endpoints. The collection includes requests for each API endpoint, facilitating faster evaluation.

# Dockerization
### The application can be containerized using Docker. A Dockerfile and docker-compose.yml file are provided to simplify the setup.

To containerize the application with Docker, follow these steps:

Install Docker on your machine.

Build the Docker image:


```docker-compose build```
Start the Docker container:


``` docker-compose up```
The API will be accessible at http://localhost:8000/.


For postmen collection. Please see the root direcotory.

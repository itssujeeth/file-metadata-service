
# Flask Metadata Application

This Flask application retrieves and processes metadata from a GitHub repository, offering two main functionalities: viewing metadata as JSON and downloading metadata as a CSV file. 

## Features

- **View Metadata**: Fetches metadata from configured GitHub repository and displays it as a JSON array.
- **Download Metadata**: Allows downloading the fetched metadata as a CSV file.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.12
- Docker
- Git (for cloning the repository)

### Setting up the codebase

If you did not receive the code base as a zip file, clone it to your local machine:

```bash
git clone https://github.com/itssujeeth/file-metadata-service.git
cd file-metadata-service
```

Install the required Python packages:

```bash
pip install -r requirements.txt -r dev-requirements.txt
```

### Configuration

Configure the application by setting the following environment variables in your `.env` file or directly in your environment:

- `GIT_OWNER`: The owner of the GitHub repository.
- `GIT_REPO`: The name of the GitHub repository.
- `SKIP_HEADER`: (Optional) Whether to skip the CSV header in the download. Defaults to `False`.

### Building the Docker Image

To build the Docker image for the application, run:

```bash
docker build -t file-metadata .
```

### Running the Application

To run the application in a Docker container:

```bash
docker run -p 5000:5000 file-metadata
```

This command runs the Flask application inside a Docker container and makes it accessible at `http://localhost:5000`.  Also, it performs an initial download of the metadata and stores it within the volume as interview.csv.  To download the file into your local folder run the below given command

```bash
docker ps | grep "file"
# This will help you get the running docker container id. Result will look similar to 
# CONTAINER ID   IMAGE                 COMMAND                  CREATED          STATUS          PORTS                    NAMES
# 29d03370caa6   file-metadata:0.0.1   "/app/start_and_down…"   20 minutes ago   Up 20 minutes   0.0.0.0:5000->5000/tcp   jovial_buck
#
# Next run the below command to copy interview.csv to local folder
docker cp <container_id>:/app/interview.csv </path/to/your/local/folder>
```

### Viewing the live results

- To view metadata as JSON, navigate to `http://localhost:5000/metadata` in your web browser or use a tool like `curl`:

  ```bash
  curl http://localhost:5000/metadata
  ```

- To download the metadata as a CSV file, navigate to `http://localhost:5000/metadata/download` in your web browser. The file `interview.csv` will be downloaded to your local system.

## Running tests

To run unit tests make sure coverage is installed and then run the below given commands in the root folder of the cloned repo

```bash
coverage run -m unittest discover

coverage report -m
```

## Deployment

Prod deployment will require following additional steps:
- Update the Flask configuration for production use.
- Use a WSGI server like Gunicorn for running the application.
- Consider using a reverse proxy like Nginx in front of your application for better performance and security.


# CS5600-Project

## Setting up the Docker Container

Install Docker and [verify](https://docs.docker.com/get-started/) that it installed correctly.

`Dockerfile` describes how to assemble the private filesystem for the container. It may also contain metadata describing how to run a container. This file specifies that the image should start from the official [httpd](https://hub.docker.com/_/httpd) image.

Build the Docker image by running `docker build --tag my-apache2 .`.
In the Docker application, you should now see **my-apache2** under 'Images'.

In the root directory of the repository, run the docker image:
`docker run --interactive --detach --tty --name project-web-server --publish 8080:80 my-apache2`.
In the Docker application, a you should now see **project-web-server** under 'Containers/Apps'. This app is an instance of the **my-apache2** image.

With the `--publish` flag, TCP port 80 in the container is mapped to port 8080 on the Docker host. Visit http://localhost:8080 to see the web server.

The container can be stopped with the `docker stop project-web-server` command and removed with the `docker rm project-web-server` command.

## Running the Flask Application

Install `flask` if necessary:

`$ pip install flask`

Simply run the application from the command line:

`$ python server.py`

Navigate to `localhost:5000` in your browser to view the application

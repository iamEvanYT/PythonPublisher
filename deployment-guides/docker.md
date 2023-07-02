## Docker Deployment

You can deploy PythonPublisher using Docker. Follow the steps below to get it running in a Docker container.

### Pre-requisites

- Docker installed on your machine. If not installed, follow the instructions [here](https://docs.docker.com/get-docker/) to install Docker.

### Step 1: Build the Docker image

Use the Dockerfile provided in the repository to build an image. You can do this by running the following command in the root directory of the project:

```
docker build -t pythonpublisher .
```

This command will build a Docker image named `pythonpublisher`.

### Step 2: Run the Docker container

Once the image is built, you can start a container using the following command:

```
docker run -d \
    -v $(pwd)/app/databases:/app/databases \
    -v $(pwd)/app/uploads:/app/uploads \
    -e ADMIN_PASSWORD=<admin_password> \
    -e OPEN_CLOUD_API_KEY=<open_cloud_api_key> \
    -e ROBLOX_COOKIE=<roblox_cookie> \
    -e PORT=<port_number> \
    --name pythonpublisher \
    pythonpublisher
```

In the above command:

- Replace `<admin_password>`, `<open_cloud_api_key>`, `<roblox_cookie>`, and `<port_number>` with your desired values.

- The `-v` flag is used to mount directories from your host to the Docker container. Here, we are mounting the `databases` and `uploads` directories.

- The `-e` flag is used to set environment variables.

- The `--name` flag is used to assign a name to the container. In this case, the container's name is `pythonpublisher`.

Now, your application is running in a Docker container!

### Accessing the application

If you're running Docker locally, you can access your application at http://localhost:<PORT>. If you're running Docker on a remote server, replace "localhost" with the server's IP address.

### Stopping and Removing the Container

To stop the Docker container, you can use the following command:

```
docker stop pythonpublisher
```

To remove the Docker container, you can use the following command:

```
docker rm pythonpublisher
```

Please note that this will not delete the data in your mounted directories.

---

You can replace `<admin_password>`, `<open_cloud_api_key>`, `<roblox_cookie>`, and `<port_number>` with the actual values for your application if you wish, or you can leave them as placeholders for users to fill in. Please adjust the instructions as necessary to match your project's setup and needs.
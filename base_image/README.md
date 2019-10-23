## Build and Push to Docker Hub

To build the base image:
```
$> docker build -t dieple/builder_tools .
$> docker push dieple/builder_tools
```

## Tidy up

Prune images
```
docker image prune -a
```

Prune containers
```
docker container prune
```

# Leo-Liatrio

## local branch

In order to run on local you must have Docker and a Kubernetes manager running on your machine.

Create the image from the Dockerfile:

```sh
docker build -t leo-flask-liatrio:local .
```

Verify with:

```sh
docker images
```

Deploy the containers:

```sh
kubectl apply -f app-deployment.yaml
```

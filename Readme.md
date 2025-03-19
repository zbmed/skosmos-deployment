# Skosmos Deployment

This repository contains the files necessary for deploying skosmos with Kubernetes.
They were obtained using [kompose](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/) 
on the docker compose file of the [Skosmos](https://github.com/NatLibFi/Skosmos) GitHub repository.

### How to deploy

To deploy the backend, run:
```
helm upgrade -i skosmos-backend ./skosmos-backend
```
The backend will be available at `http://skosmos-backend.qa.km.k8s.zbmed.de`.

To deploy the frontend, run:
```
helm upgrade -i skosmos-ui ./skosmos-ui
```
The frontend will be available at `http://skosmos.qa.km.k8s.zbmed.de`.

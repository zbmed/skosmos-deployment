# Skosmos Deployment

This repository contains the files necessary for deploying skosmos with Kubernetes.
They were obtained using [kompose](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/) 
on the docker compose file of the [Skosmos](https://github.com/NatLibFi/Skosmos) GitHub repository.

### How to deploy

1. Apply the `.yaml` files to create Kubernetes resources in your Kubernetes cluster:
   This will create the services `skosmos`, `fuseki` and `fuseki-cache`, each running in a proper container.
    ```bash
    kubectl apply -f skosmos-service.yaml,skosmos-deployment.yaml,skosmos-cm0-configmap.yaml,fuseki-service.yaml,fuseki-deployment.yaml,fuseki-cm0-configmap.yaml,fuseki-cache-service.yaml,fuseki-cache-deployment.yaml,fuseki-cache-cm0-configmap.yaml 
    ```
2. Expose the services `skosmos` and `fuseki` to access them outside the cluster.
   ```bash
   kubectl expose deployment skosmos --type=LoadBalancer --name=skosmos-exposed
   kubectl expose deployment fuseki --type=LoadBalancer --name=fuseki-exposed
   ```
   
3. Obtain the generated external IPs and ports for both services.
   ```bash
   kubectl get services skosmos-exposed
   kubectl get services fuseki-exposed
   ```
   
4. Use the external IP and port of the fuseki-exposed service to load vocabulary into the server.
   Replace `EXTERNAL_IP` and `EXTERNAL_PORT` with the values you obtained in the previous step.
   ```bash
   # load STW vocabulary data
   curl -L -o stw.ttl.zip http://zbw.eu/stw/version/latest/download/stw.ttl.zip
   unzip stw.ttl.zip
   curl -I -X POST -H Content-Type:text/turtle -T stw.ttl -G EXTERNAL_IP:EXTERNAL_PORT/skosmos/data --data-urlencode graph=http://zbw.eu/stw/
   ```

5. Access the frontend in a browser using the external IP you obtained in step 3 for the `skosmos-exposed` service.

# Cleanup
1. Delete the exposing services.
   ```bash
   kubectl delete services fuseki-exposed skosmos-exposed
   ```
2. Delete the resources created with `kubectl apply`.
   ```bash
   kubectl delete -f skosmos-service.yaml,skosmos-deployment.yaml,skosmos-cm0-configmap.yaml,fuseki-service.yaml,fuseki-deployment.yaml,fuseki-cm0-configmap.yaml,fuseki-cache-service.yaml,fuseki-cache-deployment.yaml,fuseki-cache-cm0-configmap.yaml
   ```

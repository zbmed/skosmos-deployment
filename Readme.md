# Skosmos Deployment

This repository contains a helm chart to deploy Skosmos inside a Kubernetes cluster.
The helm chart is based on the procedure to run Skosmos locally with docker from [Skosmos](https://github.com/NatLibFi/Skosmos) GitHub repository.

### How to deploy with https

To deploy the backend, run from the root folder of this repository:
```
helm install <backend-release-name> \
--set-json='backend.image="ghcr.io/zbmed/skosmos/fuseki:5.3.0"' \
skosmos-backend
```

To deploy the frontend, run from the root folder of this repository:
```
helm install <frontend-release-name> \
--set ingress.dns="<frontend-release-name>.qa.km.k8s.zbmed.de" \
--set-json='frontend.image="ghcr.io/zbmed/skosmos/skosmos:latest"' \
--set-json='backend.releaseName="<backend-release-name>"' \
--set-json='ingress.path="/"' \
--set ingress.enableSSL="true" \
--set ingress.certIssuer="letsencrypt-prod" \
skosmos-backend
```

The frontend will be available at `https://<frontend-release-name>.qa.km.k8s.zbmed.de`.

The API will be available at `https://<frontend-release-name>.qa.km.k8s.zbmed.de/rest/v1`

The services can be terminated by running:

```
helm uninstall <name>
```

### How to deploy with http

To deploy both backend and frontend, run from the root folder of this repository:
```
helm install <name> \
--set ingress.dns="<name>.qa.km.k8s.zbmed.de" \
skosmos-backend
```

The frontend will be available at `http://<name>.qa.km.k8s.zbmed.de`.

The API will be available at `http://<name>.qa.km.k8s.zbmed.de/rest/v1`

The services can be terminated by running:

```
helm uninstall <name>
```

### Load Voc4Cat vocabulary

The Voc4Cat vocabulary can be automatically loaded using the helm chart located at `backend-vocab-import/`.
Having an already running Skosmos backend with the name `<name>` (see above), just run (where `<otherName>` can be chosen arbitrarily, but cannot be the same as `<name>`):

```
helm install <otherName> \
--set-json='ingress.backendName="<name>"' \
backend-vocab-import
```

The Voc4Cat vocabulary should now be available.
Afterward, the helm chart can be uninstalled again (even if the Skosmos backend shall continue to run):

```
helm uninstall <otherName>
```

### Activate automatic update of Voc4Cat

The Voc4Cat vocabulary can be automatically updated using the helm chart located at `backend-vocab-update/`.
Having an already running Skosmos backend with the name `<name>` (see above), just run (where `<otherName>` can be chosen arbitrarily, but cannot be the same as `<name>` or any other name that is already used):

```
helm install <otherName> \
--set-json='ingress.backendName="<name>"' \
backend-vocab-update
```

The Voc4Cat vocabulary will now be checked for new releases every day at midnight.

__Note__: Uninstalling the helm chart with `helm uninstall <otherName>` will stop the cronjob being run periodically.

### Load vocabularies manually

Expose the service `<name>-fuseki` created with the helm chart (see above).
```
kubectl expose deployment <name>-fuseki --type=LoadBalancer --name=<name>-fuseki-exposed
```

Obtain the generated external IP. The external IP might be listed as "\<pending\>" at first, as this might take a while.
```
kubectl get services <name>-fuseki-exposed
  ```

Use the external IP and port to load vocabulary into the server.
```
# load STW vocabulary data
curl -L -o stw.ttl.zip http://zbw.eu/stw/version/latest/download/stw.ttl.zip
unzip stw.ttl.zip
curl -I -X POST -H Content-Type:text/turtle -T stw.ttl -G <external_ip>:<port>/skosmos/data --data-urlencode graph=http://zbw.eu/stw/

# load UNESCO vocabulary data
curl -L -o unescothes.ttl http://skos.um.es/unescothes/unescothes.ttl
curl -I -X POST -H Content-Type:text/turtle -T unescothes.ttl -G <external_ip>:<port>/skosmos/data --data-urlencode graph=http://skos.um.es/unescothes/

# load Voc4Cat vocabulary data
curl -o voc4cat.ttl -L -H "accept:application/x-turtle" https://w3id.org/nfdi4cat/voc4cat
curl -I -X POST -H Content-Type:text/turtle -T voc4cat.ttl -G <external_ip>:<port>/skosmos/data --data-urlencode graph=https://w3id.org/nfdi4cat/voc4cat
```
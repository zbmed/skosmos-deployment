# Skosmos Deployment

This repository contains a helm chart to deploy Skosmos inside a Kubernetes cluster.
The helm chart is based on the procedure to run Skosmos locally with docker from [Skosmos](https://github.com/NatLibFi/Skosmos) GitHub repository.

### How to deploy

To deploy both backend and frontend, run from the root folder of this repository:
```
helm install <name>-skosmos \
--set-json='ingress.dns="<name>-skosmos.qa.km.k8s.zbmed.de"' \
skosmos-backend
```

The frontend will be available at `<name>-skosmos.qa.km.k8s.zbmed.de`.

The API will be available at `<name>-skosmos.qa.km.k8s.zbmed.de/rest/v1`

### Load vocabularies

Expose the service `<name>-skosmos-fuseki` created with the helm chart (see above).
```
kubectl expose deployment <name>-skosmos-fuseki --type=LoadBalancer --name=<name>-skosmos-fuseki-exposed
```

Obtain the generated external IP. The external IP might be listed as "<pending>" at first, as this might take a while.
```
kubectl get services <name>-skosmos-fuseki-exposed
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
from bs4 import BeautifulSoup
import urllib.request

data = urllib.request.urlopen('https://nfdi4cat.github.io/voc4cat/latest/voc4cat.xml')

Bs_data = BeautifulSoup(data, "xml")

b_description = Bs_data.find('rdf:Description', {'rdf:about':"https://w3id.org/nfdi4cat/voc4cat_"})

version = b_description.find('owl:versionInfo').text

print(version)
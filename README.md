# agri_geo_rdf_generator

# Overview

This Python script processes a dataset and generates an RDF graph serialized in Turtle format. The script includes integration with the GeoNames API to enrich the data with geographical information. The primary goal is to create an RDF graph that includes detailed metadata about agricultural products price indexes and their related geographical features.

## Dependencies

Before running the script, ensure you have the necessary Python libraries installed:

- **pandas**: For reading and processing the CSV dataset.
- **rdflib**: For constructing and managing the RDF graph.
- **requests**: For making HTTP requests to the GeoNames API.
- **re**: For regular expression operations to extract GeoNames IDs.
- - **geopy**: For simplified access to geocoding services, including GeoNames.

Install these dependencies using `pip`:

```bash
pip install pandas rdflib requests
```


# Script Breakdown

## 1. Importing Libraries

```python
import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD
import requests
import re
```

- **pandas**: Used to load and manipulate the dataset.
- **rdflib**: Provides classes and methods to create and manage the RDF graph.
- **requests**: Handles HTTP requests to the GeoNames API.
- **re**: Python's regular expression library, used here to extract GeoNames IDs from URLs.

## 2. Loading the Dataset

```python
df = pd.read_csv(r'C:\Users\Filipi Soares\Programing\metadata_C4AI-KG.csv')
```

- **df**: The dataset is loaded into a pandas DataFrame from a CSV file located at the specified path.

## 3. Initializing the RDF Graph

```python
g = Graph()
```

- **g**: This is the RDF graph object where all triples (subject-predicate-object relationships) will be stored.

## 4. Defining Namespaces

```python
ALM = Namespace("https://w3id.org/AlmesCore#")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
GN = Namespace("http://www.geonames.org/ontology#")
SDo = Namespace("https://schema.org/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
```

- **Namespaces**: RDF graphs use URIs to identify resources, and namespaces are used to shorten these URIs in the code. For example:
  - **ALM**: Namespace for AlmesCore Metadata Schema.
  - **DCAT**: Namespace for the DCAT vocabulary, which is commonly used to describe datasets.
  - **GN**: Namespace for the GeoNames ontology, used to describe geographical features.
  - **SDo**: Namespace for Schema.org, which is used for general-purpose metadata.
  - **XSD**: XML Schema Definition namespace, used for defining data types like strings, dates, and URIs.

```python
g.bind("alm", ALM)
g.bind("dcat", DCAT)
g.bind("gn", GN)
g.bind("sdo", SDo)
g.bind("xsd", XSD)
```

- **Binding Namespaces**: This binds the namespace prefixes to the RDF graph, making the RDF output more readable by using short prefixes instead of full URIs.

## 5. Extracting GeoNames ID from URLs

```python
def extract_geonames_id(url):
    match = re.search(r'/(\d+)/', url)
    if match:
        return match.group(1)
    return None
```

- **extract_geonames_id**: A helper function that takes a URL (e.g., `https://www.geonames.org/6324358/sao-paulo.html`) and uses a regular expression to extract the GeoNames ID (e.g., `6324358`).

## 6. Fetching GeoNames Data

```python
def get_geonames_name(geonames_id):
    url = f"http://api.geonames.org/getJSON?geonameId={geonames_id}&username=filipisoares"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'name' in data:
            return data['name']
        else:
            print(f"GeoNames ID {geonames_id} did not return a valid name.")
    else:
        print(f"Failed to fetch data for GeoNames ID {geonames_id}. Status code: {response.status_code}")
    return None
```

- **get_geonames_name**: This function takes a GeoNames ID, constructs an API request to GeoNames, and retrieves the name of the geographical feature. It handles errors such as invalid GeoNames IDs or issues with the API request.

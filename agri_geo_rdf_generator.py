pip install pandas
pip install rdflib
pip install requests
pip install geopy

import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD
import requests
import re

# Load the dataset with the correct file path
df = pd.read_csv(r'C:\Users\Filipi Soares\Programing\metadata_C4AI-KG.csv')

# Initialize RDF graph
g = Graph()

# Define namespaces
ALM = Namespace("https://w3id.org/AlmesCore#")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
GN = Namespace("http://www.geonames.org/ontology#")
SDo = Namespace("https://schema.org/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

# Bind namespaces
g.bind("alm", ALM)
g.bind("dcat", DCAT)
g.bind("gn", GN)
g.bind("sdo", SDo)
g.bind("xsd", XSD)

# Function to extract GeoNames ID from the URL
def extract_geonames_id(url):
    match = re.search(r'/(\d+)/', url)
    if match:
        return match.group(1)
    return None

# GeoNames API URL
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

# Iterate over the dataset rows
for index, row in df.iterrows():
    resource = URIRef(f"https://example.org/resource/{row['dct:identifier']}")
    g.add((resource, RDF.type, DCAT.Dataset))
    
    # Mapping standard literals
    g.add((resource, ALM.productGroup, URIRef(row['alm:productgroup'])))
    g.add((resource, ALM.productType, URIRef(row['alm:producttype'])))
    g.add((resource, DCAT.title, Literal(row['dc:title'], datatype=XSD.string)))
    g.add((resource, DCAT.description, Literal(row['dct:description'], datatype=XSD.string)))
    g.add((resource, DCAT.publisher, Literal(row['dc:publisher'], datatype=XSD.string)))
    g.add((resource, DCAT.creator, Literal(row['dc:creator'], datatype=XSD.string)))
    g.add((resource, DCAT.accessURL, URIRef(row['dcat:accessURL'])))
    g.add((resource, ALM.descriptiveStatistics, Literal(row['alm:descriptiveStatistics'], datatype=XSD.string)))
    g.add((resource, DCAT.accrualPeriodicity, Literal(row['dct:accrualPeriodicity'], datatype=XSD.string)))
    g.add((resource, ALM.theme, Literal(row['alm:theme'], datatype=XSD.string)))
    g.add((resource, SDo.referenceQuantity, Literal(row['sdo:referenceQuantity'], datatype=XSD.string)))
    g.add((resource, SDo.startDate, Literal(row['sdo:startDate'], datatype=XSD.date)))
    g.add((resource, SDo.endDate, Literal(row['sdo:endDate'], datatype=XSD.date)))
    g.add((resource, DCAT.license, URIRef(row['dct:license'])))
    g.add((resource, DCAT.rights, Literal(row['dc:rights'], datatype=XSD.string)))
    g.add((resource, ALM.statisticalMethod, URIRef(row['alm:statisticalMethod'])))
    
    # Handling GeoNames location
    location_url = row['sdo:location']
    geonames_id = extract_geonames_id(location_url)
    
    if geonames_id:
        gn_feature = URIRef(f"http://sws.geonames.org/{geonames_id}/")
        gn_name = get_geonames_name(geonames_id)
        
        if gn_name:
            # Add the GeoNames feature node
            g.add((gn_feature, RDF.type, GN.Feature))
            g.add((gn_feature, GN.geonamesID, URIRef(f"http://sws.geonames.org/{geonames_id}/")))
            g.add((gn_feature, GN.name, Literal(gn_name, datatype=XSD.string)))
            
            # Link the resource to the GeoNames feature
            g.add((resource, SDo.location, gn_feature))

# Serialize to Turtle
output_file = r'C:\Users\Filipi Soares\Programing\output_metadata.ttl'
g.serialize(destination=output_file, format='turtle')

print(f"RDF data has been successfully exported to {output_file}")

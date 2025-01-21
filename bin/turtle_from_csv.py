
import argparse
import csv

from rdflib import Graph, Literal, Namespace, RDFS

parser = argparse.ArgumentParser(
    description="Read a wdreconcile CSV create a Turtle file from it.")
parser.add_argument("-i", "--input", required = True,
    help = "Input file (CSV)"
)
args = parser.parse_args()

graph = Graph()
DUCKS = Namespace('https://berlinonline.github.io/jinja-rdf-demo/example/ducks/')
SCHEMA = Namespace('https://schema.org/')
WD = Namespace('http://www.wikidata.org/entity/')

with open(args.input) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        graph.add( (WD[row['id']], SCHEMA.name, Literal(row['label'], lang='en')) )

graph.bind('rdfs', RDFS)
graph.bind('wd', WD)

print(graph.serialize(format='turtle'))
import argparse
import logging
from rdflib import Graph, Namespace

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description="Get labels from Wikidata.")
parser.add_argument('--ducks',
                    help="Path to the Turtle file with our ducks",
                    type=str,
                    )
parser.add_argument('--links',
                    help="Path to the Turtle file with links to Wikidata",
                    type=str,
                    )
args = parser.parse_args()

graph = Graph()
graph.parse(args.ducks)
graph.parse(args.links)

label_graph = Graph()

label_query_template = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>

SELECT ?duck ?label (lang(?label) as ?lang)
WHERE {
    ?duck schema:sameAs ?wikidata_duck .
    SERVICE <https://query.wikidata.org/sparql> {
        ?wikidata_duck rdfs:label ?label
    }
} ORDER BY ?duck ?lang
"""

DUCKS = Namespace('https://berlinonline.github.io/jinja-rdf-demo/example/ducks/')
SCHEMA = Namespace('https://schema.org/')

result_set = graph.query(label_query_template)
for row in result_set:
    LOG.info(f"{row.duck} - {row.label} - {row.lang}")
    label_graph.add( (row.duck, SCHEMA.name, row.label) )

label_graph.bind(prefix='ducks', namespace=DUCKS)
print(label_graph.serialize(format='turtle'))


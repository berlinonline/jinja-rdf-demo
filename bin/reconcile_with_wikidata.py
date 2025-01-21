import argparse
from wdreconcile.reconciler import Reconciler

parser = argparse.ArgumentParser(
    description="Get labels from Wikidata.")
parser.add_argument("-i", "--input", required = True,
    help = "Input file (text, line based)"
)
parser.add_argument("-o", "--output", required = True,
    help = "Output file"
)
args = parser.parse_args()

reconciler = Reconciler(
    in_file = args.input,
    out_file = args.output,
    language = 'en',
    reconciler_type = 'wdsearch',
    limit = 1,
    site = None
)

reconciler.reconcile()
reconciler.save()

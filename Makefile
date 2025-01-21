# Ducks Project

data/ducks/temp:
	mkdir -p data/ducks/temp

## get a list of all duck names for reconciliation with wikidata 
data/ducks/temp/duck_names.csv: data/ducks/temp
	arq --query queries/all_ducks.rq --data data/ducks/ducks.ttl --results=csv > $@

## some names won't work as is, so we need to fix the list a bit
data/ducks/temp/duck_names_fixed.csv: data/ducks/temp/duck_names.csv
	sed "1d" $< | sed "s/Abner Duck/Whitewater Duck/" | sed -E "s/(Dewey|Huey|Louie)/& Duck/" > $@

## get the matching wikidata items using wdreconcile
data/ducks/temp/wikidata_ducks.csv: data/ducks/temp/duck_names_fixed.csv
	python bin/reconcile_with_wikidata.py --input $< --output $@

## revert the name changes from earlier
data/ducks/temp/wikidata_ducks_fixed.csv: data/ducks/temp/wikidata_ducks.csv
	sed -E 's/(Dewey|Huey|Louie) Duck/\1/g' $< | sed -E 's/Whitewater/Abner/g' > $@

## generate a turtle file with wikidata items and labels
data/ducks/temp/wikidata_ducks.ttl: data/ducks/temp/wikidata_ducks_fixed.csv
	python bin/turtle_from_csv.py --input $< > $@

## merge wikidata ducks with our ducks
data/ducks/temp/ducks_merged.ttl: data/ducks/temp/wikidata_ducks.ttl data/ducks/ducks.ttl
	rdfpipe -i turtle $^ > $@

## generate links between our ducks and the wikidata ducks
data/ducks/temp/wikidata_links.ttl: data/ducks/temp/ducks_merged.ttl
	arq --query queries/join_wikidata.rq --data $< > $@

## get duck names in other languages by querying wikidata's SPARQL endpoint
data/ducks/temp/wikidata_labels.ttl: data/ducks/ducks.ttl data/ducks/temp/wikidata_links.ttl
	python bin/get_wikidata_labels.py --ducks $< --links $(word 2,$^) > $@

## finally, merge everything
data/ducks/all.ttl: data/ducks/ducks.ttl data/ducks/temp/wikidata_labels.ttl data/ducks/temp/wikidata_links.ttl
	rdfpipe -i turtle $^ > $@

clean-ducks:
	rm -rf data/ducks/temp

# data/ducks/duck_names_fixed.txt: data/ducks/duck_names.csv


data/all.ttl: data/ducks.ttl data/wikidata_labels.ttl data/wikidata_links.ttl
	rdfpipe -i turtle $^ > $@

generate-ducks:
	python bin/generate.py --config config/ducks.yml

generate-ducks+serve_locally:
	python bin/generate.py --config config/ducks.yml --site_url http://localhost:8000 --serve

_site:
	mkdir _site

data/temp:
	mkdir data/temp

clean:
	rm -rf _site
	rm -rf data/temp




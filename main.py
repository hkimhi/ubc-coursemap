from scrape import scrape
from build_database import build_database
from build_graph import build_graph

scrape(True)
build_database(True)
build_graph()

with open('graph.json') as infile, open('docs/anygraph.json', "w") as outfile:
    outfile.write(infile.read())
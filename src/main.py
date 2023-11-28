from config import *
from scrape import scrape
from fill_postreqs import fill_postreqs
from build_graph import build_graph

# Scrape course data from the UBC website
if IGNORE_CACHE or not FILE_PATH.is_file():
    scrape()

# Compile all courses into one file and fill in prerequisite relationships
if BUILD_DATABASE:
    fill_postreqs()

# Build graph file with course as nodes and pre- and co-requisite relationships as edges
# build_graph()

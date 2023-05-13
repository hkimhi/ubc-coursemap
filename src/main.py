from config import *
from scrape import scrape
from build_database import build_database
from build_graph import build_graph

# Scrape course data from the UBC website
if IGNORE_CACHE:
    scrape()

# Compile all courses into one file and fill in prerequisite relationships
if BUILD_DATABASE:
    build_database()

# Build graph file with course as nodes and pre- and co-requisite relationships as edges
build_graph()

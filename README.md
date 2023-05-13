# UBC Coursemap

This project is intended to facilitate course planning by displaying an interactive graph of all courses at UBC and how they relate to one another by prerequisite, corequisite, and postrequisite relationships.

## Running it locally

To run this project locally, there are a couple of steps involved. Running the `main.py` file will do all of these for you:

1. Get the course data from the UBC website by running `scrape()`. This will store a json file for each course code in the `courses/` directory

2. Compile all courses into one file and fill in the `prereq` field for each course by running `build_database()`. This will create a file called `courses.json` in the working directory.

3. Build the graph in a recognized format using `build_graph()`


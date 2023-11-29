from config import *

import sqlite3
import networkx as nx
import xml.etree.ElementTree as ET

def export_to_gexf():
    # Connect to the SQLite database
    connection = sqlite3.connect(DATABASE_FILE_PATH)
    cursor = connection.cursor()

    # Fetch all courses and their prerequisites from the database
    cursor.execute(f'SELECT name, prereqs FROM {DATABASE_TABLE_NAME}')
    all_courses = cursor.fetchall()

    # Create a directed graph using NetworkX
    graph = nx.DiGraph()

    # Add nodes and edges to the graph
    for course in all_courses:
        course_name, prereqs = course
        prereq_list = prereqs.split(', ') if prereqs else []
        graph.add_node(course_name)
        for prereq in prereq_list:
            if prereq:
                graph.add_edge(prereq, course_name)

    # Write the graph to GEXF format
    nx.write_gexf(graph, GRAPH_FILE_PATH)

    # Close the SQLite connection
    connection.close()

if __name__ == '__main__':
    export_to_gexf()

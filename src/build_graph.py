import json

def build_graph():
    with open("../courses.json", "r") as infile:
        all_courses = json.load(infile)
        nodes = []
        edges = []

        for course in all_courses:
            # Create a node for each course and append it to the nodes list

            course_description = course['desc']
            if 'desc-prereqs' in course:
                course_description += course['desc-prereqs']

            node_dict = {
                'id': course['name'],
                'title': course['title'],
                'credits': course['credits'],
                'desc': course_description,
                'x': course['x'],
                'y': course['y'],
                'group': course['group']
            }
            nodes.append(node_dict)

            # Create a directed edge from each prereq to the current course
            # Then add the edge to the edges list
            for prereq in course['prereqs']:
                edge_dict = {
                    'from': prereq,
                    'to': course['name']
                }
                edges.append(edge_dict)

            # Create a directed edge from each coreq to the current course
            # Then add the edge to the edges list
            for coreq in course['coreqs']:
                edge_dict = {
                    'from': coreq,
                    'to': course['name']
                }
                edges.append(edge_dict)

        # Create graph object
        graph = {"nodes": nodes, "edges": edges}
        # Serializing graph to json
        graph_json = json.dumps(graph, indent=4)
        # Save graph to file
        with open("../graph.json", "w") as outfile:
            outfile.write(graph_json)

    print("Finished building graph!")

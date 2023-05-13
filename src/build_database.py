from config import *
import json
import os

# 1. Load all courses into memory so we can see their preqs
# 2. For each course, add self as a post-req for each of its prereqs
# 3. Compile and save into one large dataset file which will contain every course with:
#       1) name
#       2) description
#       3) prereqs
#       4) coreqs
#       5) postreqs

def build_database():
    outfile_path = os.path.join(os.path.dirname(__file__), '..', 'courses.json')

    # Put all courses into one file, with proper JSON formatting
    with open(outfile_path, "w") as outfile:
        outfile.write('[\n')

        for i in range(len(CODES)):
            code = CODES[i]
            filepath = os.path.join(os.path.dirname(__file__), COURSE_DIRECTORY, f"{code.lower()}.json")
            with open(filepath) as infile:
                text = infile.read()
                # drop the square brackets at the start and end
                text = text[2:len(text)-2]
                if i != len(CODES) - 1:
                    text += ','
                text += '\n'

                outfile.write(text)
        
        outfile.write(']')

    # Go through each course and fill in the post-reqs list for all of its prereqs
    with open(outfile_path) as infile:
        all_courses = json.load(infile)

        for course in all_courses:
            prereqs = course['prereqs']

            for curr_course in all_courses:
                if(curr_course['name'] in prereqs):
                    curr_course['postreqs'].append(course['name'])
        
        # Serializing and writing json
        courses_json = json.dumps(all_courses, indent=4)
        with open(outfile_path, "w") as outfile:
            outfile.write(courses_json)

    print("Finished building database!")

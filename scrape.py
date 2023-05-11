from config import *

from bs4 import BeautifulSoup
from os.path import exists
import requests
import json
import re
import numpy as np

def scrape(IGNORE_CACHE):
    codes_subset = []

    for code in CODES:
        if (IGNORE_CACHE or not exists(FILEPATH.format(code.lower()))):
            codes_subset.append(code)
        else:
            print(f"File already exists for code {code}, skipping.")

    for j in range(len(codes_subset)):
        code = codes_subset[j]
        print(f"Processing {code} courses...")

        filepath = FILEPATH.format(code.lower())

        page = requests.get(BASE_LINK.format(code))
        soup = BeautifulSoup(page.text, 'html.parser')

        # print(soup.prettify())

        # list to hold all course_info dictionaries for a given course code
        all_courses = []

        courses = soup.find_all('article', class_='node--type-course')
        for course in courses:
            course_info = {}

            for elem in course.find('div').children:
                if elem.name == 'h3':
                    # get course name, title, and credits
                    course_info['name'] = elem.get_text()[:8]
                    course_info['title'] = elem.find('strong').get_text()
                    course_info['credits'] = int(elem.get_text()[elem.get_text().find('(') + 1])
                
                elif elem.name == 'p' and 'desc' not in course_info:
                    # first p element, which is the cousre description
                    course_info['desc'] = elem.get_text()
                
                elif elem.name == 'p':
                    # a following p element, so is either prerequisite or corequisite information
                    # add full prerequisite blurb to description for user info
                    if 'desc-prereqs' not in course_info:
                        course_info['desc-prereqs'] = elem.get_text()
                    else:
                        course_info['desc-prereqs'] += '\n' + elem.get_text()


                    # get coreqs
                    if("Corequisite" in elem.text):
                        coreqs = []
                        coreqs = elem.text.split("Corequisite: ")[1].split('.')[0]
                        coreqs = re.findall(r"[A-Z]{3,4} [0-9]{3}", coreqs)
                        course_info['coreqs'] = coreqs
                    
                    # get prereqs
                    if("Prerequisite" in elem.text):
                        prereqs = []
                        prereqs = elem.text.split("Prerequisite: ")[1].split('.')[0]
                        prereqs = re.findall(r"[A-Z]{3,4} [0-9]{3}", prereqs)
                        course_info['prereqs'] = prereqs
                
            if 'prereqs' not in course_info:
                # course did not have any prequisites, set to empty list
                course_info['prereqs'] = []
            
            if 'coreqs' not in course_info:
                # course did not have any corequisites, set to empty list
                course_info['coreqs'] = []

            # set empty postreqs list, will be filled in later
            course_info['postreqs'] = []

            all_courses.append(course_info)

        # add X, Y coordinate and group information for plotting the course as a node on a graph
        num = len(all_courses)
        for i in range(num):
            course_info = all_courses[i]
            R = 100
            L = 600
            course_info['x'] = int(L * np.cos(2*np.pi*j/float(len(CODES))) + R * np.cos(2*np.pi*i / float(num)))
            course_info['y'] = int(L * np.sin(2*np.pi*j/float(len(CODES))) + R * np.sin(2*np.pi*i / float(num)))
            course_info['group'] = code.lower()

        # Serialize course to json
        courses_json = json.dumps(all_courses, indent=4)
        # Save to file
        with open(filepath, "w") as outfile:
            outfile.write(courses_json)

    print("Finished processing!")

if __name__ == '__main__':
    scrape(IGNORE_CACHE)
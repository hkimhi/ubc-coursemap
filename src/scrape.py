from config import *

import sqlite3
from bs4 import BeautifulSoup
import requests
import re
from time import sleep
from pathlib import Path

# Define your database file and table name
FILE_NAME = 'courses.db'
TABLE_NAME = 'courses'
FILEPATH = Path(__file__).parent.parent / FILE_NAME

def scrape():
    # Create SQLite connection and cursor
    connection = sqlite3.connect(FILEPATH)
    cursor = connection.cursor()

    # Create table if it does not exist
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                name TEXT UNIQUE,
                code TEXT,
                title TEXT,
                credits INTEGER,
                desc TEXT,
                desc_prereqs TEXT,
                prereqs TEXT,
                coreqs TEXT,
                postreqs TEXT
                )''')
    
    # Commit table creation
    connection.commit()

    # process each course code from the CODES list
    for j in range(len(CODES)):
        code = CODES[j]
        print(f"Processing {code} courses...")

        # get the UBC page for the given course code
        page = requests.get(BASE_LINK.format(code))
        soup = BeautifulSoup(page.text, 'html.parser')

        courses = soup.find_all('article', class_='node--type-course')
        for course in courses:
            course_info = {'code': code.lower()}

            for elem in course.find('div').children:
                if elem.name == 'h3':
                    # get course name, title, and credits
                    course_info['name'] = elem.get_text()[:8]
                    course_info['title'] = elem.find('strong').get_text()
                    course_info['credits'] = int(elem.get_text()[elem.get_text().find('(') + 1])
                
                elif elem.name == 'p' and 'desc' not in course_info:
                    # first p element, which is the course description
                    course_info['desc'] = elem.get_text()
                
                elif elem.name == 'p':
                    # a following p element, so is either prerequisite or corequisite information
                    # add full prerequisite blurb to description for user info
                    if 'desc_prereqs' not in course_info:
                        course_info['desc_prereqs'] = elem.get_text()
                    else:
                        course_info['desc_prereqs'] += '\n' + elem.get_text()

                    # get coreqs
                    if("Corequisite" in elem.text):
                        coreqs = elem.text.split("Corequisite: ")[1].split('.')[0]
                        coreqs = re.findall(r"[A-Z]{3,4} [0-9]{3}", coreqs)
                        course_info['coreqs'] = coreqs
                    
                    # get prereqs
                    if("Prerequisite" in elem.text):
                        prereqs = elem.text.split("Prerequisite: ")[1].split('.')[0]
                        prereqs = re.findall(r"[A-Z]{3,4} [0-9]{3}", prereqs)
                        course_info['prereqs'] = prereqs
                
            if 'prereqs' not in course_info:
                # course did not have any prequisites, set to empty list
                course_info['prereqs'] = []
                course_info['desc_prereqs'] = ""
            
            if 'coreqs' not in course_info:
                # course did not have any corequisites, set to empty list
                course_info['coreqs'] = []

            # set empty postreqs list, will be filled in later
            course_info['postreqs'] = []

            # Insert course into SQLite table (if it does not already exist)
            cursor.execute(f'''INSERT OR IGNORE INTO {TABLE_NAME} (
                           name, code, title, credits, desc,
                           desc_prereqs, prereqs, coreqs, postreqs
                           ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                           ''', (
                           course_info['name'], course_info['code'], course_info['title'],
                           course_info['credits'], course_info['desc'], course_info['desc_prereqs'],
                           ', '.join(course_info['prereqs']), ', '.join(course_info['coreqs']), ', '.join(course_info['postreqs'])
                           )
            )

        # Commit courses of current code to the database
        connection.commit()

        # I think I was getting rate-limited, so this is not to overload with requests
        sleep(200 / 10000)

    print("Finished processing!")

    # Close the SQLite connection
    connection.close()

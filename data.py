import json

from bs4 import BeautifulSoup
import requests

def download_schedule_html():
    r = requests.get('http://ona13.journalists.org/program/schedule/')

    with open('data/schedule.html', 'wb') as writefile:
        writefile.write(r.content)

def parse_schedule_html():
    with open('data/schedule.html', 'rb') as readfile:
        soup = BeautifulSoup(readfile.read())

    output = []

    for klass in ['make', 'listen', 'solve']:
        for row in soup.select('tr.%s' % klass):
            session_dict = {}

            for index, cell in enumerate(row.select('td')):
                if index == 0:
                    session_dict['start_time'] = cell\
                                                .text\
                                                .split('\n')[0]\
                                                .replace(u'\u2013', '-')\
                                                .split('-')[0]\
                                                .strip()
                    try:
                        session_dict['end_time'] = cell\
                                                    .text\
                                                    .split('\n')[0]\
                                                    .replace(u'\u2013', '-')\
                                                    .split('-')[1]\
                                                    .strip()
                    except IndexError:
                        session_dict['end_time'] = None

                    session_dict['session_type'] = cell.text.split('\n')[1].strip()
                    session_dict['session_section'] = klass

                    if session_dict['end_time']:
                        if 'p.m.' in session_dict['end_time']:
                            if 'a.m.' not in session_dict['start_time']:
                                session_dict['start_time'] = '%s p.m.' % session_dict['start_time']

                if index == 1:

                    session_dict['title'] = cell\
                                            .text\
                                            .split('\n')[0]\
                                            .replace(u'\u2013', '-')\
                                            .replace(u'\u2019', "'")\
                                            .strip()

                    session_dict['leaders'] = []
                    try:
                        for leader in cell.text.split('\n')[1].split('/'):
                            leader_dict = {}
                            leader_dict['name'] = leader.split(', ')[0].strip()
                            leader_dict['organization'] = leader.split(', ')[1].strip()
                            session_dict['leaders'].append(leader_dict)

                    except IndexError:
                    	pass

            output.append(session_dict)

    with open('data/schedule.json', 'wb') as writefile:
    	writefile.write(json.dumps(output))

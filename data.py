import json
import time

from bs4 import BeautifulSoup
from dateutil.parser import *
from pytz import timezone
import requests

def download_schedule_html():
    r = requests.get('http://ona13.journalists.org/program/schedule/')

    with open('data/schedule.html', 'wb') as writefile:
        writefile.write(r.content)

def parse_schedule_html():
    with open('data/schedule.html', 'rb') as readfile:
        soup = BeautifulSoup(readfile.read())

    eastern = timezone('US/Eastern')
    DATES = ['Thursday, October 17', 'Friday, October 18', 'Saturday, October 19']
    output = []

    for klass in ['make', 'listen', 'solve']:

        day_slice = 0
        am = True

        for row in soup.select('tr.%s' % klass):
            session_dict = {}
            session_dict['time'] = {}

            for index, cell in enumerate(row.select('td')):
                if index == 0:
                    session_dict['time']['start_time_string'] = cell\
                                                .text\
                                                .split('\n')[0]\
                                                .replace(u'\u2013', '-')\
                                                .split('-')[0]\
                                                .strip()
                    try:
                        session_dict['time']['end_time_string'] = cell\
                                                    .text\
                                                    .split('\n')[0]\
                                                    .replace(u'\u2013', '-')\
                                                    .split('-')[1]\
                                                    .strip()
                    except IndexError:
                        session_dict['time']['end_time_string'] = None

                    session_dict['session_type'] = cell.text.split('\n')[1].strip()
                    session_dict['session_section'] = klass

                    if session_dict['time']['end_time_string']:
                        if 'p.m.' in session_dict['time']['end_time_string']:
                            if 'a.m.' not in session_dict['time']['start_time_string']:
                                session_dict['time']['start_time_string'] = '%s p.m.' % session_dict['time']['start_time_string']

                        if 'a.m.' in session_dict['time']['end_time_string']:
                            session_dict['time']['start_time_string'] = '%s a.m.' % session_dict['time']['start_time_string']                           

                    session_dict['time']['start_time_string'] = session_dict['time']['start_time_string'].replace('p.m. p.m.', 'a.m.')

                    if 'p.m.' in session_dict['time']['start_time_string']:
                        if am is True:
                            am = False

                    if 'a.m.' in session_dict['time']['start_time_string']:
                        if am is False:
                            am = True
                            day_slice += 1

                    session_dict['time']['date_string'] = DATES[day_slice]

                    session_dict['time']['start_timestamp'] = eastern.localize(
                                                        parse("%s %s" % (
                                                            session_dict['time']['date_string'],
                                                            session_dict['time']['start_time_string']),
                                                        ignoretz=True))
                    session_dict['time']['start_timestamp'] = time.mktime(session_dict['time']['start_timestamp'].timetuple())

                    if session_dict['time']['end_time_string']:

                        if ':' not in session_dict['time']['end_time_string']:
                            if 'p.m.' in session_dict['time']['end_time_string']:
                                session_dict['time']['end_time_string'] = session_dict['time']['end_time_string'].split(' p.m.')[0] + ':00 p.m.'
                            if 'a.m.' in session_dict['time']['end_time_string']:
                                session_dict['time']['end_time_string'] = session_dict['time']['end_time_string'].split(' a.m.')[0] + ':00 a.m.'

                        session_dict['time']['end_timestamp'] = eastern.localize(
                                                            parse("%s %s" % (
                                                                session_dict['time']['date_string'],
                                                                session_dict['time']['end_time_string']),
                                                            ignoretz=True))

                        session_dict['time']['end_timestamp'] = time.mktime(session_dict['time']['end_timestamp'].timetuple())


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

import json
import time

from bs4 import BeautifulSoup
from dateutil.parser import *
from pytz import timezone
import requests

def clean(text, **kwargs):
    """
    Clean is better than dirty.
    Strips bad characters and
    other marks (breaks, etc)
    from text; returns clean.
    """
    BAD_CHARS = [
        (u'\u201c', '"'),
        (u'\u201d', '"'),
        (u'\u2019', "'"),
        (u'\u2014', '--'),
        (u'\u2026', ''),
    ]

    if kwargs.get('breaks', None) != True:
        BAD_CHARS.append((u'\n', ''))
        BAD_CHARS.append((u'\r', ''))

    for bad, good in BAD_CHARS:
        text = text.replace(bad, good)

    return text.strip()

def clean_restaurant_descriptions():
    cleaned = []
    with open('data/restaurants.json', 'rb') as readfile:
        restaurants = json.loads(readfile.read())

    for restaurant in restaurants:
        if restaurant['full_description']:
            if 'Executive chef: ' in restaurant['full_description']:
                restaurant['full_description'] = restaurant['full_description'].split('Executive chef: ')[0]
        cleaned.append(restaurant)

    with open('data/clean_restaurants.json', 'wb') as writefile:
        writefile.write(json.dumps(cleaned))

def parse_restaurant_html():
    ROOT_URL = 'http://entertainment.accessatlanta.com'

    restaurants = []

    for star in [3,4,5]:
        with open('data/%s-stars.html' % star, 'rb') as readfile:
            soup = BeautifulSoup(readfile.read())

        results = soup.select('td.search_result_content')
        for result in results:
            restaurant_dict = {}

            restaurant_dict['stars'] = star
            restaurant_dict['title'] = clean(result.select('td.title_content a')[0].text)
            restaurant_dict['detail_url'] = ROOT_URL + result.select('td.title_content a')[0].attrs['href']
            restaurant_dict['short_description'] = clean(result.select('td.description_content div')[0].text)
            restaurant_dict['address'] = clean(result.select('td.meta_content')[0].text.split('\n\n')[2])
            restaurant_dict['city'] = 'Atlanta'
            restaurant_dict['state'] = 'GA'

            restaurant_dict['phone'] = None
            try:
                if '(' in result.select('td.meta_content')[0].text.split('\n\n')[4]:
                    restaurant_dict['phone'] = clean(result.select('td.meta_content')[0].text.split('\n\n')[4].replace('(', '').replace(') ', '-'))
                elif '(' in result.select('td.meta_content')[0].text.split('\n\n')[3]:
                    restaurant_dict['phone'] = clean(result.select('td.meta_content')[0].text.split('\n\n')[3].replace('(', '').replace(') ', '-'))
                else:
                    pass
            except IndexError:
                pass

            r = requests.get(restaurant_dict['detail_url'])
            soup = BeautifulSoup(r.content)

            try:
                restaurant_dict['full_description'] = clean(soup.select('div.description .excerpt')[0].text, breaks=True) + ' ...'
            except IndexError:
                restaurant_dict['full_description'] = None

            try:
                restaurant_dict['hours'] = soup.select('div.restaurant_data_indent')[0].text.replace('\n\n', '\n')
            except IndexError:
                restaurant_dict['hours'] = None

            restaurants.append(restaurant_dict)

    with open('data/restaurants.json', 'wb') as writefile:
        writefile.write(json.dumps(restaurants))

def download_restaurant_html():
    for star in [3,4,5]:
        r = requests.get('http://entertainment.accessatlanta.com/search?critic_stars=%s&new=n&sort=0&srad=10.0&srss=250&st=restaurant&st_select=restaurant&swhat=&swhen=&swhere=265+Peachtree+Center+Ave+NE+Atlanta+GA+30303' % star)

        with open('data/%s-stars.html' % star, 'wb') as writefile:
            writefile.write(r.content)

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

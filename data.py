import csv
import json
from math import radians, cos, sin, asin, sqrt
import time

from bs4 import BeautifulSoup
from dateutil.parser import *
from geopy import geocoders
from pytz import timezone
import requests


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees).
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    # Convert to KM
    miles = 3961.0 * float(c)

    return miles


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


def get_events_csv():
    r = requests.get('https://docs.google.com/spreadsheet/pub?key=0Any1XR8XqgwLdG8zNm4yeGZQaS1qalJqUjlIMV9fcUE&output=csv')
    with open('data/events.csv', 'wb') as writefile:
        writefile.write(r.content)


def parse_events_csv():
    events = []
    eastern = timezone('US/Eastern')

    with open('data/events.csv', 'rb') as readfile:
        csvreader = csv.DictReader(readfile)

        for event in csvreader:
            event_dict = dict(event)

            event_dict['venue'] = {}
            event_dict['venue']['name'] = event_dict['venue_name']
            event_dict.pop('venue_name')

            event_dict['venue']['address'] = event_dict['venue_address_string']
            event_dict.pop('venue_address_string')

            g = geocoders.GoogleV3()
            places = list(g.geocode(event_dict['venue']['address'], exactly_one=False))

            place, (lat, lng) = places[0]
            event_dict['venue']['lat'] = lat
            event_dict['venue']['lng'] = lng
            event_dict['venue']['geocoded_address'] = place

            event_dict['venue']['distance_from_hotel'] = haversine(
                float(event_dict['venue']['lng']),
                float(event_dict['venue']['lat']),
                -84.385917,
                33.7615262)

            event_dict['timestamp'] = eastern.localize(
                                        parse("%s %s" % (
                                            event_dict['date'],
                                            event_dict['time']),
                                        ignoretz=True))
            event_dict['timestamp'] = time.mktime(event_dict['timestamp'].timetuple())
            event_dict.pop('date')
            event_dict.pop('time')

            time.sleep(0.5)

            distances = []

            with open('data/restaurants.json', 'rb') as readfile:
                restaurants = json.loads(readfile.read())

            for restaurant in restaurants:
                distance_dict = {}
                distance_dict['restaurant'] = dict(restaurant)

                # Loops over every restaurant and calculates the haversine
                # distance between this venue and the restaurant.
                # If a restaurant is within a half mile, we add it to the nearby
                # restaurants list.
                distance_dict['distance'] = haversine(
                    float(event_dict['venue']['lng']),
                    float(event_dict['venue']['lat']),
                    float(restaurant['lng']),
                    float(restaurant['lat']))

                if distance_dict['distance'] < 1.0:
                    distances.append(distance_dict)

            event_dict['nearby_restaurants'] = sorted(distances, key=lambda restaurant: restaurant['distance'])
            event_dict['nearby_restaurants_count'] = len(distances)

            events.append(event_dict)

    with open('data/events.json', 'wb') as writefile:
        writefile.write(json.dumps(events))

def geocode_restaurants():
    """
    Loops over restaurants in the JSON file and geocodes them.
    Writes to a separate file.
    Combine or replace manually.
    """
    geocoded = []
    with open('data/restaurants.json', 'rb') as readfile:
        restaurants = json.loads(readfile.read())

    for restaurant in restaurants:
        g = geocoders.GoogleV3()
        raw_places = list(g.geocode('%s %s %s' % (restaurant['address'], restaurant['city'], 'GA'), exactly_one=False))

        places = []
        for possible_place in raw_places:
            place, (lat, lng) = possible_place
            for city in ['Atlanta, GA', 'Decatur, GA', 'Smyrna, GA', 'Tucker, GA', 'Doraville, GA']:
                if city in place:
                    places.append(possible_place)

        print places
        place, (lat, lng) = places[0]
        restaurant['lat'] = lat
        restaurant['lng'] = lng
        restaurant['geocoded_address'] = place
        geocoded.append(restaurant)
        time.sleep(1)

    with open('data/geocoded_restaurants.json', 'wb') as writefile:
        writefile.write(json.dumps(geocoded))


def clean_restaurant_hours():
    """
    Handles formatting for the restaurant's hours.
    Writes to a separate file.
    Combine or replace manually.
    """
    cleaned = []
    with open('data/restaurants.json', 'rb') as readfile:
        restaurants = json.loads(readfile.read())

    for restaurant in restaurants:
        if restaurant['hours']:
            restaurant['hours'] = restaurant['hours'].strip()
        cleaned.append(restaurant)

    with open('data/clean_restaurants.json', 'wb') as writefile:
        writefile.write(json.dumps(cleaned))


def clean_restaurant_descriptions():
    """
    Handles formatting for restaurant descriptions.
    Writes to a separate file.
    Combine or replace manually.
    """
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
    """
    Read downloaded restaurant HTML from the Access Atlanta search site.
    Writes a JSON file.
    """
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
                restaurant_dict['full_description'] = clean(soup.select('div.description .excerpt')[0].text, breaks=True) + ' ...'.strip()
            except IndexError:
                restaurant_dict['full_description'] = None

            try:
                restaurant_dict['hours'] = soup.select('div.restaurant_data_indent')[0].text.replace('\n\n', '\n').strip()
            except IndexError:
                restaurant_dict['hours'] = None

            restaurants.append(restaurant_dict)

    with open('data/restaurants.json', 'wb') as writefile:
        writefile.write(json.dumps(restaurants))


def download_restaurant_html():
    """
    Downloads restaurant HTML for various classifications of restaurants.
    """
    for star in [3,4,5]:
        r = requests.get('http://entertainment.accessatlanta.com/search?critic_stars=%s&new=n&sort=0&srad=10.0&srss=250&st=restaurant&st_select=restaurant&swhat=&swhen=&swhere=265+Peachtree+Center+Ave+NE+Atlanta+GA+30303' % star)

        with open('data/%s-stars.html' % star, 'wb') as writefile:
            writefile.write(r.content)


def download_schedule_html():
    """
    Downloads the ONA13 schedule.
    """
    r = requests.get('http://ona13.journalists.org/program/schedule/')

    with open('data/schedule.html', 'wb') as writefile:
        writefile.write(r.content)


def parse_schedule_html():
    """
    Parses the downloaded schedule HTML.
    Writes to a JSON file.
    """
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

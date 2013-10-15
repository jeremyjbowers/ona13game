from fabric.api import *

import data

def load_schedule():
    """
    Build the schedule JSON.
    """
    data.download_schedule_html()
    data.parse_schedule_html()


def load_restaurants():
    """
    Build the restaurant JSON.
    """
    data.download_restaurant_html()
    data.parse_restaurant_html()


def geocode_restaurants():
    data.geocode_restaurants()


def load_events():
    data.get_events_csv()
    data.parse_events_csv()
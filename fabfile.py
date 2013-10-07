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

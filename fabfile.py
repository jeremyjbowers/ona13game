from fabric.api import *

import data

def load_schedule():
	data.download_schedule_html()
	data.parse_schedule_html()
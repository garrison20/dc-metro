from adafruit_bitmap_font import bitmap_font

config = {
	#########################
	# Network Configuration #
	#########################

	# WIFI Network SSID
	'wifi_ssid': '<Your 2.4ghz WiFi SSID>',

	# WIFI Password
	'wifi_password': '<Your WiFi Password>',

	#########################
	# Metro Configuration   #
	#########################

	# Metro Station Code
	'metro_station_code': 'D02',

	# Default track to display.
	# Will either show this one first if 'is_single_track' is True, 
	# otherwise it will show both tracks.
	'default_track': '1',

	# Metro Train Group
	'is_single_track': True,

	# This value determines how many times train_board.refresh() needs to be called to switch between track 1 and track 2 if enabled.
	# The wmata api reference at https://developer.wmata.com/docs/services/547636a6f9182302184cda78/operations/547636a6f918230da855363f
	# specifies that "Next train arrival information is refreshed once every 20 to 30 seconds approximately," so just refreshing every 
	# 20 seconds three times per track should be good enough for the board to update 2-3 times per track per minute.
	'double_track_switch_interval': 3,

	# API Key for WMATA
	'metro_api_key': '<Your WMATA API Key>',

	#########################
	# Other Values You      #
	# Probably Shouldn't    #
	# Touch                 #
	#########################
	'metro_api_url': 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/',
	'metro_api_retries': 2,
	'refresh_interval': 20, # Note: 20 second interval is to roughly match WMATA update period, but the processor is also slow

	# Display Settings
	'matrix_width': 64,
	'num_trains': 3,
	'font': bitmap_font.load_font('lib/5x7.bdf'), # characters 5px wide and 7px tall

	# Character height and width must match the font file
	'character_width': 5,
	'character_height': 7,
	'text_padding': 1,
	'text_color': 0xFF7500, # ORANGE

	# Default text loaded for each of the three "train" info lines
	'loading_destination_text': 'Loading',
	'loading_min_text': '---',
	'loading_line_color': 0xFF00FF, # Purple

	'heading_text': 'LN DEST   MIN',
	'heading_color': 0xFF0000, # Red

	'train_line_height': 6,
	'train_line_width': 2,

	'min_label_characters': 3,
	'destination_max_characters': 8,
}

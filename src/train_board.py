import displayio
import time
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label
from adafruit_matrixportal.matrix import Matrix

from config import config

# Enum for clearly defining active track
class Track:
	one = '1'
	two = '2'

# Main display board that holds and updates all the pixels and data based on api data received
class TrainBoard:
	"""
		get_new_data is a function that is expected to return an array of dictionaries like this:

		[
			{
				'line_color': 0xFFFFFF,
				'destination': 'Dest Str',
				'arrival': '5'
			}
		]
	"""
	def __init__(self, get_new_data):
		# FUNCTION CALLBACK FOR metro_api
		self.get_new_data = get_new_data

		# TRACK VARS FOR MAINTAINING TRACK SELECTION STATE
		self.track = Track.one if config['default_track'] == Track.one else Track.two # Starting track if double-track, only track if single-track.
		self.is_single_track = config['is_single_track']
		self.double_track_switch_interval = config['double_track_switch_interval']
		self.refresh_count = 0

		# OBJECT THAT WILL DISPLAY OUR GROUPS
		self.display = Matrix().display

		# GROUP THAT HOLDS OUR OBJECTS (e.g. Rect()'s and Labels()'s)
		self.parent_group = displayio.Group()

		# BUILD THE HEADING LABEL ("LN DEST   MIN")
		self.heading_label = Label(config['font'], anchor_point=(0,0), anchored_position=(0,.5))
		self.heading_label.color = config['heading_color']
		self.heading_label.text=config['heading_text']
		self.parent_group.append(self.heading_label)

		# MAIN LIST THAT HOLDS THE REFERENCE TO OUR THREE SUB-GROUPS OF TRAIN DATA (not an actual displayio.Group(), just a class with data)
		self.trains = []
		for i in range(config['num_trains']):
			self.trains.append(Train(self.parent_group, i))

		# SHOW THE WHOLE BOARD (will default to loading screen on startup)
		self.display.show(self.parent_group)

	def refresh(self) -> bool:
		print('Refreshing train information...')
		# SET THE ACTIVE TRACK
		self._set_curr_track()

		train_data = self.get_new_data(self.track)

		# If we have successfully received our data from wmata,
		# then update train info based on what we received
		if train_data is not None:
			print('Reply received.')
			for i in range(config['num_trains']):
				if i < len(train_data): # Ensure the number of trains we parse doesn't exceed the number of trains we want
					train = train_data[i]
					self._update_train(i, train['line_color'], train['destination'], train['arrival'])
				else:
					self._hide_train(i)

			print('Successfully updated.')
		else:
			print('No data received. Clearing display.')

			for i in range(config['num_trains']):
				self._hide_train(i)

	def _hide_train(self, index: int):
		self.trains[index].hide()

	def _update_train(self, index: int, line_color: int, destination: str, minutes: str):
		self.trains[index].update(line_color, destination, minutes)

	def _set_curr_track(self):
		# JUST RETURN ORIGINAL TRACK IF SINGLE TRACK WAS SET
		if self.is_single_track:
			return self.track

		self.refresh_count += 1
		# UPDATE TRACK IF WE'VE REACHED OUR REFRESH THRESHOLD
		if self.refresh_count >= self.double_track_switch_interval:
			self.track = Track.one if self.track == Track.two else Track.two
			self.refresh_count = 0
			print('Switched active track.')

# Class for holding data that defines a line of train info
class Train:
	def __init__(self, parent_group, index):
		# GET THE Y VALUE OF THE CURRENT TRAIN SECTION
		y = (int)(config['character_height'] + config['text_padding']) * (index + 1)

		# BUILD THE RECT THAT SHOWS THE COLOR COORDINATED WITH THE INCOMING TRAIN
		self.line_rect = Rect(0, y, config['train_line_width'], config['train_line_height'], fill=config['loading_line_color'])

		self.destination_label 			= Label(config['font'], anchor_point=(0,0))
		self.destination_label.x 		= config['train_line_width'] + 2
        # y value is 3 pixels too high for some reason (notice how rect is fine)
        # I suspect this has something to do with the font??
		self.destination_label.y 		= y + 3
		self.destination_label.color 	= config['text_color']
		self.destination_label.text 	= config['loading_destination_text'][:config['destination_max_characters']]

		self.min_label 			= Label(config['font'], anchor_point=(0,0))
		self.min_label.x 		= config['matrix_width'] - (config['min_label_characters'] * config['character_width']) + 1
        # y value is 3 pixels too high for some reason (notice how rect is fine)
        # I suspect this has something to do with the font??
		self.min_label.y 		= y + 3
		self.min_label.color 	= config['text_color']
		self.min_label.text 	= config['loading_min_text']

		self.group = displayio.Group()
		self.group.append(self.line_rect)
		self.group.append(self.destination_label)
		self.group.append(self.min_label)

		parent_group.append(self.group)

	def show(self):
		self.group.hidden = False

	def hide(self):
		self.group.hidden = True

	def set_line_color(self, line_color: int):
		self.line_rect.fill = line_color

	def set_destination(self, destination: str):
		self.destination_label.text = destination[:config['destination_max_characters']]

	def set_arrival_time(self, minutes: str):
		# Ensuring we have a string
		minutes = str(minutes)
		minutes_len = len(minutes)

		# Left-padding the minutes label
		minutes = ' ' * (config['min_label_characters'] - minutes_len) + minutes

		self.min_label.text = minutes

	def update(self, line_color: int, destination: str, minutes: str):
		self.show()
		self.set_line_color(line_color)
		self.set_destination(destination)
		self.set_arrival_time(minutes)

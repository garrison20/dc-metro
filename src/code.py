# DC Metro Board
import time

from config import config
from train_board import TrainBoard
from metro_api import MetroApi, MetroApiOnFireException

STATION_CODE = config['metro_station_code']
REFRESH_INTERVAL = config['refresh_interval']

def refresh_trains(train_group: str) -> [dict]:
	try:
		return MetroApi.fetch_train_predictions(STATION_CODE, train_group)
	except MetroApiOnFireException:
		print('WMATA Api is currently on fire. Trying again later ...')
		return None

train_board = TrainBoard(refresh_trains)

# Main loop
while True:
	train_board.refresh()
	time.sleep(REFRESH_INTERVAL)

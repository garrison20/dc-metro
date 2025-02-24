import board
from adafruit_matrixportal.network import Network

from config import config
from secrets import secrets

# Keeping a global reference for this
_network = Network(status_neopixel=board.NEOPIXEL)

class MetroApiOnFireException(Exception):
    print('Failed to connect to WMATA api.')

class MetroApi:
    def fetch_train_predictions(station_code: str, group: str) -> [dict]:
        return MetroApi._fetch_train_predictions(station_code, group)

    def _fetch_train_predictions(station_code: str, group: str) -> [dict]:
        retry_attempt = 0
        while retry_attempt < config['metro_api_retries']:
            try:
                # Ensure we don't retry failed fetch attempts indefinitely
                retry_attempt += 1

                # Construct URL that will fetch data for our desired station
                api_url = config['metro_api_url'] + station_code
                # Fetch data for our desired station from URL
                train_data = _network.fetch(api_url, headers={
                    'api_key': config['metro_api_key']
                }).json()

                print('Received response from WMATA api...')

                # Filter out train data so only objects for our desired train group are in the list
                trains = filter(lambda t: t['Group'] == group, train_data['Trains'])

                # Convert train objects list to custom list that only has what's needed 
                normalized_results = list(map(MetroApi._normalize_train_response, trains))

                return normalized_results
            except RuntimeError:
                print('Failed to connect to WMATA API. Reattempting...')

        print('Reached maximum number of api connection attempts.')
        raise MetroApiOnFireException()

    def _normalize_train_response(train: dict) -> dict:
        # Take a json object for a single train and extract only the needed data
        line = train['Line']
        destination = train['Destination']
        arrival = train['Min']

        if destination == 'No Passenger' or destination == 'NoPssenger' or destination == 'ssenger':
            destination = 'No Psngr'

        # Return a simplified json object that can be used later for displaying train info
        return {
            'line_color': MetroApi._get_line_color(line),
            'destination': destination,
            'arrival': arrival
        }

    def _get_line_color(line: str) -> int:
        if line == 'RD':
            return 0xFF0000
        elif line == 'OR':
            return 0xFF5500
        elif line == 'YL':
            return 0xFFFF00
        elif line == 'GR':
            return 0x00FF00
        elif line == 'BL':
            return 0x0000FF
        else:
            return 0xAAAAAA

import pandas as pd
import time, datetime

# read in the data
stops = pd.read_csv('data/stop_times.txt')
trips = pd.read_csv('data/trips.txt')
stations = pd.read_csv('data/stops.txt')

# station data
stops = pd.merge(stops, stations, on='stop_id', how="outer")

# do a self join to get connections
stop_table = pd.merge(stops, stops, on='trip_id', how="outer")

# merge in trip data
df = pd.merge(stop_table, trips, on='trip_id', how="outer")

# filters
x = df[df['arrival_time_y'] > df['arrival_time_x']]

table = x[['service_id', 'trip_headsign', 'stop_id_x', 'stop_id_y', 'arrival_time_x', 'arrival_time_y']]

# hardcoded service to day mapping

day_to_service = {
    5: '745A1674',
    6: '746A1674',
}

# mon - fri
DEFAULT_SERVICE = '744A1674'

def times(from_id, to_id):
    """
    Return times for a given trip using the current day
    """

    day = datetime.datetime.today().weekday()
    service_id = day_to_service.get(day, DEFAULT_SERVICE)

    results = table[(table['stop_id_x'] == from_id) & (table['stop_id_y'] == to_id) & (table['service_id'] == service_id)]

    return results.sort('arrival_time_x').to_json(orient='records')

def now():
    """
    Return the current trains approaching stations
    """

    day = datetime.datetime.today().weekday()
    service_id = day_to_service.get(day, DEFAULT_SERVICE)

    results = table[(table['service_id'] == service_id)]

    return results

def to_dict(df):

    return [dict((k, v) for k, v in zip(df.columns, row))
                    for row in df.values]

def clean_up_time(t):
    """
    Convert military time
    """

    try:
        t = time.strptime(t, '%H:%M:%S')
        return time.strftime('%I:%M:%S %p', t)
    except ValueError:
        return None

# exports
stations = to_dict(stations)
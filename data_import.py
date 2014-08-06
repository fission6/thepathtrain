import pandas as pd
import time
# read in the data
stops = pd.read_csv('data/stop_times.txt')
trips = pd.read_csv('data/trips.txt')
stations = pd.read_csv('data/stops.txt')

# do a self join to get connections
stop_table = pd.merge(stops, stops, on='trip_id', how="outer")

# merge in trip data

df = pd.merge(stop_table, trips, on='trip_id', how="outer")

# filters
x = df[df['arrival_time_y'] > df['arrival_time_x']]

table = x[['service_id', 'trip_headsign', 'stop_id_x', 'stop_id_y', 'arrival_time_x', 'arrival_time_y']]

def times(from_id, to_id, service_id):

    results = table[(table['stop_id_x'] == from_id) & (table['stop_id_y'] == to_id) & (table['service_id'] == service_id)]

    return results.sort('arrival_time_x').to_json(orient='records')


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
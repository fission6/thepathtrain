import pandas as pd

stops = pd.read_csv('data/stop_times.txt')

df = pd.merge(stops, stops, on='trip_id', how="outer")

# filters
x = df[df['arrival_time_y'] > df['arrival_time_x']]

table = x[['stop_id_x', 'stop_id_y', 'arrival_time_x', 'arrival_time_y']]

def times(from_id, to_id):

    results = table[(table['stop_id_x'] == from_id) & (table['stop_id_y'] == to_id)]

    return results.sort('arrival_time_x').to_json(orient='records')
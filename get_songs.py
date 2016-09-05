from functions import get_song, get_local_time, insert, get_db_song, daily_songs, create_table, create_db
from datetime import datetime
import csv
import time
import schedule

create_db()
create_table()

def write_log():
    current_date = datetime.now().strftime('%Y-%m-%d')
    i = (current_date+'.csv')
    x = daily_songs(current_date)

    with open(i, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['artists ', 'songs ', 'time'])
        writer.writerows(x)

schedule.every().hour.do(write_log)
rest_url = 'http://www.radio21.ro/track.json'
database_check = get_db_song()

if database_check is None:
    previous_songs = get_song(rest_url)
    previous_song = previous_songs[0]['track']
    previous_song_artist = previous_songs[0]['artist']
    ro_time = get_local_time()
    insert(previous_song_artist, previous_song, ro_time)

song_db = get_db_song()

while True:
    schedule.run_pending()
    time.sleep(60)
    current_songs = get_song(rest_url)
    current_song= current_songs[0]['track']
    current_song_artist = current_songs[0]['artist']

    if current_song != song_db:
        ro_time = get_local_time()
        insert(current_song_artist, current_song, ro_time)
        song_db = current_song
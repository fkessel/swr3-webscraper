import requests
from bs4 import BeautifulSoup as bs
from datetime import date, timedelta
from time import sleep
import json


song_names = []
song_artists = []
song_dates = []
song_clock = []
pages = list(range(0,24))
daterange = []
base_url = "https://www.swr3.de/playlisten/index.html?time"


# https://stackoverflow.com/a/7274316
start_date = date(2021, 1, 15)
end_date = date(2020, 1, 17)
delta = end_date - start_date

for i in range(delta.days + 1):
    day = start_date + timedelta(days=i)
    daterange.append(day.strftime("%Y-%m-%d"))


for date in daterange:
    end_url = f'%3A00&date={date}'

    for page in pages:
        # https://stackoverflow.com/a/134951
        page = f'{base_url}{page:02d}{end_url}'
        r = requests.get(page)
        swr3_soup = bs(r.content, "lxml")
        print(page)
        
        for playlist_item in swr3_soup.find_all("div", class_="list-playlist-item"):
            song = playlist_item.find("dt", string="Titel")
            song_cleaned = song.find_next("dd").get_text()
            song_names.append(song_cleaned)
                        
            artist = playlist_item.find("dt", string="Interpret")
            artist_cleaned = artist.find_next("dd").get_text()
            song_artists.append(artist_cleaned)
                        
            date = playlist_item.find("time")["datetime"]
            first_date = date.split("T")[0]
            second_date = date.split("T")[1]
            song_dates.append(first_date)
            song_clock.append(second_date)

            all_together = {"Künstler": song_artists, "Song": song_names, 
            "Datum": song_dates, "Uhrzeit": song_clock}

            with open("playlist_2021_test.json", "w") as file_playlist:
                json.dump(all_together, file_playlist, indent=2)

    sleep(2)


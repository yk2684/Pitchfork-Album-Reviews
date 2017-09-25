#script to add genre, playcount, listener count, album duration, and number of songs information from lastfm
#to all album reviews scraped from pitchfork

import requests
import json
import pandas as pd
import time

#load in table of album reviews metadata (album name, artist, review date, and rating)
album_table = pd.read_csv('album_reviews.csv')

album_table['artist'] = album_table['artist'].astype(str)
album_table['album'] = album_table['album'].astype(str).map(lambda x: str(x)[:-1])
album_table['release_date'] = album_table['release_date'].map(lambda x: str(x)[6:])

for i in range(0,len(album_table)):
    
    print(i)
    
    #modify artist string for adding into request    
    artist_string = album_table.ix[i]['artist'].replace(" ","+")
    artist_string = artist_string.replace("'","")
    
    #modify album string for adding into request
    album_string = album_table.ix[i]['album'].replace(" ","+")
    album_string = album_string.replace("'","")
    
    #putting together full string to make request
    start_of_string = str("http://ws.audioscrobbler.com/2.0/?method=album.getInfo&api_key=9a8052cdb60a2adf250c5ee28c54ff9f&artist=")
    album_field = str("&album=")
    resp_format = str("&format=json")
    search_string = str(start_of_string+artist_string+album_field+album_string+resp_format)
    
    #try to retrieve album info from last.fm api
    try:
        album = requests.get(search_string)
        j = album.json()

    #if api cannot find album then pass
    except:
        pass

    else:
            
        try:
            #add playcount
            album_table.ix[i, 'Playcount'] = j['album']['playcount']

        except:
            continue

        try:
            #add listeners
            album_table.ix[i, 'Listeners'] = j['album']['listeners']

        except:
            continue

        try:
            #add number of songs and album duration
            Duration = 0
            NumSongs = 0
            for m in range(0,len(j['album']['tracks']['track'])):
                songDuration = int(j['album']['tracks']['track'][m]['duration'])
                Duration = Duration + songDuration
                NumSongs += 1
            album_table.ix[i, 'Duration'] = Duration
            album_table.ix[i, 'NumSongs'] = NumSongs

        except:
            continue
        
        try:
            #add first five genres listed for album
            for k in range(0,max(5,len(j['album']['tags']['tag']))):
                colname = str('Genre'+str(k+1))
                album_table.ix[i, colname] = j['album']['tags']['tag'][k]['name']
        
        except:
            continue
    
    time.sleep(0.3)

#save revised CSV with album information from lastfm
album_table.to_csv("reviews.csv")
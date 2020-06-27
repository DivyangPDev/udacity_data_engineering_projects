# # DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""create table if not exists songplays
(songplay_id SERIAL PRIMARY KEY, 
start_time bigint,
user_id int NOT NULL,
song_id varchar,
artist_id varchar,
session_id int,
location varchar,
user_agent varchar)
""")

user_table_create = ("""create table if not exists users
(user_id int PRIMARY KEY,
first_name varchar,
last_name varchar,
gender varchar,
level varchar)
""")

song_table_create = ("""create table if not exists songs
(song_id varchar PRIMARY KEY,
title varchar,
artist_id varchar NOT NULL,
year int,
duration bigint)
""")

artist_table_create = ("""create table if not exists artists
(artist_id varchar PRIMARY KEY,
name varchar,
location varchar,
latitude decimal,
longitude decimal)
""")

time_table_create = ("""create table if not exists time
(start_time bigint,
hour int,
day int,
week int,
month int,
year int,
weekday int)
""")

# INSERT RECORDS

songplay_table_insert = (""" insert into songplays
(start_time,
user_id,
song_id,
artist_id,
session_id,
location,
user_agent) values(%s,%s,%s,%s,%s,%s,%s)
""")

user_table_insert = ("""insert into users
(user_id,
first_name,
last_name,
gender,
level) values(%s,%s,%s,%s,%s)
ON CONFLICT (user_id) 
DO NOTHING;
""")

song_table_insert = ("""insert into songs
(song_id,
title,
artist_id,
year,
duration) values(%s,%s,%s,%s,%s)
""")

artist_table_insert = ("""insert into artists
(artist_id,
name,
location,
latitude,
longitude) values(%s,%s,%s,%s,%s)
ON CONFLICT (artist_id) 
DO NOTHING;
""")


time_table_insert = ("""insert into time
(start_time,
hour,
day,
week,
month,
year,
weekday) values(%s,%s,%s,%s,%s,%s,%s)
""")

# FIND SONGS

song_select = ("""select s.song_id, s.artist_id from songs s, artists a where 
s.artist_id = a.artist_id 
and s.title = %s 
and a.name = %s 
and s.duration=%s 
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "drop table if exists stg_events;"
staging_songs_table_drop = "drop table if exists stg_songs;"
songplay_table_drop = "drop table if exists songplay;"
user_table_drop = "drop table if exists users;"
song_table_drop = "drop table if exists songs;"
artist_table_drop = "drop table if exists artists;"
time_table_drop = "drop table if exists time;"

# CREATE TABLES

staging_events_table_create= ("""create table stg_events(
artist varchar,
auth varchar,
first_name varchar,
gender varchar,
item_in_session integer,
last_name varchar,
length float,
level varchar,
location varchar,
method varchar,
page varchar,
registration float,
session_id integer,
song varchar,
status integer,
ts timestamp,
user_agent varchar,
user_id integer
) diststyle even;
""")

staging_songs_table_create = ("""create table stg_songs(
num_songs integer
,artist_id varchar
,artist_latitude float
,artist_longitude float
,artist_location varchar
,artist_name varchar
,song_id varchar
,title varchar
,duration float
,year int
)
diststyle even;
""")

songplay_table_create = ("""
CREATE table if not exists songplays
(songplay_id integer primary key
,start_time timestamp not null sortkey
, user_id integer not null
, level varchar
, song_id varchar not null
, artist_id varchar not null
, session_id integer
, location varchar
, user_agent varchar)
diststyle even;
""")

user_table_create = ("""CREATE table if not exists users
(user_id int sortkey primary key
, first_name varchar not null
, last_name varchar not null
, gender varchar not null
, level varchar not null)
diststyle all;
""")

song_table_create = ("""CREATE table if not exists songs
(song_id varchar sortkey primary key
, title varchar not null
, artist_id varchar not null
, year integer not null
, duration float)
diststyle all;
""")

artist_table_create = ("""CREATE table if not exists artists
(artist_id varchar sortkey primary key
, name varchar not null
, location varchar
, latitude float
, longitude float )
diststyle all;
""")

time_table_create = ("""CREATE table if not exists time
(start_time timestamp sortkey primary key
, hour integer not null
, day  integer not null
, week  integer not null
, month  integer not null
, year  integer not null
, weekday varchar not null)
diststyle all;
""")

# STAGING TABLES

staging_events_copy = ("""copy stg_events
from {}
iam_role {}
format as JSON {}
region 'us-west-2'
timeformat as 'epochmillisecs';
""").format(config["S3"]["LOG_DATA"], config["IAM_ROLE"]["ARN"], config["S3"]["LOG_JSONPATH"])

staging_songs_copy = ("""copy stg_songs
from {}
iam_role {}
region 'us-west-2'
format as JSON 'auto'
truncatecolumns ;
""").format(config["S3"]["SONG_DATA"], config["IAM_ROLE"]["ARN"])

# FINAL TABLES

songplay_table_insert = ("""Insert into songplays(songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) (
select  distinct(e.ts)  AS start_time,
            e.user_id
            e.level
            s.song_id
            s.artist_id
            e.session_id
            e.location
            e.user_agent
    FROM stg_events e
    JOIN stg_songs s on (e.song = s.title AND e.artist = s.artist_name);
""")

user_table_insert = ("""Insert into users(user_id, first_name, last_name, gender, level) (
select distinct(user_id)
    ,first_name
    ,last_name
    ,gender
    ,level
    from stg_events
    where user_id is not null );
""")

song_table_insert = ("""Insert into songs(song_id , title , artist_id , year , duration ) (
select distinct(song_id)
    , title
    , artist_id
    , year
    , duration
    from stg_songs
    where song_id is not null);
""")

artist_table_insert = ("""Insert into artists(artist_id, name, location, latitude, longitude) (
select distinct(artist_id)
    , name
    , location
    , latitude
    , longitude
    from stg_songs
    where artist_id is not null)
""")

time_table_insert = ("""Insert into time(start_time, hour, day, week, month, year, weekday) (
select start_time
    extract(hour from start_time) hour,
    extract(day from start_time) day,
    extract(week from start_time) week,
    extract(month from start_time) month,
    extract(year from start_time) year,
    extract(dayofweek from start_time) weekday
from songplays );
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

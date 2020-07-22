## Project AIM: To build an ETL pipeline for a database hosted on Redshift.

## Project Description
A music streaming startup, Sparkify, has grown the user base and 
song database and want to move their processes and data onto the 
cloud. Their data resides in S3, in a directory of JSON logs on
user activity on the app, as well as a directory with JSON metadata
on the songs in their app.

Built an ETL pipeline that extracts their data from S3, stages them 
in Redshift, and transforms data into a set of dimensional tables 
for their analytics team to continue finding insights in what songs 
their users are listening to

### ETL Design

Idea is to load the logs files from s3 and the streaming data from 
s3 to stanging tables

from the staging tables move the relevent filtered and processed 
data into the respective facts and dimention tables.

### Schema Design

Fact table
songplays - records in log data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

Dimentions table
users - users in the app
user_id, first_name, last_name, gender, level

songs - songs in music database
song_id, title, artist_id, year, duration

artists - artists in music database
artist_id, name, location, latitude, longitude

time - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday

Staging table

stg_events
    dumping event log files from s3 directly in this table
stg_songs
    dumping songs files from s3 directly in this table
    
### List of scripts

sql_queries.py - includes (CRUD) queries
create_tables.py - Resets the database by droppoing and recreating the tables
etl.py - loads the json files for songs and logs dataset from the s3 folder on the db in the staging table and then insert into
fact and dimension tables.




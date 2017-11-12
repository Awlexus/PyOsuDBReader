# PyOsuDBReader
Little python library to read the different .db-files from osu 

# Requirements
* Python 3.5+

# Usage
There are three Classes. Each of them is designed to read from a different database:
* [CollectionsDbReader](https://github.com/Awlexus/PyOsuDBReader/blob/master/pyosudbreader.py#L109) - Read collections from **_collection.db_**. 
* [OsuDbReader](https://github.com/Awlexus/PyOsuDBReader/blob/master/pyosudbreader.py#L145) - Read Beatmaps from **_osu!.db_**. 
* [ScoreDbReader](https://github.com/Awlexus/PyOsuDBReader/blob/master/pyosudbreader.py#L316) - Read Scores from **_scores.db_**. 

By default each reader looks up the default osu! folder-for your OS, meaning that you don't have to provide a path to the databasefile, unless you have a custom installation folder. The readers follow the [wiki specifications for .db-files](https://osu.ppy.sh/help/wiki/osu!_File_Formats/Db_%28file_format%29). 

## CollectionsDbReader
### Attributes
Detailed version: [osu wiki](https://osu.ppy.sh/help/wiki/osu!_File_Formats/Db_%28file_format%29#collection.db)
* Version
* Number of collections
* List of collections

### functions
* read_collection - reads one collection. The collection will be returned as well as added to the list of collections
* read_all_collections - reads the rest of the collections and returns the list of collections

## OsuDbReader
### Attributes
Detailed version: [osu wiki](https://osu.ppy.sh/help/wiki/osu!_File_Formats/Db_%28file_format%29#osu!.db-format)
* Version
* Folder count
* Account unlocked
* Date the account will be unlocked
* Player name
* Number of beatmaps
* List of beatmaps

### functions
* read_beatmap - reads one beatmap. The beatmap will be returned as well as added to the list of beatmaps
* read_all_beatmaps - reads the rest of the beatmaps and returns the list of beatmaps


## ScoreDbReader
### Attributes
Detailed version: [osu wiki](https://osu.ppy.sh/help/wiki/osu!_File_Formats/Db_%28file_format%29#scores.db)
* Version
* Number of beatmaps with scores
* List of beatmaps with scores 

### functions
* read_score - reads one beatmap and it's associated scores. The beatmap will be returned as well as added to the list of beatmaps
* read_all_scores - reads the rest of the beatmaps and returns the list of beatmaps

## Note
Each reader should be treated as a resource and be closed after usage.<br>
Example using with:
```python
with ScoreDbReader() as db:
  # Do reading here
  db.read_all_beatmaps()

# Do work here
for beatmap in db.beatmaps:
  ...
```


# License
A copy of the license can be found [here](https://github.com/Awlexus/PyOsuDBReader/blob/master/LICENSE)

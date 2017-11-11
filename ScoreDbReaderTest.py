from pyosudbreader import ScoreDbReader
import pprint

db_reader = ScoreDbReader()

print('''
Version: %i
Number of Beatmaps: %i''' % (db_reader.version, db_reader.num_maps))
print('First Beatmap:')
pprint.pprint(db_reader.read_beatmap())

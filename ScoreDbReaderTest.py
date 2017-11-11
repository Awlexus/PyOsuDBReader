from pyosudbreader import ScoreDbReader
import pprint

with ScoreDbReader() as db:
    beatmaps = db.read_all_beatmaps()
    print('''
    Version: %i
    Number of Beatmaps: %i
    Number of Beatmaps found %i''' % (db.version, db.num_beatmaps, len(beatmaps)))
    print('First Beatmap:')
    pprint.pprint(beatmaps[0])

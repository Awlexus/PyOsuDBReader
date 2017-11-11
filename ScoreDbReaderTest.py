import pprint

from .pyosudbreader import ScoreDbReader

with ScoreDbReader() as db:
    beatmaps = db.read_all_beatmaps()
    print(
        'Version: %i\n'
        'Number of Beatmaps: %i\n'
        'Number of Beatmaps found %i\n' % (db.version, db.num_beatmaps, len(beatmaps)))
    print('First Beatmap:')
    pprint.pprint(beatmaps[0])

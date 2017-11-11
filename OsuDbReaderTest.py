from pyosudbreader import OsuDbReader
import pprint

with OsuDbReader() as db:
    beatmaps = db.read_all_beatmaps()
    print('''
       version: %i
       folder_count: %i
       unlocked: %s
       date_unlocked: %s
       player: %s
       number of beatmaps: %i
       number of beatmaps found: %i''' % (db.version, db.folder_count, db.unlocked, db.date_unlocked, db.player,
                                          db.num_beatmaps, len(beatmaps)))
    print('First Beatmap:')
    pprint.pprint(beatmaps[0])

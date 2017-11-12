import pprint

from pyosudbreader import OsuDbReader

with OsuDbReader() as db:
    db.read_all_beatmaps()
    print(
        'version: %i\n'
        'folder_count: %i\n'
        'unlocked: %s\n'
        'date_unlocked: %s\n'
        'player: %s\n'
        'number of beatmaps: %i\n'
        'number of beatmaps found: %i' % (db.version, db.folder_count, db.unlocked, db.date_unlocked, db.player,
                                          db.num_beatmaps, len(db.beatmaps)))
    print('First Beatmap:')
    pprint.pprint(db.beatmaps[0])

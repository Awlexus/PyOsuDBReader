import pprint

from .pyosudbreader import CollectionsDbReader

with CollectionsDbReader() as db:
    collections = db.read_all_collections()
    print('Version: %i\n'
          'Number of Collections: %i\n'
          'Number of Collections found: %i' % (db.version, db.num_collections, len(collections)))
    print('First collection:')
    pprint.pprint(collections[0])

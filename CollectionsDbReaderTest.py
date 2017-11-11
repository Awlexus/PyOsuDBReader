from pyosudbreader import CollectionsDbReader
import pprint

with CollectionsDbReader() as db:
    collections = db.read_all_collections()
    print('''
    Version: %i
    Number of Collections: %i
    Number of Collections found: %i''' % (db.version, db.num_collections, len(collections)))
    print('First collection:')
    pprint.pprint(collections[0])

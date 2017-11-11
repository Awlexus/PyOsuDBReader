from pyosudbreader import CollectionsDbReader
import pprint

db_reader = CollectionsDbReader()

print('''
Version: %i
Number of Collections: %i''' % (db_reader.version, db_reader.num_collections))
print('First collection:')
pprint.pprint(db_reader.read_collection())

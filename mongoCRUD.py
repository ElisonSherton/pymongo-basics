"""
This script aims to demonstrate basic CRUD commands in pymongo
"""

import json
from pymongo import MongoClient

with open("spotifyTop50.json", "r") as f:
    spotifyTop50 = json.load(f)
    f.close()

# Create a mongo connection
client = MongoClient("mongodb://localhost:27017/")

# Have a look at all the databases in the client connection
print(client.list_database_names())

# Have a look at all the collection names in all the databases in client connection
for item in client.list_database_names():
    tempDB = client[item]
    print(f'Database: {item:<20}, Collections: {tempDB.list_collection_names()}')

# Create a database
db = client["spotifyData"]

# Create a collection
coll = db["Top50"]

#----------------------------- Create document in a collection ---------------------------#
# Create a single document in the collection
one_document = spotifyTop50[0]
coll.insert_one(one_document)

# Create many documents in the collection (excluding first one since it's already created)
all_records = spotifyTop50[1:]
coll.insert_many(all_records)

#----------------------------- Read/Query from a collection -----------------------------#
# Find all the documents sung by Taylor Swift
taySwiftrecs = coll.find({"Artist Name": "Taylor Swift"})
for recs in taySwiftrecs:
    print(recs)

# Find all the documents which are highly popular (popularity > 90)
pop90recs = coll.find({"Popularity": {"$gte": 90}})
for recs in pop90recs:
    print(recs)

# Find all the documents which belong to the pop genre
popSongs = coll.find({"Genre": {"$regex": "pop$"}})
for recs in popSongs:
    print(recs)

#----------------------------- Update Items in a collection -----------------------------#
# Update the popularity scale for all documents between 1-5 from 1-100
allSongs = coll.update_many({},
                            {"$mul": {"Popularity": 0.05}})
for recs in coll.find():
    print(recs)

# Update the name of Ed Sheeran to his nickname Teddy in all the Ed Sheeran tracks
result = coll.update_many({"Artist Name": "Ed Sheeran"},
                          {"$set": {"Artist Name": "Teddy"}},
                          upsert = False)

print(f"Matched: {result.matched_count}, Modified: {result.modified_count}.")

#----------------------------- Delete documents from a collection -----------------------#
# Delete all the songs sung by Drake from the collection
result = coll.delete_many({"Artist Name": "Drake"})
print(f"Deleted: {result.deleted_count}")

# Delete all the songs having popularity less than 4
result = coll.delete_many({"Popularity": {"$lt": 4.0}})
print(f"Deleted: {result.deleted_count}")

#----------------------------- Delete collections from a database -----------------------#

# Drop collection with reference
coll.drop()
# Drop collection from database with name
db.drop_collection("Top50")

#----------------------------- Delete database from a mongoDB server --------------------#

# Drop database from a mongodb server
client.drop_database("spotifyData")

# Close the connection responsibly
client.close()
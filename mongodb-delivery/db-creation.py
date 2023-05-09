from pymongo import MongoClient
from bson import ObjectId
import uuid
import json

client = MongoClient('mongodb://localhost:27017/')
db = client["bibliographyDB"]
papersCollection = db["papers"]

papers_id = {} # maps cited papers titles to ObjectID, used to create manual reference for citatons
data = json.load(open('mongodb-delivery/mongodb-documents-no-text.json')) # remove no-text for mongodb

for paper in data:
  id = ObjectId(uuid.uuid4().hex[:24])
  papers_id[paper["title"]] = id
  paper["year"] = int(paper["year"])

for paper in data:
  paper["_id"] = papers_id[paper["title"]]
  citations = []
  for cited_paper in paper["citations"]:
    citations.append(papers_id[cited_paper])
  paper["citations"] = citations  
  papersCollection.insert_one(paper)
  
print("DB and collection created")
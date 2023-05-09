# Returns the name of the author with the most number of publications

db.papers.aggregate([ 
  { "$unwind": { "path": "$authors" } }, 
  { "$group": { "_id": "$authors.name", "count": { "$sum": 1} } },
  { "$sort": {"count": -1 }},
  { "$limit": 1 }
])
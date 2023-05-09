# Authors with at least two publications

db.papers.aggregate([ 
  { "$unwind": { "path": "$authors" } }, 
  { "$group": { "_id": "$authors.name", "count": { "$sum": 1} } },
  { "$match": { "count": { "$gte": 2 }}}
])
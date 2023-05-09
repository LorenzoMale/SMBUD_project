db.papers.updateOne(
   { _id: ObjectId("637ba64b2dd099d0e47dfb83") },
   { $push: { authors: { 
      name: "Author2", 
      email: "author2@mail.com",
      bio: "Sample Bio 2",
      affiliations: "University",
      birth_year: 1985
    } } }
)
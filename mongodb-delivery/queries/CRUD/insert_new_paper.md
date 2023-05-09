db.papers.insertOne({ 
  authors: [ 
    { 
      name: "Author", 
      email: "author@mail.com",
      bio: "Sample Bio",
      affiliations: "University",
      birth_year: 1980
    }
  ],
  title: "Title",
  year: 2022,
  type: "article",
  abstract: "Sample abstract",
  documentBody: [
  {
    chapter: {
      title: "Chapter title",
      sections: [
        { section: {
            title: "Section title",
            paragraphs: [
              {
                text: "Sample text"
              }
            ],
            figures: [
              {
                url: "url",
                caption: "caption"
              }
            ]
          }
        },      
      ]
    }
  }],
  citations: [],
  keywords: [ "keyword" ]
})

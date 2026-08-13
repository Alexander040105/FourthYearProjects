// Switch to or create the database namespace
use juanmart_data_lake 

// Create the raw landing collection explicitly
db.createCollection("rawLanding")

// Insert a first document so the database/collection definitely exist
db.rawLanding.insertOne({
  source: "landing",
  createdAt: new Date(),
  status: "new"
})

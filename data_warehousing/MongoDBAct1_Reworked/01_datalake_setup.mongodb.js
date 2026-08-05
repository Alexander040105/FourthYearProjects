// Switch to the JuanMart Data Lake namespace
use juanmart_data_lake;

// Create the raw checkout landing collection as a capped collection.
// Capped collections keep the landing zone bounded while still accepting
// unvalidated, schemaless raw JSON payloads.
db.createCollection("raw_checkout_landing", {
    capped: true,
    size: 52428800,   // 50 MB
    max: 50000        // maximum number of documents
});

// Indexing patterns for downstream extraction and audit queries.
db.raw_checkout_landing.createIndex({ source: 1 });
db.raw_checkout_landing.createIndex({ eventType: 1 });
db.raw_checkout_landing.createIndex({ ingestedAt: -1 });
db.raw_checkout_landing.createIndex({ source: 1, eventType: 1 });
db.raw_checkout_landing.createIndex({ source: 1, ingestedAt: -1 });
db.raw_checkout_landing.createIndex({ eventType: 1, ingestedAt: -1 });

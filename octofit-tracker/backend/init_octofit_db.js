const { MongoClient } = require('mongodb');

async function initDb() {
	const uri = 'mongodb://localhost:27017';
	const client = new MongoClient(uri);

	try {
		await client.connect();
		const db = client.db('octofit_db');

		await db.createCollection("users");
		await db.createCollection("teams");
		await db.createCollection("activity");
		await db.createCollection("leaderboard");
		await db.createCollection("workouts");

		await db.collection("users").createIndex({ "email": 1 }, { unique: true });
		console.log("Database initialized successfully.");
	} catch (err) {
		console.error("Error initializing database:", err);
	} finally {
		await client.close();
	}
}

initDb();

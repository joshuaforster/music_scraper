import express from "express";
import { pool } from "./db/pool.js";
import { router } from "./routes/genres.js";
const app = express();
app.use(express.json());
app.use(router);
app.get("/db-test", async (req, res) => {
    const result = await pool.query("SELECT COUNT(*) FROM events;");
    res.json(result.rows[0]);
});
app.get("/", (req, res) => {
    res.send("API running");
});
export default app;

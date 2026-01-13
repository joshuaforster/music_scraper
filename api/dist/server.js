import "dotenv/config";
import app from "./app.js";
const PORT = process.env.PORT ?? 3000;
console.log("DATABASE_URL:", process.env.DATABASE_URL);
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

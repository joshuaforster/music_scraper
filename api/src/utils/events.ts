import { pool } from "../db/pool.js";

export async function getEventsByGenre(genre: string) {
  const result = await pool.query(
    `
    SELECT
      events.id,
      events.title,
      events.event_datetime,
      events.genre,
      events.price_text,
      events.min_price,
      events.max_price,
      events.booking_url,
      venues.name AS venue_name
    FROM events
    JOIN venues ON venues.id = events.venue_id
    WHERE
      events.event_datetime > NOW()
      AND events.genre ILIKE $1
    ORDER BY events.event_datetime ASC
    `,
    [`%${genre}%`]
  );

  return result.rows;
}

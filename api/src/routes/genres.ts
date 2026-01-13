import { Request, Response, Router } from "express";
import { getEventsByGenre } from "../utils/events.js";
import { transporter } from "../emails/transporter.js";
import { pool } from "../db/pool.js";

export const router = Router();

async function getMusicByGenre(genre: string) {
  return getEventsByGenre(genre)
}



router.get("/events", async (req, res) => {

const worldMusic = await getMusicByGenre("World")

const jazzMusic = await getMusicByGenre("Jazz")

const sentRows = await pool.query("SELECT booking_url FROM emailed_events")
const alreadySent = new Set(sentRows.rows.map(r => r.booking_url))


const seen = new Set<string>()

const sections = [
  {
    title: "Jazz",
    events: jazzMusic,
  },
  {
    title: "World",
    events: worldMusic,
  }
]

const emailSections = sections.map(section => {
  const uniqueEvents: any[] = []

  for (const event of section.events) {
    if (seen.has(event.booking_url)) continue
    if (alreadySent.has(event.booking_url)) continue

    seen.add(event.booking_url)
    uniqueEvents.push(event)
}

  return {
    title: section.title,
    events: uniqueEvents.map(event => ({
        title: event.title,
        date: event.event_datetime,
        genre: event.genre,
        venue: "Norwich Arts Centre",
        price: event.price_text || `${event.min_price}–${event.max_price}`,
        booking_url: event.booking_url
    }))
  }
})

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("en-GB", {
    weekday: "short",
    day: "numeric",
    month: "short"
  })
}


const htmlBody = `
<div style="font-family: Arial, Helvetica, sans-serif; background:#f6f6f6; padding:24px;">
  <div style="max-width:600px; margin:auto; background:white; padding:24px; border-radius:8px;">
    
    <h1 style="margin-top:0; color:#111;">
      🎶 Today’s New Live Music Listings
    </h1>

    <p style="color:#555; line-height:1.5;">
      I’ve put this together by automatically checking the Norwich Arts Centre listings and grouping the best upcoming gigs by genre, so you don’t have to.
    </p>

    ${emailSections.map(section => {
      const events = section.events.map(event => `
        <div style="border-left:4px solid #111; padding-left:12px; margin-bottom:16px;">
          <div style="font-size:16px; font-weight:bold; color:#111;">
            ${event.title}
          </div>
          <div style="color:#555; margin:4px 0;">
            ${formatDate(event.date)} at ${event.venue}
          </div>
          <div style="color:#555;">
            ${event.price}
          </div>
          <a href="${event.booking_url}" style="display:inline-block; margin-top:6px; color:#2563eb; text-decoration:none;">
            Book tickets →
          </a>
        </div>
      `).join("")

      return `
        <h2 style="margin-top:32px; border-bottom:1px solid #ddd; padding-bottom:4px;">
          ${section.title}
        </h2>
        ${events}
      `
    }).join("")}

    <p style="font-size:12px; color:#888; margin-top:32px;">
      All events are taken from the venue’s public website. Please double-check the booking links for the latest info.
    </p>

  </div>
</div>
`
const totalEvents = emailSections.reduce(
  (sum, section) => sum + section.events.length,
  0
)

if (totalEvents === 0) {
  return res.json({ success: true, message: "No new events to email" })
}
  await transporter.sendMail({
    to: ["joshuaforster95@gmail.com", "holly.hipwell@hotmail.com", "joshdevelops@icloud.com"],   
    subject: "This week’s Norwich live music",
    html: htmlBody
  })

  for (const section of emailSections) {
  for (const event of section.events) {
    await pool.query(
      "INSERT INTO emailed_events (booking_url) VALUES ($1) ON CONFLICT DO NOTHING",
      [event.booking_url]
    )
  }
}


  res.json({ success: true })
})
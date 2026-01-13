import nodemailer from "nodemailer";

console.log("EMAILPASS exists:", Boolean(process.env.EMAILPASS))

export const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: "joshuaforster95@gmail.com",
    pass: process.env.EMAILPASS
  }
});

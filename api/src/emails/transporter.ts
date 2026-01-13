import nodemailer from "nodemailer";

export const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: "joshuaforster95@gmail.com",
    pass: process.env.EMAILPASS
  }
});

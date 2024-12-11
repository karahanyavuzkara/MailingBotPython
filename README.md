# Bulk Email Sender

A Python script for sending bulk emails with rate limiting and batch processing capabilities.

## Features
- CSV contact list processing
- Rate limiting to avoid email server restrictions
- Batch processing with configurable delays
- Error handling and retry options

## Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your email configuration:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_app_password
   ```
4. Prepare your CSV file with columns: name, surname, email

## Usage
1. Place your contacts CSV file in the project directory
2. Run the script:
   ```bash
   python app.py
   ```

## CSV Format
The CSV file should have the following columns:
- name
- surname
- email

## Security Note
- Never commit your `.env` file or CSV files containing personal data
- Use Gmail App Passwords instead of your main account password 
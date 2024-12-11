import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Email configuration from environment variables
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Validate configuration
if not all([SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD]):
    raise ValueError("Missing required environment variables. Please check your .env file.")

def read_contacts(csv_file):
    """Read contacts from CSV file"""
    try:
        df = pd.read_csv(csv_file)
        print(f"Successfully read CSV file with {len(df)} rows")
        print("Columns found:", df.columns.tolist())
        return df
    except pd.errors.EmptyDataError:
        print(f"The CSV file '{csv_file}' is empty or has no valid data")
        raise
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        raise

def send_email(recipient_email, name, surname):
    """Send email to a single recipient"""
    # Create message
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = "YOUR E-MAIL SUBJECT"


    # Create email body
    body = f"""
    Your mail body and text.! 🚀
    """
    
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Create SMTP session
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, recipient_email, text)
        print(f"Successfully sent email to {name} {surname} ({recipient_email})")
        
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email to {recipient_email}. Error: {str(e)}")
        return False

def main():
    csv_file = "mailingbes.csv"
    print(f"Attempting to read {csv_file}...")
    
    try:
        # Read contacts with explicit header row

        contacts = pd.read_csv(csv_file, encoding='utf-8', names=['name', 'surname', 'email'])
        total = len(contacts)
        print(f"\nFound {total} contacts")
        
        # Confirm before sending
        print("\nReady to send emails. Press Enter to continue or Ctrl+C to cancel...")
        input()
        
        # Send emails with rate limiting
        emails_sent = 0
        batch_size = 50  # Send 50 emails per batch
        delay_between_emails = 2  # 2 seconds between emails
        delay_between_batches = 100  # 5 minutes between batches
        
        for index, row in contacts.iterrows():
            current = index + 1
            recipient_email = row['email'].strip()
            name = row['name'].strip()
            surname = row['surname'].strip()
            
            # Check if we need a batch delay
            if emails_sent > 0 and emails_sent % batch_size == 0:
                print(f"\n>>> Pausing for {delay_between_batches} seconds to avoid rate limits...")
                print(f">>> Sent {emails_sent}/{total} emails so far")
                print(f">>> Current time: {datetime.now().strftime('%H:%M:%S')}")
                time.sleep(delay_between_batches)
            
            print(f"\nProcessing {current}/{total}: {name} {surname} ({recipient_email})")
            
            try:
                send_email(recipient_email, name, surname)
                emails_sent += 1
                time.sleep(delay_between_emails)  # Wait between emails
                
            except Exception as e:
                print(f"Error sending to {recipient_email}: {str(e)}")
                retry = input("Retry this email? (y/n): ").lower()
                if retry == 'y':
                    try:
                        send_email(recipient_email, name, surname)
                        emails_sent += 1
                    except Exception as e:
                        print(f"Failed on retry: {str(e)}")
                continue
            
        print(f"\nCompleted! Sent {emails_sent} out of {total} emails")
            
    except KeyboardInterrupt:
        print("\nProcess stopped by user")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

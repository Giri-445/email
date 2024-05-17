import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Function to load recipient data from CSV
def load_recipients(file):
    return pd.read_csv(file)

# Function to personalize the email content
def personalize_email(name, preference):
    subject = f"Hello {name}, check out our latest {preference}!"
    body = f"Dear {name},\n\nWe have some exciting {preference} just for you.\n\nBest Regards,\nYour Company"
    return subject, body

# Function to send the email
def send_email(sender_email, sender_password, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        return f"Email sent to {recipient_email}"
    except Exception as e:
        return f"Failed to send email to {recipient_email}. Error: {str(e)}"

# Streamlit App
st.title("Personalized Email Sender")

# Step 1: Email credentials
st.header("Step 1: Enter Your Email Credentials")
sender_email = st.text_input("Sender Email")
sender_password = st.text_input("Sender Password", type="password")

# Step 2: Upload recipient CSV file
st.header("Step 2: Upload Recipient CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    recipients = load_recipients(uploaded_file)
    st.write("Recipient Data Preview")
    st.dataframe(recipients)

    # Step 3: Send Emails
    if st.button("Send Emails"):
        if sender_email and sender_password:
            status_messages = []
            for index, row in recipients.iterrows():
                name = row['name']
                email = row['email']
                preference = row['preference']
                
                subject, body = personalize_email(name, preference)
                status = send_email(sender_email, sender_password, email, subject, body)
                status_messages.append(status)
            
            st.write("Email Sending Status")
            for message in status_messages:
                st.write(message)
        else:
            st.warning("Please enter your email credentials.")

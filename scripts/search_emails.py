import imaplib
import email
from email.header import decode_header
import os

def search_emails():
    username = "oasisaisolutions@gmail.com"
    password = "audbdlvkwphlluia"
    imap_server = "imap.gmail.com"

    # Connect to the server
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, password)

    # Search in all folders
    status, messages = imap.select("INBOX")
    if status != "OK":
        print("Could not select INBOX")
        return

    # Search for "PropFlow"
    status, message_ids = imap.search(None, 'BODY "PropFlow"')
    if status == "OK":
        ids = message_ids[0].split()
        print(f"Found {len(ids)} emails with 'PropFlow'")
        for i in ids[-5:]: # Last 5
            res, msg = imap.fetch(i, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    print(f"Subject: {subject}")
                    print(f"To: {msg['To']}")
                    print(f"From: {msg['From']}")
                    print("-" * 20)

    # Search for "Pazit"
    print("\nSearching for 'Pazit'...")
    status, message_ids = imap.search(None, 'BODY "Pazit"')
    if status == "OK":
        ids = message_ids[0].split()
        print(f"Found {len(ids)} emails with 'Pazit'")
        for i in ids:
            res, msg = imap.fetch(i, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    print(f"Subject: {subject}")
                    print(f"To: {msg['To']}")
                    print(f"From: {msg['From']}")
                    print("-" * 20)

    imap.close()
    imap.logout()

if __name__ == "__main__":
    search_emails()

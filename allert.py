import requests
import hashlib
import time
import tkinter as tk
from tkinter import messagebox

# URL of the website to monitor
url = "https://www.resmigazete.gov.tr/ilanlar/eskiilanlar/2024/09/20240906-4.htm"

# File to store the last hash value
hash_file = 'last_hash.txt'

# Interval between checks (in seconds)
interval = 300

def get_page_hash(url):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    page_content = response.text
    return hashlib.sha256(page_content.encode('utf-8')).hexdigest()

def load_last_hash(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_current_hash(file_path, hash_value):
    with open(file_path, 'w') as f:
        f.write(hash_value)

def send_alert(message):
    # Create a Tkinter root window (it will be hidden)
    root = tk.Tk()
    root.withdraw()
    # Show a popup message
    messagebox.showwarning("Website Update Alert", message)
    # Optionally, you can destroy the root window after showing the popup
    root.destroy()

def monitor_website(url, hash_file, interval):
    print("Monitoring started. Checking for changes every {} seconds.".format(interval))
    while True:
        try:
            current_hash = get_page_hash(url)
            last_hash = load_last_hash(hash_file)
            
            if last_hash is None:
                print("Initial check. No previous hash found.")
                save_current_hash(hash_file, current_hash)
            elif current_hash != last_hash:
                send_alert("Website has been updated!")
                save_current_hash(hash_file, current_hash)
            else:
                print("No changes detected.")
        
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(interval)

if __name__ == "__main__":
    monitor_website(url, hash_file, interval)

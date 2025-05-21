import tkinter as tk
import requests
import json
from datetime import datetime
from hijri_converter import Hijri  # Fallback library

class HijriDateApp:
    def __init__(self):
        self.api_key = "API_KEY=YOUR_API_KEY_HERE" #Configuration  Get a free API key at [Calendarific](https://calendarific.com/)
        self.country = "SA"
        self.setup_ui()
        self.fetch_date()

    def setup_ui(self):
        """Create the application window"""
        self.root = tk.Tk()
        self.root.title("Hijri Date")
        self.root.geometry("350x120")
        self.root.configure(bg='#1a1a1a')
        
        # Main date display
        self.date_label = tk.Label(
            self.root,
            text="Loading date...",
            font=('Segoe UI', 14),
            fg='white',
            bg='#1a1a1a',
            pady=10
        )
        self.date_label.pack()
        
        # Status message
        self.status_label = tk.Label(
            self.root,
            text="",
            font=('Segoe UI', 8),
            fg='#aaaaaa',
            bg='#1a1a1a'
        )
        self.status_label.pack()
        
        # Refresh button
        self.refresh_btn = tk.Button(
            self.root,
            text="Refresh",
            command=self.fetch_date,
            bg='#333333',
            fg='white'
        )
        self.refresh_btn.pack(pady=5)

    def fetch_date(self):
        """Try to get date from API, fallback to local calculation"""
        try:
            # Try API first
            self.status_label.config(text="Connecting to API...")
            self.root.update()  # Force UI update
            
            url = f"https://calendarific.com/api/v2/holidays?api_key={self.api_key}&country={self.country}&year={datetime.now().year}&type=islamic"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            if data['meta']['code'] == 200:
                hijri_date = data['response']['holidays'][0]['date']['hijri']
                day, month, year = hijri_date.split('-')
                month_names = [
                    "Muḥarram", "Ṣafar", "Rabīʿ al-Awwal", "Rabīʿ al-Thānī",
                    "Jumādá al-Ūlá", "Jumādá al-Ākhirah", "Rajab", "Shaʿbān",
                    "Ramaḍān", "Shawwāl", "Dhū al-Qaʿdah", "Dhū al-Ḥijjah"
                ]
                self.date_label.config(text=f"{day} {month_names[int(month)-1]} {year} AH")
                self.status_label.config(text="Live API data", fg='green')
                return
                
        except Exception as api_error:
            # Fallback to local calculation if API fails
            try:
                self.status_label.config(text="API failed, using local calculation...", fg='orange')
                today = Hijri.today()
                self.date_label.config(text=f"{today.day} {today.month_name()} {today.year} AH")
                self.status_label.config(text="", fg='orange')
            except Exception as local_error:
                self.date_label.config(text="Date unavailable")
                self.status_label.config(text=f"Error: {str(local_error)}", fg='red')

if __name__ == "__main__":
    try:
        # Install required packages automatically
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "hijri-converter"])
        
        app = HijriDateApp()
        app.root.mainloop()
    except Exception as e:
        print(f"Critical error: {e}")
        input("Press Enter to close...")
import requests
import json
from flask import Flask, render_template
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from urllib.parse import quote

app = Flask(__name__)

@app.route("/")
def show_games():

    # set the date to today's date:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    # 1. Define the API URL

    url = f"https://api.sportsblaze.com/wnba/v1/schedule/daily/{today}.json?key=sb1d4svo6l0foz1sdnberho"

    try:
        # 2. Make the GET request
        response = requests.get(url)

        # 3. Check for successful response
        if response.status_code == 200:
            # 4. Parse JSON, pull out games

            data = response.json()
            games = data.get("games", [])

            output = ""
            for game in games:

                # date handing 
                iso_date = game["date"] # e.g., "2025-07-25T19:30:00Z"
                try:
                    # Remove the trailing 'Z' because it's served in Eastern time, not UTC
                    if iso_date.endswith('Z'):
                        iso_date = iso_date[:-1]
                    # Parse as naive datetime, then attach Eastern tz
                    dt_eastern = datetime.fromisoformat(iso_date).replace(tzinfo=ZoneInfo("America/New_York"))
                    #Conver to Central Time
                    dt_central = dt_eastern.astimezone(ZoneInfo("America/Chicago"))
                    #format date
                    game["readable_date"] = dt_central.strftime("%B %d, %Y, %-I:%M %p")
                except Exception as e:
                    print(f"Failed to parse date: {iso_date}. Reason: {e}")
                    game["readable_date"] = "Date unavailable"

                # score handling
                try:
                    home_score = game["scores"]["home"]
                    away_score = game["scores"]["away"]
                    game["score_display"] = f"{away_score} - {home_score}"
                except Exception as e:
                    game["score_display"] = "Score not available"

                home_team = game["teams"]["home"]["name"]
                away_team = game["teams"]["away"]["name"]
                date = game["readable_date"]
                venue = game["venue"]["name"]

                output += f"{away_team} at {home_team} - {venue} on {date} <br>"
            
            # 5. Return/render something displaying games
            return render_template("games.html", games=games)
        else:
            # Handle the error: show error message
            return "There was an error - sorry!"
    except Exception as e:
        # Handle exceptions
        return f"There was an error: {e}"
    
    







# def jprint(obj):  
#     text = json.dumps(obj, sort_keys=True, indent=4) 
#     print(text) 

# jprint(response.json())
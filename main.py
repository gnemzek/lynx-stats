import requests
import json
from flask import Flask, render_template
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from urllib.parse import quote

app = Flask(__name__)

def get_lynx_players():
    try:
        season = 2025
        api_key = "sb1d4svo6l0foz1sdnberho"
        # Fetch Lynx roster for the season
        roster_url = f"https://api.sportsblaze.com/wnba/v1/rosters/{season}.json?key={api_key}&team=Minnesota%20Lynx"
        roster_response = requests.get(roster_url)
        lynx_player_ids = set()
        headshot_map = {}
        if roster_response.status_code == 200:
            roster_data = roster_response.json()
            if roster_data.get("teams"):
                for player in roster_data["teams"][0].get("roster", []):
                    headshot_map[player["id"]] = player.get("headshot")
        else:
            print("Error fetching roster:", roster_response.status_code)
            return []

        # Now fetch all player split stats
        stats_url = (
            f"https://api.sportsblaze.com/wnba/v1/splits/players/{season}/regular_season.json"
            f"?key={api_key}&stats=average_points"
        )
        stats_response = requests.get(stats_url)
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            all_players = stats_data.get("players", [])
            lynx_players = [p for p in all_players if p.get("id") in headshot_map]
            lynx_players.sort(key=lambda p: p["stats"]["average"].get("points", 0), reverse=True)
            top_lynx_players = lynx_players[:6]
            for player in top_lynx_players:
                player["headshot"] = headshot_map.get(player["id"])
            return top_lynx_players
        else:
            print("Error fetching split stats:", stats_response.status_code)
            return []
    except Exception as e:
        print("Error fetching leaderboard:", e)
        return []

def get_recent_games(num=5):
    season = 2025
    url = f"https://api.sportsblaze.com/wnba/v1/schedule/season/{season}.json?key=sb1d4svo6l0foz1sdnberho"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        all_games = data.get("games", [])

        # Get only games with a 'Final' status, sort descending by date
        recent_games = [
            game for game in all_games
            if game.get("status") == "Final"
        ]
        # Sort by date, newest first
        recent_games.sort(key=lambda g: g["date"], reverse=True)
        # Take the last 3 (or whatever number you want)
        recent_games = recent_games[:num]

        for game in recent_games:
            # Format the date for display
            iso_date = game.get("date", "")
            try:
                if iso_date.endswith('Z'):
                    iso_date = iso_date[:-1]
                dt_eastern = datetime.fromisoformat(iso_date).replace(tzinfo=ZoneInfo("America/New_York"))
                dt_central = dt_eastern.astimezone(ZoneInfo("America/Chicago"))
                game["readable_date"] = dt_central.strftime("%B %d, %Y, %-I:%M %p")
            except Exception:
                game["readable_date"] = "Date unavailable"
            
            # Format the score for display
            try:
                home_score = game["scores"]["total"]["home"]["points"]
                away_score = game["scores"]["total"]["away"]["points"]
                game["score_display"] = f"{away_score} - {home_score}"
            except Exception:
                game["score_display"] = "Score not available"
        return recent_games
    else:
        # Handle the error: show error message
        print("data is:", data)
        return "There was an error - sorry!"

@app.route("/")
def show_games():

    # set the date to today's date:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    # Define the API URL

    url = f"https://api.sportsblaze.com/wnba/v1/schedule/daily/{today}.json?key=sb1d4svo6l0foz1sdnberho"

    try:
        # Make the GET request
        response = requests.get(url)

        # Check for successful response
        if response.status_code == 200:
            # Parse JSON, pull out games

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
                    home_score = game["scores"]["total"]["home"]["points"]
                    away_score = game["scores"]["total"]["away"]["points"]
                    game["score_display"] = f"{away_score} - {home_score}"
                except Exception as e:
                    game["score_display"] = "Score not available"

                home_team = game["teams"]["home"]["name"]
                away_team = game["teams"]["away"]["name"]
                date = game["readable_date"]
                venue = game["venue"]["name"]

                output += f"{away_team} at {home_team} - {venue} on {date} <br>"
            
            # Return/render something displaying games
            recent_games = get_recent_games(num=5)
            lynx_players = get_lynx_players()
            return render_template("games.html", games=games, recent_games=recent_games, lynx_players=lynx_players)
        else:
            # Handle the error: show error message
            return "There was an error - sorry!"
    except Exception as e:
        # Handle exceptions
        return f"There was an error: {e}"
    
@app.route("/players/<player_id>")
def player_gamelog(player_id):
    # Fetch gamelogs for this player from the API
    season = 2025
    api_key = "sb1d4svo6l0foz1sdnberho"
    url = f"https://api.sportsblaze.com/wnba/v1/gamelogs/players/{season}/{player_id}.json?key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data.keys())
        print(data.get("results"))
        print(data.get("total"))
        player = data.get("player", {})
        games = data.get("games", [])
        return render_template("player_gamelog.html", player=player, games=games)
    else:
        return f"Could not fetch gamelog for this player (status {response.status_code})"

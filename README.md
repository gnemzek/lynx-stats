# wnba-stats
A project built for the Boot.dev Hackathon Weekend. The main goal of this project is to gather important information about upcoming WNBA games, adding those games to your personal calendar, seeing top players from the upcoming games, etc. This is a project meant for casual WNBA fans who would like some extra info. 

## Setup Instructions
1. Clone the repository
2. Create and activate a virtual environment
  -  ``` python3 -m venv venv
  source venv/bin/activate  # On Linux/Mac
  # or
  venv\Scripts\activate     # On Windows ```
3. Install dependencies
  - ``` pip install -r requirements.txt ```
4. Set the Flask app environment variable
_(Flask needs to know your entry file; here it’s main.py.)_
  ``` export FLASK_APP=main.py      # On Linux/Mac
# or
set FLASK_APP=main.py         # On Windows ```
5. (Recommended) Enable debug mode for development
  ``` export FLASK_ENV=development  # On Linux/Mac
# or
set FLASK_ENV=development     # On Windows ```
6.  Run the Flask development server
  - ``` flask run ```
7. Open your browser and navigate to
``` http://localhost:5000/ ``` 



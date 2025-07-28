# Lynx Stats
A project built for the Boot.dev Hackathon Weekend. The main goal of this project is to gather important information about upcoming WNBA games, seeing the top Lynx players and the full roster, and dialing down into individual player stats. This is a project meant for casual WNBA fans who would like some extra info. 

## Demo
For a live demo (so you don't have to get your own API key and set it up locally) please see: [https://lynx-stats.onrender.com/](https://lynx-stats.onrender.com/). (This might take up to a minute to load depending on when the last render was.)

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/gnemzek/lynx-stats.git
    cd your-repo-name
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/Mac
    # or
    venv\Scripts\activate     # On Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set the Flask app environment variable  
   _(Flask needs to know your entry file; here it’s `main.py`.)_
    ```bash
    export FLASK_APP=main.py      # On Linux/Mac
    # or
    set FLASK_APP=main.py         # On Windows
    ```

5. (Recommended) Enable debug mode for development:
    ```bash
    export FLASK_ENV=development  # On Linux/Mac
    # or
    set FLASK_ENV=development     # On Windows
    ```

6. Run the Flask development server:
    ```bash
    flask run
    ```

7. Open your browser and navigate to  
   [http://localhost:5000/](http://localhost:5000/)


## Limitations

Due to API limitations:
- All games do not appear in the inidivdual players' gamelog pages. 
- API does not update as frequently as scores do - this is not a project for seeing realtime score updates. 
- Recent games may not be up-to-date because of frequency of API updates. 



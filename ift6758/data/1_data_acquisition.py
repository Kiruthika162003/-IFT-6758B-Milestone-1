
from google.colab import drive
drive.mount('/content/drive')

import os
import requests
import json

# Cache directory inside Google Drive
CACHE_DIR = "/content/drive/MyDrive/NHL_Datas/raw"

def fetch_and_cache_nhl_data(season, game_type, game_number, cache_dir=CACHE_DIR):
    """
    Fetch and cache NHL play-by-play data for a given game.

    Args:
        season (int): Starting year of the NHL season (e.g., 2016 for 2016-17 season).
        game_type (str): '02' for regular season, '03' for playoffs.
        game_number (str): Game number padded to 4 digits (e.g., '0001').
        cache_dir (str): Directory to store cached data.

    Returns:
        dict: JSON data of the play-by-play or None if not found.
    """
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    game_id = f"{season}{game_type}{game_number}"
    cache_file = os.path.join(cache_dir, f"{game_id}.json")

    if os.path.exists(cache_file):
        print(f"Loading cached data for Game ID {game_id}.")
        with open(cache_file, 'r') as f:
            return json.load(f)

    url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play"
    try:
        print(f"Fetching data for Game ID {game_id}...")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        save_data_to_file(data, cache_file)
        return data
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(f"Game ID {game_id} not found (404). Skipping.")
        else:
            print(f"HTTP Error: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
    return None

def save_data_to_file(data, file_path):
    """
    Save JSON data to a file.

    Args:
        data (dict): JSON data to be saved.
        file_path (str): Path to save the data.
    """
    with open(file_path, 'w') as f:
        json.dump(data, f)
    print(f"Data saved to {file_path}")

def download_season_data(season, game_type="02", max_games=1300):
    """
    Download all play-by-play data for a season.

    Args:
        season (int): The starting year of the season (e.g., 2016 for 2016-17).
        game_type (str): '02' for regular season, '03' for playoffs.
        max_games (int): Maximum games to download (1300 to cover all games).
    """
    for game_number in range(1, max_games + 1):
        game_number_str = str(game_number).zfill(4)
        data = fetch_and_cache_nhl_data(season, game_type, game_number_str)
        if not data:
            break  # Stop if a game ID is not found (end of season)

def download_all_seasons(start_year=2016, end_year=2023):
    """
    Download play-by-play data for all seasons from start_year to end_year.

    Args:
        start_year (int): The first season to download (e.g., 2016).
        end_year (int): The last season to download (e.g., 2023).
    """
    for year in range(start_year, end_year + 1):
        print(f"\nDownloading regular season data for {year}-{year + 1}...")
        download_season_data(year, "02")

        print(f"\nDownloading playoff data for {year}-{year + 1}...")
        download_season_data(year, "03")

# Example: Download all data from 2016-17 to 2023-24
download_all_seasons(2016, 2024)

#  print thethe json file for Game ID 2024021300

from google.colab import drive
import os
import requests
import json

# Mount Google Drive
drive.mount('/content/drive')


# Cache directory inside Google Drive
CACHE_DIR = "/content/drive/MyDrive/NHL_Datas/raw"

def print_json_content(season, game_type, game_number, cache_dir=CACHE_DIR):
  """
  Prints the content of a JSON file.
  """
  game_id = f"{season}{game_type}{game_number}"
  cache_file = os.path.join(cache_dir, f"{game_id}.json")

  if os.path.exists(cache_file):
    print(f"Printing the content inside the json file Fetching data for Game ID {game_id}")
    with open(cache_file, 'r') as f:
      try:
        data = json.load(f)
        print(json.dumps(data, indent=2))  # Print with indentation for better readability
      except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
  else:
    print(f"File not found: {cache_file}")



# Example: Print the content of the JSON file for game ID 2024021300
print_json_content(2024, "02", "1300")


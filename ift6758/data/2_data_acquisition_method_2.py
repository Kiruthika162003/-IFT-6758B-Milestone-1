

import os
import requests
import json

def fetch_nhl_play_by_play_data(season, game_type, game_number):
    """
    Fetch NHL play-by-play data for a given game in a season.

    Args:
        season (int): The starting year of the NHL season (e.g., 2016 for the 2016-17 season).
        game_type (str): The type of game (e.g., "01" for preseason, "02" for regular, "03" for playoffs).
        game_number (str): The specific game number, padded appropriately.

    Returns:
        dict: JSON data of the play-by-play for the specified game, or None if not found.
    """
    game_id = f"{season}{game_type}{game_number}"
    url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (e.g., 404)
        data = response.json()
        return data
    except requests.exceptions.HTTPError as errh:
        if response.status_code == 404:
            print(f"Game ID {game_id} not found (404). Skipping.")
        else:
            print("HTTP Error:", errh)
    except requests.exceptions.RequestException as err:
        print("Request Error:", err)
        return None


def save_data_to_file(data, file_path):
    """
    Save fetched data to a JSON file.

    Args:
        data (dict): The JSON data to save.
        file_path (str): The file path to save the data to.
    """
    if data:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {file_path}")
    else:
        print("No data to save.")


def download_and_cache_nhl_data(season_start_year, game_type, game_range):
    """
    Download and save NHL play-by-play data for a given season and game type.

    Args:
        season_start_year (int): The starting year of the season (e.g., 2016 for the 2016-17 season).
        game_type (str): The type of game ("01" for preseason, "02" for regular, "03" for playoffs, "04" for all-star).
        game_range (range): The range of games to download.
    """
    season = f"{season_start_year + 1}"  # Format the season part of the game ID
    data_folder = os.getenv("NHL_DATA_FOLDER", "./nhl_data")  # Default to local folder if env variable not set
    os.makedirs(data_folder, exist_ok=True)

    for game_num in game_range:
        if game_type == "03":  # Special formatting for playoff games
            game_id_str = f"0{str(game_num).zfill(3)}"  # Pad with a leading zero, followed by 3 digits (e.g., "0001" -> "00001")
        else:
            game_id_str = str(game_num).zfill(4)  # Zero-pad game number to 4 digits

        file_path = os.path.join(data_folder, f"game_{season}_{game_type}_{game_id_str}.json")

        # Check if data already exists locally
        if os.path.exists(file_path):
            print(f"Data already exists for game {season}-{game_type}-{game_id_str}. Skipping download.")
            continue

#use a loop to download from 2016 to 2024 other method without range

if __name__ == "__main__":
  # Iterate over each season from 2016 to 2024
  for year in range(2015, 2021):
      for game_type in ["02", "03"]:
          if game_type == "02":
              game_numbers = list(range(1, 1272))
          else:
              game_numbers = list(range(1, 132))

          for game_num in game_numbers:
              if game_type == "03":  # Special formatting for playoff games
                  game_id_str = f"0{str(game_num).zfill(3)}"  # Pad with a leading zero, followed by 3 digits (e.g., "0001" -> "00001")
              else:
                  game_id_str = str(game_num).zfill(4)  # Zero-pad game number to 4 digits

              data_folder = os.getenv("NHL_DATA_FOLDER", "./nhl_data")  # Default to local folder if env variable not set
              os.makedirs(data_folder, exist_ok=True)

              file_path = os.path.join(data_folder, f"game_{year + 1}_{game_type}_{game_id_str}.json")

              # Check if data already exists locally
              if os.path.exists(file_path):
                  print(f"Data already exists for game {year + 1}-{game_type}-{game_id_str}. Skipping download.")
                  continue

              # Fetch and save data
              data = fetch_nhl_play_by_play_data(year, game_type, game_id_str)
              if data:
                  save_data_to_file(data, file_path)

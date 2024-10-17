

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
  for year in range(2016, 2016):
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

"""#Interactive Debugging tool"""

!pip install ipywidgets matplotlib

import ipywidgets as widgets
import matplotlib.pyplot as plt
import json
import os

def browse_files(folder_path):
  """
  Creates an interactive file browser for the specified folder.
  """
  file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
  dropdown = widgets.Dropdown(options=file_list, description='Select File:')
  output = widgets.Output()

  def on_file_selected(change):
    with output:
      output.clear_output()
      selected_file = change['new']
      file_path = os.path.join(folder_path, selected_file)
      try:
        with open(file_path, 'r') as f:
          try:
            data = json.load(f)
            print(f"Content of {selected_file}:")
            print(json.dumps(data, indent=2))
          except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {selected_file}: {e}")
            print(f"Content of {selected_file}:")
            print(f.read())

      except FileNotFoundError:
        print(f"File not found: {file_path}")

  dropdown.observe(on_file_selected, names='value')
  display(widgets.VBox([dropdown, output]))

# Example usage for the /content/nhl_data folder
browse_files('/content/nhl_data')

!pip install rich

from rich import print
from rich.console import Console
from rich.traceback import install
install()
import json
console = Console()

def browse_files(folder_path):
  """
  Creates an interactive file browser for the specified folder.
  """
  file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
  dropdown = widgets.Dropdown(options=file_list, description='Select File:')
  output = widgets.Output()

  def on_file_selected(change):
    with output:
      output.clear_output()
      selected_file = change['new']
      file_path = os.path.join(folder_path, selected_file)
      try:
        with open(file_path, 'r') as f:
          try:
            data = json.load(f)
            print(f"[bold green]Content of {selected_file}:[/bold green]")
            console.print_json(data=data)  # Use Rich to print the JSON with colors and formatting
          except json.JSONDecodeError as e:
            print(f"[bold red]Error decoding JSON from {selected_file}: {e}[/bold red]")
            print(f"[bold yellow]Content of {selected_file}:[/bold yellow]")
            print(f.read())

      except FileNotFoundError:
        print(f"[bold red]File not found: {file_path}[/bold red]")

  dropdown.observe(on_file_selected, names='value')
  display(widgets.VBox([dropdown, output]))

# Example usage for the /content/nhl_data folder
browse_files('/content/nhl_data')

import json

def extract_info_from_json(file_path):
    """
    Extracts information from a JSON file and prints key details.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Print some information about the JSON structure (adapt to your specific needs)
            print("Keys in the top-level JSON object:", list(data.keys()))
            print("-" * 20)
            if "gameData" in data:
                game_data = data["gameData"]
                print("Keys in 'gameData':", list(game_data.keys()))
                if "teams" in game_data:
                    teams_data = game_data["teams"]
                    print("Home team:", teams_data["home"]["name"])
                    print("Away team:", teams_data["away"]["name"])
            if "liveData" in data:
                live_data = data["liveData"]
                print("Keys in 'liveData':", list(live_data.keys()))
                if "plays" in live_data:
                  plays_data = live_data["plays"]
                  print("Keys in 'plays':", list(plays_data.keys()))
                  if 'allPlays' in plays_data:
                    all_plays_data = plays_data['allPlays']
                    print(f"Number of plays: {len(all_plays_data)}")
                    first_play = all_plays_data[0]
                    print("First play:", first_play)


    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")


# Example usage
file_path = "/content/nhl_data/game_2017_02_0616.json"
extract_info_from_json(file_path)

import json

def extract_all_keys(data, parent_key='', sep='.'):
    """Recursively extracts all keys from a nested dictionary or list."""
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = parent_key + sep + k if parent_key else k
            yield new_key
            yield from extract_all_keys(v, new_key, sep=sep)
    elif isinstance(data, list):
        for i, v in enumerate(data):
            new_key = parent_key + sep + str(i) if parent_key else str(i)
            yield new_key
            yield from extract_all_keys(v, new_key, sep=sep)


def extract_keys_from_json_file(file_path):
    """Extracts all keys from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            all_keys = list(extract_all_keys(data))
            return all_keys
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return []


# Example usage:
file_path = "/content/nhl_data/game_2017_02_0001.json"
all_keys = extract_keys_from_json_file(file_path)
if all_keys:
  print("All keys in the JSON file:")
  for key in all_keys:
      print(key)

#visualize the info as a widget and if i chose i want to get answer in that json file

import ipywidgets as widgets
from IPython.display import display, clear_output

def extract_value_by_key(data, key):
    """Extracts a value from a nested dictionary using a dot-separated key."""
    keys = key.split('.')
    current_data = data
    for k in keys:
        if isinstance(current_data, dict) and k in current_data:
            current_data = current_data[k]
        elif isinstance(current_data, list) and k.isdigit() and int(k) < len(current_data):
            current_data = current_data[int(k)]
        else:
            return None
    return current_data

def on_key_selected(change):
    selected_key = change.new
    file_path = "/content/nhl_data/game_2017_02_0001.json"  # Replace with your file path
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            value = extract_value_by_key(data, selected_key)
            with output:
                clear_output()
                if value is not None:
                    print(f"Value for key '{selected_key}':")
                    console.print_json(data=value)
                else:
                    print(f"Key '{selected_key}' not found in the JSON data.")
    except FileNotFoundError:
        with output:
            clear_output()
            print(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        with output:
            clear_output()
            print(f"Error decoding JSON from {file_path}: {e}")

file_path = "/content/nhl_data/game_2017_02_0001.json"  # Replace with your file path
all_keys = extract_keys_from_json_file(file_path)

dropdown = widgets.Dropdown(
    options=all_keys,
    description='Select Key:',
)

output = widgets.Output()

dropdown.observe(on_key_selected, names='value')

display(dropdown, output)

import os
import json
import ipywidgets as widgets
from IPython.display import display, clear_output


def browse_files(folder_path):
    """
    Creates an interactive file browser for the specified folder.
    """
    file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    file_dropdown = widgets.Dropdown(options=file_list, description='Select File:')
    output = widgets.Output()

    def on_file_selected(change):
        with output:
            output.clear_output()
            selected_file = change['new']
            file_path = os.path.join(folder_path, selected_file)
            try:
                with open(file_path, 'r') as f:
                    try:
                        global data  # Declare data as a global variable
                        data = json.load(f)
                        # Update the key dropdown with the keys from the selected file
                        update_key_dropdown(data)

                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from {selected_file}: {e}")
                        print(f"Content of {selected_file}:")
                        print(f.read())

            except FileNotFoundError:
                print(f"File not found: {file_path}")

    file_dropdown.observe(on_file_selected, names='value')
    display(widgets.VBox([file_dropdown, output]))


def update_key_dropdown(data):
    """Updates the key dropdown with keys from the selected JSON file."""
    if data:
        key_dropdown = widgets.Dropdown(options=list(data.keys()), description='Select Key:')
        output_widget = widgets.Output()

        def on_key_selected(change):
            with output_widget:
                clear_output()
                selected_key = change.new
                if selected_key in data:
                    selected_value = data[selected_key]
                    if isinstance(selected_value, dict):
                        # If the value is a dictionary, create a sub-key dropdown
                        update_subkey_dropdown(selected_value, selected_key)
                    else:
                        print(f"Value for '{selected_key}': {selected_value}")
                else:
                    print(f"Key '{selected_key}' not found in the JSON.")

        key_dropdown.observe(on_key_selected, names='value')

        display(widgets.VBox([key_dropdown, output_widget]))


def update_subkey_dropdown(selected_value, selected_key):
    """Updates the subkey dropdown."""
    if selected_value:
        subkey_dropdown = widgets.Dropdown(options=list(selected_value.keys()), description='Select Subkey:')
        output_widget = widgets.Output()

        def on_subkey_selected(change):
            with output_widget:
                clear_output()
                subkey = change.new
                if subkey in selected_value:
                    print(f"Value for '{selected_key}.{subkey}': {selected_value[subkey]}")

        subkey_dropdown.observe(on_subkey_selected, names='value')
        display(widgets.VBox([subkey_dropdown, output_widget]))


# Example usage for the /content/nhl_data folder
browse_files('/content/nhl_data')

#while selecting file give option  season,   regular or play off then choose file, key and subkey

import os
import requests
import json
import ipywidgets as widgets
import matplotlib.pyplot as plt
from rich import print
from rich.console import Console
from rich.traceback import install
from IPython.display import display, clear_output

# ... (Your existing code for fetching and browsing NHL data) ...

def browse_files_with_filters(folder_path):
    """
    Creates an interactive file browser with filters for season, regular/playoff.
    """
    season_dropdown = widgets.Dropdown(options=list(range(2016, 2025)), description='Select Season:')
    game_type_dropdown = widgets.Dropdown(options=['Regular Season', 'Playoffs'], description='Game Type:')
    file_dropdown = widgets.Dropdown(description='Select File:')
    output = widgets.Output()

    def update_file_dropdown(change):
        season = season_dropdown.value
        game_type = game_type_dropdown.value
        file_list = []

        if game_type == 'Regular Season':
            game_type_code = '02'
        else:
            game_type_code = '03'

        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                if f"game_{season + 1}_{game_type_code}" in filename:
                    file_list.append(filename)

        file_dropdown.options = file_list

    season_dropdown.observe(update_file_dropdown, names='value')
    game_type_dropdown.observe(update_file_dropdown, names='value')

    def on_file_selected(change):
        with output:
            output.clear_output()
            selected_file = change['new']
            file_path = os.path.join(folder_path, selected_file)
            try:
                with open(file_path, 'r') as f:
                    try:
                        global data  # Declare data as a global variable
                        data = json.load(f)
                        # Update the key dropdown with the keys from the selected file
                        update_key_dropdown(data)

                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from {selected_file}: {e}")
                        print(f"Content of {selected_file}:")
                        print(f.read())

            except FileNotFoundError:
                print(f"File not found: {file_path}")

    file_dropdown.observe(on_file_selected, names='value')
    display(widgets.VBox([season_dropdown, game_type_dropdown, file_dropdown, output]))

# Example usage for the /content/nhl_data folder
browse_files_with_filters('/content/nhl_data')

#store keys and sub keys as a list

def extract_keys_and_subkeys(data, parent_key=None):
  """
  Recursively extracts all keys and subkeys from a nested dictionary.

  Args:
    data: The dictionary to extract keys from.
    parent_key: The parent key (if any) for the current level.

  Returns:
    A list of tuples, where each tuple contains a key and a list of its subkeys.
  """
  keys_and_subkeys = []
  if isinstance(data, dict):
    for key, value in data.items():
      current_key = key if parent_key is None else f"{parent_key}.{key}"
      if isinstance(value, dict):
        subkeys = [
            f"{current_key}.{sub_key}" for sub_key in value.keys()
        ]  # Extract subkeys
        keys_and_subkeys.append((current_key, subkeys))
        keys_and_subkeys.extend(extract_keys_and_subkeys(value, current_key))
      elif isinstance(value, list):
          keys_and_subkeys.extend(extract_keys_and_subkeys(value, current_key))
      else:
        keys_and_subkeys.append((current_key, []))
  elif isinstance(data, list):
      for index, item in enumerate(data):
          current_key = str(index) if parent_key is None else f"{parent_key}.{index}"
          keys_and_subkeys.extend(extract_keys_and_subkeys(item, current_key))

  return keys_and_subkeys


# Example usage:
file_path = "/content/nhl_data/game_2017_02_0001.json"
try:
    with open(file_path, "r") as f:
        data = json.load(f)
        all_keys_and_subkeys = extract_keys_and_subkeys(data)

        print("Keys and Subkeys:")
        for key, subkeys in all_keys_and_subkeys:
            print(f"- {key}: {subkeys}")

except FileNotFoundError:
    print(f"File not found: {file_path}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON from {file_path}: {e}")

import ipywidgets as widgets
from IPython.display import display

def has_coordinates(data):
    """
    Recursively checks if the JSON data contains 'xCoord' and 'yCoord'.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'xCoord' or key == 'yCoord':
                return True
            if isinstance(value, (dict, list)):
                if has_coordinates(value):
                    return True
    elif isinstance(data, list):
        for item in data:
            if has_coordinates(item):
                return True
    return False

def check_coordinates_in_file(file_path):
    """Checks if a given JSON file contains coordinates."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return has_coordinates(data)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}")
        return False


def on_file_selected(change):
    """Callback function for the dropdown widget."""
    selected_file = change['new']
    file_path = os.path.join('/content/nhl_data', selected_file)  # Assuming files are in /content/nhl_data
    if check_coordinates_in_file(file_path):
        print(f"File '{selected_file}' contains coordinates.")
    else:
        print(f"File '{selected_file}' does not contain coordinates.")


# Create a dropdown widget for selecting a file
file_list = [f for f in os.listdir('/content/nhl_data') if f.endswith('.json')]
dropdown = widgets.Dropdown(options=file_list, description='Select File:')

# Observe changes in the dropdown and call the callback function
dropdown.observe(on_file_selected, names='value')

# Display the widget
display(dropdown)

#  Create a function that processes the raw JSON datas in directory for each game, extracting events of type "shot-on-goal" and "goal" from "plays" into a  dataframe. Include features like game_id, periodDescriptor.number, timeInPeriod, details.eventOwnerTeamId, typeDescKey, details.xCoord, details.yCoord, details.shootingPlayerId ordetails.scoringPlayerId, details.goalieInNetId, details.shotT

import pandas as pd
import json
import os

def process_nhl_data(directory):
  """
  Processes NHL game data JSON files in a directory, extracting shot-on-goal and goal events.

  Args:
    directory: The directory containing the NHL game data JSON files.

  Returns:
    A pandas DataFrame containing the extracted events.
  """

  all_events = []
  for filename in os.listdir(directory):
    if filename.endswith(".json"):
      file_path = os.path.join(directory, filename)
      try:
        with open(file_path, "r") as f:
          data = json.load(f)
          game_id = data.get("gamePk")
          if "liveData" in data and "plays" in data["liveData"] and "allPlays" in data["liveData"]["plays"]:
            plays = data["liveData"]["plays"]["allPlays"]
            for play in plays:
              if "result" in play and "event" in play["result"]:
                event_type = play["result"]["event"]
                if event_type in ["Shot on Goal", "Goal"]:
                  event_data = {
                      "game_id": game_id,
                      "periodDescriptor.number": play.get("about", {}).get("period"),
                      "timeInPeriod": play.get("about", {}).get("periodTime"),
                      "details.eventOwnerTeamId": play.get("team", {}).get("id"),
                      "typeDescKey": play["result"].get("eventTypeId"),
                      "details.xCoord": play.get("coordinates", {}).get("x"),
                      "details.yCoord": play.get("coordinates", {}).get("y"),
                      "details.shotType": play.get("result", {}).get("secondaryType"),
                  }
                  if "players" in play:
                    for player in play["players"]:
                      if player["playerType"] == "Shooter":
                        event_data["details.shootingPlayerId"] = player.get("player", {}).get("id")
                      elif player["playerType"] == "Scorer":
                         event_data["details.scoringPlayerId"] = player.get("player", {}).get("id")
                      elif player["playerType"] == "Goalie":
                        event_data["details.goalieInNetId"] = player.get("player", {}).get("id")

                  all_events.append(event_data)

      except FileNotFoundError:
        print(f"File not found: {file_path}")
      except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}")

  df = pd.DataFrame(all_events)
  return df

# Example usage:
directory = "/content/nhl_data"
nhl_df = process_nhl_data(directory)
print(nhl_df.head())

"""#Part 3

"""

#  convert json files in a directory to data frame

import pandas as pd
import json
import os

def json_to_dataframe(folder_path):
  """
  Converts all JSON files in a directory to a single Pandas DataFrame.

  Args:
    folder_path: The path to the directory containing the JSON files.

  Returns:
    A Pandas DataFrame containing the data from all JSON files.
  """
  dataframes = []
  for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
      file_path = os.path.join(folder_path, filename)
      with open(file_path, 'r') as f:
        try:
          data = json.load(f)
          df = pd.json_normalize(data)  # Flatten the JSON data into a DataFrame
          dataframes.append(df)
        except json.JSONDecodeError as e:
          print(f"Error decoding JSON from {filename}: {e}")

  if dataframes:
    return pd.concat(dataframes, ignore_index=True)
  else:
    return pd.DataFrame()

# Example usage:
folder_path = '/content/nhl_data'
df = json_to_dataframe(folder_path)

# Print the resulting DataFrame or perform further analysis
if not df.empty:
  print(df.head())
else:
  print("No valid JSON files found in the directory.")

print(df.columns)

# Assuming df is your original dataframe with all columns

# List of columns to keep
columns_to_keep = [
    'id', 'season', 'gameType', 'gameDate', 'startTimeUTC',
        'awayTeam.id', 'awayTeam.name.default', 'awayTeam.abbrev', 'awayTeam.score', 'awayTeam.sog',
            'homeTeam.id', 'homeTeam.name.default', 'homeTeam.abbrev', 'homeTeam.score', 'homeTeam.sog',
                'venue.default', 'venueLocation.default',
                    'shootoutInUse', 'otInUse', 'periodDescriptor.number', 'periodDescriptor.periodType',
                        'clock.timeRemaining', 'clock.secondsRemaining', 'gameOutcome.lastPeriodType',
                            'plays'
                            ]
filtered_df = df[columns_to_keep]
print(filtered_df.head())


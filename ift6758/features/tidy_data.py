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
  for year in range(2016, 2025):
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

"""#Part 3

"""

import json
import pandas as pd

# Function to process game events into a dataframe
def process_game_events_to_dataframe(json_file):
    # Load JSON data
    with open(json_file) as f:
        data = json.load(f)

    game_id = data['id']
    events = data['plays']

    # List to store the processed data
    processed_events = []

    # Loop through each play in the events
    for event in events:
        # Filter shots and goals
        if event['typeDescKey'] in ['shot-on-goal', 'goal']:
            # Extract general event details
            period = event['periodDescriptor']['number']
            time_in_period = event['timeInPeriod']
            event_type = 'shot' if event['typeDescKey'] == 'shot-on-goal' else 'goal'
            event_details = event.get('details', {})

            # Extract specific details for each event
            x_coord = event_details.get('xCoord')
            y_coord = event_details.get('yCoord')
            shot_type = event_details.get('shotType')
            shooting_player_id = event_details.get('shootingPlayerId') if 'shootingPlayerId' in event_details else event_details.get('scoringPlayerId')
            goalie_player_id = event_details.get('goalieInNetId')
            team_id = event_details.get('eventOwnerTeamId')
            strength = "even" if event_type == 'goal' else "N/A"

            # Add processed event data to the list
            processed_events.append({
                'game_id': game_id,
                'period': period,
                'time_in_period': time_in_period,
                'event_type': event_type,
                'x_coord': x_coord,
                'y_coord': y_coord,
                'shot_type': shot_type,
                'shooting_player_id': shooting_player_id,
                'goalie_player_id': goalie_player_id,
                'team_id': team_id,
                'strength': strength
            })

    # Create DataFrame from the processed list
    df = pd.DataFrame(processed_events)
    return df

# Example usage in Google Colab
json_file_path = '/content/nhl_data/game_2017_02_0001.json'  # Update path if the file is saved in another location in Colab
df = process_game_events_to_dataframe(json_file_path)
print(df.head(10))

"""**Create a pandas dataframe from all the JSON file, filtering only "shot-on-goal" and "goal" events. Include columns: game_id, period, time_in_period, event_type (shot or goal), team_id, x_coord, y_coord, shot_type, shooting_player_id, goalie_player_id, and strength (default to "even"). Extract these values from corresponding fields in the JSON and structure them accordingly.**





"""

import json
import pandas as pd
import glob

# Function to process game events into a dataframe for a single file
def process_game_events_to_dataframe(json_file):
    # Load JSON data
    with open(json_file) as f:
        data = json.load(f)

    game_id = data['id']
    events = data['plays']

    # List to store the processed data
    processed_events = []

    # Loop through each play in the events
    for event in events:
        # Filter shots and goals
        if event['typeDescKey'] in ['shot-on-goal', 'goal']:
            # Extract general event details
            period = event['periodDescriptor']['number']
            time_in_period = event['timeInPeriod']
            event_type = 'shot' if event['typeDescKey'] == 'shot-on-goal' else 'goal'
            event_details = event.get('details', {})

            # Extract specific details for each event
            x_coord = event_details.get('xCoord')
            y_coord = event_details.get('yCoord')
            shot_type = event_details.get('shotType')
            shooting_player_id = event_details.get('shootingPlayerId') if 'shootingPlayerId' in event_details else event_details.get('scoringPlayerId')
            goalie_player_id = event_details.get('goalieInNetId')
            team_id = event_details.get('eventOwnerTeamId')
            strength = "even" if event_type == 'goal' else "N/A"

            # Add processed event data to the list
            processed_events.append({
                'game_id': game_id,
                'period': period,
                'time_in_period': time_in_period,
                'event_type': event_type,
                'x_coord': x_coord,
                'y_coord': y_coord,
                'shot_type': shot_type,
                'shooting_player_id': shooting_player_id,
                'goalie_player_id': goalie_player_id,
                'team_id': team_id,
                'strength': strength
            })

    return pd.DataFrame(processed_events)

# Process all JSON files in the specified directory and concatenate them into a single dataframe
def process_all_games_in_directory(directory_path):
    all_files = glob.glob(f"{directory_path}/*.json")
    all_dataframes = []

    for json_file in all_files:
        df = process_game_events_to_dataframe(json_file)
        all_dataframes.append(df)

    # Concatenate all dataframes into one
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    return combined_df

# Example usage in Google Colab
directory_path = '/content/nhl_data'  # Update this path to match your directory containing the JSON files in Colab
combined_df = process_all_games_in_directory(directory_path)
print(combined_df.head(10))

import json
import pandas as pd
import glob

def process_all_games_in_directory(directory_path):
    """
    Processes all JSON files in the specified directory and converts them into a pandas dataframe
    containing only "shot" and "goal" events.

    Parameters:
        directory_path (str): Path to the directory containing JSON files.

    Returns:
        pd.DataFrame: Dataframe containing relevant event information for "shot" and "goal" events.
    """
    all_files = glob.glob(f"{directory_path}/*.json")
    processed_events = []

    # Loop through all JSON files in the directory
    for json_file in all_files:
        with open(json_file) as f:
            data = json.load(f)

        game_id = data['id']
        events = data['plays']

        # Loop through each play in the events
        for event in events:
            # Filter for "shots" and "goals"
            if event['typeDescKey'] in ['shot-on-goal', 'goal']:
                # Extract general event details
                period = event['periodDescriptor']['number']
                time_in_period = event['timeInPeriod']
                event_type = 'shot' if event['typeDescKey'] == 'shot-on-goal' else 'goal'
                event_details = event.get('details', {})

                # Extract specific details for each event
                x_coord = event_details.get('xCoord')
                y_coord = event_details.get('yCoord')
                shot_type = event_details.get('shotType')
                shooting_player_id = event_details.get('shootingPlayerId') if 'shootingPlayerId' in event_details else event_details.get('scoringPlayerId')
                goalie_player_id = event_details.get('goalieInNetId')
                team_id = event_details.get('eventOwnerTeamId')
                empty_net = event_details.get('emptyNet', False)  # Assuming empty net information, defaulting to False
                strength = "even" if event_type == 'goal' else "N/A"

                # Append processed event data to the list
                processed_events.append({
                    'game_id': game_id,
                    'period': period,
                    'time_in_period': time_in_period,
                    'event_type': event_type,
                    'team_id': team_id,
                    'x_coord': x_coord,
                    'y_coord': y_coord,
                    'shot_type': shot_type,
                    'shooting_player_id': shooting_player_id,
                    'goalie_player_id': goalie_player_id,
                    'empty_net': empty_net,
                    'strength': strength
                })

    # Create a DataFrame from the processed list
    df = pd.DataFrame(processed_events)
    return df

# Example usage in Google Colab
directory_path = '/content/nhl_data'  # Update this path to match your directory containing the JSON files in Colab
combined_df = process_all_games_in_directory(directory_path)

# Print the first 10 rows of the resulting dataframe
print(combined_df.head(10))

import json
import pandas as pd
import glob

def process_all_games_in_directory(directory_path):
    """
    Processes all JSON files in the specified directory and converts them into a pandas dataframe
    containing only "shot" and "goal" events.

    Parameters:
        directory_path (str): Path to the directory containing JSON files.

    Returns:
        pd.DataFrame: Dataframe containing relevant event information for "shot" and "goal" events.
    """
    all_files = glob.glob(f"{directory_path}/*.json")
    processed_events = []

    # Loop through all JSON files in the directory
    for json_file in all_files:
        with open(json_file) as f:
            data = json.load(f)

        game_id = data['id']
        events = data['plays']

        # Loop through each play in the events
        for event in events:
            # Filter for "shots" and "goals"
            if event['typeDescKey'] in ['shot-on-goal', 'goal']:
                # Extract general event details
                period = event['periodDescriptor']['number']
                time_in_period = event['timeInPeriod']
                event_type = 'shot' if event['typeDescKey'] == 'shot-on-goal' else 'goal'
                event_details = event.get('details', {})

                # Extract specific details for each event
                x_coord = event_details.get('xCoord')
                y_coord = event_details.get('yCoord')
                shot_type = event_details.get('shotType')
                shooting_player_id = event_details.get('shootingPlayerId') if 'shootingPlayerId' in event_details else event_details.get('scoringPlayerId')
                goalie_player_id = event_details.get('goalieInNetId')
                team_id = event_details.get('eventOwnerTeamId')
                empty_net = event_details.get('emptyNet', False)  # Assuming empty net information, defaulting to False
                strength = "even" if event_type == 'goal' else None

                # Append processed event data to the list
                processed_events.append({
                    'Game ID': game_id,
                    'Period': period,
                    'Time in Period': time_in_period,
                    'Event Type': event_type.capitalize(),
                    'Team ID': team_id,
                    'X Coordinate': x_coord,
                    'Y Coordinate': y_coord,
                    'Shot Type': shot_type.capitalize() if shot_type else None,
                    'Shooter ID': shooting_player_id,
                    'Goalie ID': goalie_player_id,
                    'Empty Net': empty_net,
                    'Strength': strength.capitalize() if strength else None
                })

    # Create a DataFrame from the processed list
    df = pd.DataFrame(processed_events)

    # Convert the dataframe columns to more appropriate data types for analysis
    df['Game ID'] = df['Game ID'].astype(int)
    df['Period'] = df['Period'].astype(int)
    df['X Coordinate'] = df['X Coordinate'].astype(float)
    df['Y Coordinate'] = df['Y Coordinate'].astype(float)
    df['Team ID'] = df['Team ID'].astype(int)
    df['Shooter ID'] = df['Shooter ID'].astype(int)
    df['Goalie ID'] = df['Goalie ID'].astype(float)  # Allow for NaN values for Goalie ID
    df['Empty Net'] = df['Empty Net'].astype(bool)

    # Set appropriate column order
    column_order = [
        'Game ID', 'Period', 'Time in Period', 'Event Type', 'Team ID', 'X Coordinate',
        'Y Coordinate', 'Shot Type', 'Shooter ID', 'Goalie ID', 'Empty Net', 'Strength'
    ]
    df = df[column_order]

    # Neatly format the DataFrame for clean output in print
    pd.set_option('display.float_format', '{:.1f}'.format)  # Format floats to one decimal
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.width', 1000)  # Increase width to fit more columns
    pd.set_option('display.colheader_justify', 'center')  # Center align headers

    return df

# Example usage in Google Colab
directory_path = '/content/nhl_data'  # Update this path to match your directory containing the JSON files in Colab
combined_df = process_all_games_in_directory(directory_path)

# Display the first 10 rows of the dataframe
print(combined_df.head(10))

"""The combined DataFrame (df) is created from all JSON files in the directory.
Three new features (rebound, shot_off_rush, danger_zone) are added to enhance the analysis.


"""

import json
import pandas as pd
import glob

def load_all_games(directory_path):
    """
    Load and process all JSON files from the specified directory.

    Parameters:
        directory_path (str): Path to the directory containing JSON files.

    Returns:
        pd.DataFrame: Combined DataFrame with event details from all games.
    """
    all_files = glob.glob(f"{directory_path}/*.json")
    processed_events = []

    # Loop through all JSON files in the directory
    for json_file in all_files:
        with open(json_file) as f:
            data = json.load(f)

        events = data.get('plays', [])
        game_id = data['id']

        # Extract relevant event data
        for event in events:
            event_type = event.get('typeDescKey')
            period = event['periodDescriptor']['number']
            time_in_period = event['timeInPeriod']
            details = event.get('details', {})
            team_id = details.get('eventOwnerTeamId')
            x_coord = details.get('xCoord')
            y_coord = details.get('yCoord')

            # Append processed event to the list
            processed_events.append({
                'game_id': game_id,
                'period': period,
                'time_in_period': time_in_period,
                'event_type': event_type,
                'team_id': team_id,
                'x_coord': x_coord,
                'y_coord': y_coord
            })

    # Create a DataFrame from the processed list
    df = pd.DataFrame(processed_events)
    return df

def add_rebound_indicator(df):
    df = df.sort_values(by=['game_id', 'period', 'time_in_period'])
    df['rebound'] = False
    df['time_in_period_sec'] = df['time_in_period'].apply(lambda x: int(x.split(":")[0]) * 60 + int(x.split(":")[1]))

    for idx in range(1, len(df)):
        current_event = df.iloc[idx]
        previous_event = df.iloc[idx - 1]

        if (current_event['game_id'] == previous_event['game_id'] and
                current_event['period'] == previous_event['period'] and
                current_event['team_id'] == previous_event['team_id'] and
                current_event['event_type'] == 'shot-on-goal' and previous_event['event_type'] in ['shot-on-goal', 'goal']):

            time_difference = current_event['time_in_period_sec'] - previous_event['time_in_period_sec']

            if 0 < time_difference <= 10:
                df.at[idx, 'rebound'] = True

    return df

def add_shot_off_rush_indicator(df):
    df = df.sort_values(by=['game_id', 'period', 'time_in_period'])
    df['shot_off_rush'] = False
    df['time_in_period_sec'] = df['time_in_period'].apply(lambda x: int(x.split(":")[0]) * 60 + int(x.split(":")[1]))

    for idx in range(1, len(df)):
        current_event = df.iloc[idx]
        previous_event = df.iloc[idx - 1]

        if (current_event['game_id'] == previous_event['game_id'] and
                current_event['period'] == previous_event['period'] and
                current_event['team_id'] == previous_event['team_id'] and
                current_event['event_type'] == 'shot-on-goal' and previous_event['event_type'] == 'takeaway'):

            time_difference = current_event['time_in_period_sec'] - previous_event['time_in_period_sec']

            if 0 < time_difference <= 10:
                df.at[idx, 'shot_off_rush'] = True

    return df

def add_danger_zone(df):
    df['danger_zone'] = 'Low'

    for idx in range(len(df)):
        x_coord = df.at[idx, 'x_coord']
        y_coord = df.at[idx, 'y_coord']

        if x_coord is not None and y_coord is not None:
            if -20 <= x_coord <= 20 and -10 <= y_coord <= 10:
                df.at[idx, 'danger_zone'] = 'High'
            elif -30 <= x_coord <= 30 and -20 <= y_coord <= 20:
                df.at[idx, 'danger_zone'] = 'Medium'

    return df

# Example usage in Google Colab or local environment
directory_path = '/content/nhl_data'  # Path to directory containing JSON files
df = load_all_games(directory_path)

# Add features to the DataFrame
df = add_rebound_indicator(df)
df = add_shot_off_rush_indicator(df)
df = add_danger_zone(df)

# Display the first 10 rows of the DataFrame
print(df.head(10))

"""All Features Added:

**Shot Distance from Goal (shot_distance)**

Calculates the Euclidean distance of each shot from the goal.

**Time Between Shots (time_between_shots)**

Calculates the time elapsed since the previous shot, providing context on the game's pace.

**Odd-Man Rush Indicator (odd_man_rush)**

Marks whether a shot was part of an odd-man rush, indicating an advantageous attacking situation.
"""

import numpy as np

def add_shot_distance(df):
    """Add a feature for the distance from the goal."""
    df['shot_distance'] = np.sqrt(df['x_coord']**2 + df['y_coord']**2)
    return df

def add_time_between_shots(df):
    """Add a feature for the time elapsed since the previous shot."""
    df = df.sort_values(by=['game_id', 'period', 'time_in_period'])
    df['time_between_shots'] = None

    for idx in range(1, len(df)):
        current_event = df.iloc[idx]
        previous_event = df.iloc[idx - 1]

        if (current_event['game_id'] == previous_event['game_id'] and
                current_event['period'] == previous_event['period'] and
                current_event['event_type'] == 'shot-on-goal'):

            current_time = int(current_event['time_in_period'].split(":")[0]) * 60 + int(current_event['time_in_period'].split(":")[1])
            previous_time = int(previous_event['time_in_period'].split(":")[0]) * 60 + int(previous_event['time_in_period'].split(":")[1])
            time_diff = current_time - previous_time

            df.at[idx, 'time_between_shots'] = time_diff

    df['time_between_shots'] = df['time_between_shots'].fillna(0).astype(int)
    return df

def add_odd_man_rush_indicator(df):
    """Add a feature indicating if the shot was part of an odd-man rush."""
    df = df.sort_values(by=['game_id', 'period', 'time_in_period'])
    df['odd_man_rush'] = False

    for idx in range(1, len(df)):
        current_event = df.iloc[idx]
        previous_event = df.iloc[idx - 1]

        # Assuming a takeaway by the same team immediately followed by a shot is an indicator of an odd-man rush
        if (current_event['game_id'] == previous_event['game_id'] and
                current_event['period'] == previous_event['period'] and
                current_event['team_id'] == previous_event['team_id'] and
                current_event['event_type'] == 'shot-on-goal' and previous_event['event_type'] == 'takeaway'):

            current_time = int(current_event['time_in_period'].split(":")[0]) * 60 + int(current_event['time_in_period'].split(":")[1])
            previous_time = int(previous_event['time_in_period'].split(":")[0]) * 60 + int(previous_event['time_in_period'].split(":")[1])
            time_diff = current_time - previous_time

            if 0 < time_diff <= 10:
                df.at[idx, 'odd_man_rush'] = True

    return df

# Example usage in Google Colab or local environment
directory_path = '/content/nhl_data'  # Path to directory containing JSON files
df = load_all_games(directory_path)

# Add original features to the DataFrame
df = add_rebound_indicator(df)
df = add_shot_off_rush_indicator(df)
df = add_danger_zone(df)

# Add new features to the DataFrame
df = add_shot_distance(df)
df = add_time_between_shots(df)
df = add_odd_man_rush_indicator(df)

# Display the first 10 rows of the DataFrame with all features
print(df.head(10))


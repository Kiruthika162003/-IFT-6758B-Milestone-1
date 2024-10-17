
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

import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
from PIL import Image


import os

nhl_files = os.listdir('/content/nhl_data')



def get_metadata(game_id, event_id, files):
  f = open('/content/nhl_data/' + nhl_files[game_id - 1])
  selected_game = json.load(f)
  selected_event = {}



  for e in selected_game['plays']:
    if e['eventId'] == event_id:
      selected_event = e
      break


  return len(selected_game['plays']) - 1, selected_game['id'], selected_game['startTimeUTC'], selected_game['homeTeam']['name']['default'], selected_game['awayTeam']['name']['default'], e









rink_image_path = '/content/nhl_rink.png'  # Replace with your ice rink image file path
rink_image = Image.open(rink_image_path)
center_x, center_y = rink_image.width / 2, rink_image.height / 2

# Function to plot a single event on the rink image
def plot_single_event_on_rink(event, game_id, event_id):
    # Create a plot with the rink image as the background
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(rink_image, extent=[-90, 90, 42.5, -42.5])  # Adjust extent to center origin


    # Plot the single event
    ax.scatter(event['details']['xCoord'], event['details']['yCoord'], c='red', s=200, marker='o')
    ax.text(event['details']['xCoord'] + 5, event['details']['yCoord'], f"Game {game_id} - {event['eventId']}", fontsize=12, color='white')

    # Set plot title and hide axis
    plt.title(f"Game ID: {game_id}, Event ID: {event_id}")
    ax.axis('off')  # Hide axis
    plt.show()

# Create interactive sliders
game_id_slider = widgets.IntSlider(min=1, max=len(nhl_files), step=1, value=1, description='Game ID')
event_id_slider = widgets.IntSlider(min=1, max=2, step=1, value=1, description='Event ID')

# Function to update the plot based on slider values
def update_plot(game_id, event_id):
    # Get the selected event based on the slider value
    events_length, id, time, home, away, selected_event = get_metadata(game_id, event_id, nhl_files)

    # Update event_id slider range based on the number of events in the selected game

    event_id_slider.max = events_length

    print('id:'+str(id))
    print(time)
    print(home+'(home) vs '+away+'(away)')

    print(selected_event)


    if 'details' in selected_event.keys():
      if 'xCoord' in selected_event['details'].keys():
        # Plot the selected event on the rink
        plot_single_event_on_rink(selected_event, game_id, event_id)

    print(selected_event)


# Link sliders to the update function
widgets.interact(update_plot, game_id=game_id_slider, event_id=event_id_slider)

# Display the sliders
display(game_id_slider, event_id_slider)


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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import seaborn as sns
import os
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
          try:
            data = json.load(f)
          except ValueError:
            pass


        # Debug: Print the JSON data keys to verify the structure
        print(f"Processing file: {json_file}")
        print("Top-level keys:", data.keys())

        game_id = data.get('id')
        if game_id is None:
            print(f"Game ID missing in file: {json_file}. Skipping.")
            continue

        # Extract the season from the first four characters of game_id
        game_id_str = str(game_id)  # Ensure game_id is treated as a string
        season = game_id_str[:4]  # Extract the first four characters to determine the season
        events = data.get('plays', [])

        # Extract relevant event data
        for event in events:
            event_type = event.get('typeDescKey')
            period = event.get('periodDescriptor', {}).get('number')
            time_in_period = event.get('timeInPeriod')
            details = event.get('details', {})
            team_id = details.get('eventOwnerTeamId')
            x_coord = details.get('xCoord')
            y_coord = details.get('yCoord')
            shot_type = details.get('shotType')  # Extracting shot type

            # Append processed event to the list
            processed_events.append({
                'game_id': game_id,
                'season': season,  # Use the first four digits as the season
                'period': period,
                'time_in_period': time_in_period,
                'event_type': event_type,
                'team_id': team_id,
                'x_coord': x_coord,
                'y_coord': y_coord,
                'shot_type': shot_type
            })

    # Create a DataFrame from the processed list
    df = pd.DataFrame(processed_events)
    return df

# Normalize coordinates for plotting (offensive zone only)
def normalize_coordinates(df):
    # Filter shot events
    shot_df = df[df['event_type'].isin(['shot-on-goal', 'goal'])].copy()  # Use .copy() to avoid SettingWithCopyWarning

    # Normalize the x-coordinates for offensive zone shots (ensuring all are positive for plotting)
    shot_df.loc[:, 'norm_x'] = shot_df['x_coord'].abs()
    shot_df.loc[:, 'norm_y'] = shot_df['y_coord']

    return shot_df

directory_path = '/content/nhl_data'  # Path to directory containing JSON files
df = load_all_games(directory_path)

# Normalize the coordinates of the data
shot_df = normalize_coordinates(df)

# Debug: Check some sample rows
print("Normalized Coordinates:\n", shot_df[['game_id', 'team_id', 'norm_x', 'norm_y', 'shot_type']].head())

def get_season(shot_df,seasons):
  shot_df_clean = shot_df.dropna(subset=['x_coord'])
  return shot_df_clean[(shot_df_clean['season'] == str(seasons[0]))]

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
from PIL import Image
import plotly.graph_objects as go


# Load rink background image if needed (assuming you have a rink image)
rink_image_path = '/content/325781728659385_.pic.jpg'  # Use the uploaded image file if needed
rink_image = Image.open(rink_image_path)

# Sample shot data (replace with actual shot data)

# Create a DataFrame from the sample shot data

# Define the area for the rink dimensions in the plot
rink_extent = [-42.5, 42.5, 0, 90]  # Define extent for the rink image

for season in [[2016,2017],[2017,2018],[2018,2019],[2019,2020],[2020,2021]]:
  selected_seasons_df = get_season(shot_df,season)
  selected_seasons_df_clean = selected_seasons_df.dropna()
  print(len(selected_seasons_df_clean))
  # Create a density estimate (2D Kernel Density Estimation) using Gaussian KDE
  kde = gaussian_kde([selected_seasons_df_clean['norm_y'], selected_seasons_df_clean['norm_x']], bw_method=0.5)
  # kde_selected_team = gaussian_kde([season2018_team1_df['norm_y'], season2018_team1_df['norm_x']], bw_method=0.5)



  # Create a grid over the rink to evaluate the KDE
  x_grid = np.linspace(-42.5, 42.5, 85)
  y_grid = np.linspace(0, 90, 90)
  x_mesh, y_mesh = np.meshgrid(x_grid, y_grid)
  positions = np.vstack([x_mesh.ravel(), y_mesh.ravel()])
  kde_values = np.reshape(kde(positions).T, x_mesh.shape)
  # kde_values_selected_team = np.reshape(kde_selected_team(positions).T, x_mesh.shape)

  # # total_hours = len(set(season2018_df['game_id'][0:10000]))
  # # team_hours = len(set(season2018_team1_df['game_id']))

  # # kde_values_per_hour = kde_values * 10000 / total_hours
  # # kde_values_selected_team_per_hour = kde_values_selected_team * len(season2018_team1_df) / team_hours
  # excess_shot_rate = kde_values_selected_team - kde_values
  # excess_shot_rate/= excess_shot_rate.max()
  # # Normalize KDE values (optional) to make it easier to interpret
  # kde_values_selected_team_per_hour /= kde_values_selected_team_per_hour.max()
  # print(kde_values_selected_team_per_hour)
  # # Create the plot
  # fig, ax = plt.subplots(figsize=(10, 8))

  # # Show the rink image as the background
  # ax.imshow(rink_image, extent=rink_extent, aspect='auto', alpha=0.5, zorder=0)
  # levels = np.linspace(-1, 1, 9)
  # contour = ax.contourf(x_mesh, y_mesh, excess_shot_rate, levels=levels, cmap='coolwarm', alpha=0.8, zorder=1)

  # # Add a color bar to the plot with discrete levels
  # cbar = plt.colorbar(contour, ax=ax, shrink=0.75, ticks=levels)
  # cbar.set_label('Escess Shot Rate (per hour)', rotation=270, labelpad=15)


  # # Configure axis labels and title
  # ax.set_xlabel("Distance from Centre of Rink (ft)")
  # ax.set_ylabel("Distance from Goal Line (ft)")
  # ax.set_title("Excess Shot Rate Heatmap for the Season")

  # # # Remove axis ticks and labels for a cleaner look
  # # ax.set_xticks([])
  # # ax.set_yticks([])

  # # Show the final plot
  # plt.show()

  kde_values_by_team = {}
  teams = list(set(selected_seasons_df['team_id']))

  # Calculate KDE values and excess shot rate for each team
  for team in teams:
      # Filter shot data for the selected team
      team_df = selected_seasons_df_clean[selected_seasons_df_clean['team_id'] == team]

      # Create a KDE for the selected team
      kde_team = gaussian_kde([team_df['norm_y'], team_df['norm_x']], bw_method=0.5)
      kde_values_team = np.reshape(kde_team(positions).T, x_mesh.shape)

      # Calculate shot rate per hour for the selected team
      # team_hours = len(set(team_df['game_id']))
      # kde_values_per_hour_team = kde_values_team * len(team_df) / team_hours

      # Calculate shot rate per hour for all teams
      # kde_values_per_hour_all_teams = kde_values_all_teams * len(season2018_df) / total_hours_all_teams

      # Calculate excess shot rate
      excess_shot_rate = kde_values_team - kde_values

      excess_shot_rate /= excess_shot_rate.max()

      # Store the KDE and excess shot rate values for each team
      kde_values_by_team[team] = excess_shot_rate

  # Create Plotly figure with dropdown menu
  fig = go.Figure()
  custom_colorscale = [
      [0.0, 'rgb(0, 0, 255)'],    # Blue for -1
      [0.5, 'rgb(255, 255, 255)'], # White for 0
      [1.0, 'rgb(255, 0, 0)']      # Red for 1
  ]
  # Add heatmap traces for each team
  for team, excess_shot_rate in kde_values_by_team.items():
      # Create a heatmap trace for each team's excess shot rate
      fig.add_trace(go.Contour(
      z=excess_shot_rate,
      x=x_grid,
      y=y_grid,
      colorscale=custom_colorscale,
      colorbar=dict(title='Excess Shot Rate per Hour'),
      visible=False,
      name=team,
      contours=dict(
          showlines=False,  # Do not show separate black lines
          coloring='heatmap'
      ),
      zmin=-1,
      zmax=1,
      opacity=0.8,
      line_smoothing=0.85
  ))

  # Set the first team's heatmap to be visible by default
  fig.data[0].visible = True

  # Create dropdown menu buttons
  dropdown_buttons = [
      dict(label=team,
          method='update',
          args=[{'visible': [str(team) == str(trace.name) for trace in fig.data]},
                {'title': f'Excess Shot Rate Heatmap for team number {int(team)} in season '+str(season[0])+'~'+str(season[1])}])
      for team in teams
  ]

  # Configure the layout with dropdown menu
  fig.update_layout(
      title=f'Excess Shot Rate Heatmap for team number {int(teams[0])} in season '+str(season[0])+'~'+str(season[1]),
      xaxis=dict(title='Distance from Centre of Rink (ft)'),
      yaxis=dict(title='Distance from Goal Line (ft)'),
      updatemenus=[
          dict(
              buttons=dropdown_buttons,
              direction='down',
              showactive=True,
              x=0.17,
              xanchor='left',
              y=1.15,
              yanchor='top'
          )
      ]
  )

  # Add the background rink image as a layout image
  fig.update_layout(
      images=[dict(
          source=rink_image,
          xref="x",
          yref="y",
          x=-42.5,
          y=90,
          sizex=85,
          sizey=90,
          sizing="stretch",
          opacity=0.5,
          layer="below"
      )]
  )
  # fig.update_xaxes(range=[-42.5, 42.5], scaleanchor="y", scaleratio=1)
  # fig.update_yaxes(range=[0, 90],scaleanchor="x", scaleratio=1)
  # Show the interactive plot
  fig.show()

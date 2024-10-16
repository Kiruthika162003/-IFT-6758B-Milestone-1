import os
import json
import glob
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import ipywidgets as widgets
from IPython.display import display
from rich.console import Console
from rich.traceback import install
from scipy.stats import norm
from PIL import Image

install()
console = Console()

from .plotly_html_advanced_visuals import (
    update_plot,
    plot_single_event_on_rink,
    browse_files,
    browse_files_with_filters,
    on_file_selected,
    update_key_dropdown,
    update_subkey_dropdown,
    on_key_selected,
)

from .yet_another_copy_of_data_acquisition import (
    download_and_cache_nhl_data,
    fetch_nhl_play_by_play_data,
    load_all_games,
    process_all_games_in_directory,
    process_game_events_to_dataframe,
    normalize_coordinates,
    has_coordinates,
    add_shot_distance,
    add_shot_off_rush_indicator,
    add_rebound_indicator,
    add_time_between_shots,
    add_odd_man_rush_indicator,
    add_danger_zone,
    process_nhl_data,
    get_metadata,
    get_season,
    extract_all_keys,
    extract_info_from_json,
    extract_value_by_key,
    extract_keys_and_subkeys,
    extract_keys_from_json_file,
    save_data_to_file,
    check_coordinates_in_file,
)

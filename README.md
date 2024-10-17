

# **IFT 6758 Project: Milestone 1**

### **Team Members**
| Name                    | Email                                    |
|-------------------------|------------------------------------------|
| Kiruthika Subramani     | [kiruthika.subramani@umontreal.ca](mailto:kiruthika.subramani@umontreal.ca) |
| Tikshan Kumar Soobanah  | [tikshan.kumar.soobanah@umontreal.ca](mailto:tikshan.kumar.soobanah@umontreal.ca) |
| Yizhan Li               | [yizhan.li@umontreal.ca](mailto:yizhan.li@umontreal.ca) |

---

## **Project Overview**
This project focuses on **NHL hockey data** retrieval, wrangling, and visualization using the **NHL stats API**. The primary goal of Milestone 1 is to perform:
1. **Data acquisition** of play-by-play game data and season statistics.
2. **Tidy data creation** to make raw event data suitable for analysis.
3. **Exploratory visualizations** to gain insights into shot types, shot probabilities, and team performances.
4. **Interactive tools** to explore and debug the play-by-play data.
5. **Advanced visualizations** using shot maps to analyze shot patterns and success rates.

---

## **Project Structure**

```
IFT-6758B-Milestone-1-main/
│
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── setup.py                    # Installation setup (if applicable)
├── environment.yml             # Conda environment configuration (optional)
│
├── figures/                    # Generated visualizations and outputs
│   ├── Advanced_Visualization.png
│   ├── Comparison_of_Shot_Types_with_Goals_Overlay.png
│   ├── Goal_Percentage_by_Distance_and_Shot_Type_2018-19.png
│   ├── Interactive_Debugging_Output.png
│   ├── Shot_Distance_vs_Goal_Probability.png
│   ├── Shot_Distance_Distribution_by_Goal_Outcome.png
│   └── nhl_rink.png            # Ice rink image for plotting events
│
├── ift6758/                    # Main code modules for different tasks
│   ├── data/
│   │   ├── 1_data_acquisition.py          # Primary data acquisition script
│   │   ├── 2_data_acquisition_method_2.py # Alternative data retrieval logic
│   │   ├── Final_Dataframe.zip            # Sample processed data output
│   │   └── Sample_Json_Downloaded.json    # Sample raw JSON from API
│   │
│   ├── features/
│   │   ├── 2_interactive_debugging_nhl_data.py  # Interactive tool logic
│   │   └── exploring_the_json_files(_additional_eda).py  # EDA on raw data
│   │
│   └── visualizations/
│       ├── simple_visualization.py        # Simple visualizations
│       └── 5_advanced_visualization.py    # Advanced shot maps and KDE
│
├── notebooks/                 # Jupyter notebooks for different analysis phases
│   ├── 1_Data_Acquisition.ipynb           # Downloading NHL game data
│   ├── 2_Data_Acquisition_Method_2.ipynb  # Alternative data acquisition
│   ├── 2_Interactive_Debugging_NHL_Data.ipynb  # Interactive debugging exploration
│   ├── Exploring_the_Json_Files(_Additional_EDA).ipynb # Additional EDA notebook
│   ├── Simple_visualizations.ipynb        # Generating simple plots and insights
│   └── Tidy_Data.ipynb                    # Data cleaning and processing logic
```

---

## **Setup and Installation**

### **1. Clone the Repository**
```bash
git clone <your-repo-url>
cd IFT-6758B-Milestone-1-main
```

### **2. Set up the Python Environment**
Use **pip** or **Conda** to install the necessary dependencies:

- **Using pip**:
    ```bash
    pip install -r requirements.txt
    ```

- **Using Conda**:
    ```bash
    conda env create -f environment.yml
    conda activate nhl-data-project
    ```

---

## **How to Run the Code**

### **1. Data Acquisition**
The `1_data_acquisition.py` script retrieves **play-by-play data** for regular season and playoff games.

- **Example Usage**:
    ```python
    from ift6758.data import data_acquisition

    # Download game data for a specific game ID
    data = data_acquisition.download_game_data(game_id="2022030411")
    ```

- **Caching**: Data is saved locally to avoid repeated downloads. Ensure the cache path is correctly configured.

---

### **2. Interactive Debugging Tool**
The `2_interactive_debugging_nhl_data.py` script launches an **interactive tool** for navigating through game events.

- **Usage**:
    ```python
    from ift6758.features import interactive_debugging

    # Launch the interactive debugging tool
    interactive_debugging.launch_tool(season="2019", game_type="regular")
    ```
- **Functionality**: 
    - Flip through individual events of a game.
    - **Plot event coordinates** on the provided rink image.
    - Switch between **regular season and playoffs**.

---

### **3. Tidy Data Creation**
The `tidy_data.py` script processes the raw event data into a **tidy Pandas DataFrame**.

- **Usage**:
    ```python
    from ift6758.features import tidy_data

    # Process events into a tidy DataFrame
    df = tidy_data.process_events(["shots", "goals"])
    print(df.head())
    ```
- **Output**: Includes fields like **event time, period, team, shooter, goalie, coordinates, and shot type**.

---

### **4. Simple Visualizations**
Generate **basic visualizations** using the `simple_visualization.py` script.

- **Example**: 
    ```python
    from ift6758.visualizations import simple_visualization

    # Plot comparison of shot types and goals
    simple_visualization.plot_shot_types_with_goals()
    ```

- **Available Figures**:
    - Shot types with goal overlays.
    - Shot probability vs distance from the net.
    - Goal percentage by shot type and distance.

---

### **5. Advanced Visualizations: Shot Maps**
Use `5_advanced_visualization.py` to create **interactive shot maps**.

- **Example Usage**:
    ```python
    from ift6758.visualizations import advanced_visualization

    # Generate an interactive shot map for a given team and season
    advanced_visualization.plot_shot_map(team="Colorado Avalanche", season="2016-17")
    ```
- **Features**:
    - KDE-based heatmaps showing shot patterns.
    - Select any team and season (2016-17 to 2020-21).
    - **Interactive output** embedded as HTML.

---

## **Blog Post Submission**
- **Figures and analysis** from this project are compiled in a **Jekyll-based blog post**.
- The **interactive shot maps** are embedded as HTML elements for easy navigation.
- Instructions for setting up the blog post are provided separately, but can be easily hosted via **GitHub Pages**.

---

## **Key Figures and Insights**
- **Comparison of Shot Types**: Visualizes the relationship between different shot types and their goal conversion.
- **Shot Distance vs Goal Probability**: Analyzes the impact of shot distance on scoring chances.
- **Shot Maps**: Heatmaps highlighting offensive shot patterns for different NHL teams across seasons.

---

## **Contact Information**
If you encounter any issues or have questions, feel free to contact any of the team members:

- **Kiruthika Subramani**: [kiruthika.subramani@umontreal.ca](mailto:kiruthika.subramani@umontreal.ca)  
- **Tikshan Kumar Soobanah**: [tikshan.kumar.soobanah@umontreal.ca](mailto:tikshan.kumar.soobanah@umontreal.ca)  
- **Yizhan Li**: [yizhan.li@umontreal.ca](mailto:yizhan.li@umontreal.ca)  

---

## **Acknowledgments**
- Data is provided by the **NHL stats API**.
- Inspired by **HockeyViz** visualizations.
- Special thanks to the **IFT 6758 course team** for guidance and resources.



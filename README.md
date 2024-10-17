

# **IFT 6758 Project: Milestone 1**

## **Team Members**
| Name                    | Email                                    |
|-------------------------|------------------------------------------|
| Kiruthika Subramani     | [kiruthika.subramani@umontreal.ca](mailto:kiruthika.subramani@umontreal.ca) |
| Tikshan Kumar Soobanah  | [tikshan.kumar.soobanah@umontreal.ca](mailto:tikshan.kumar.soobanah@umontreal.ca) |
| Yizhan Li               | [yizhan.li@umontreal.ca](mailto:yizhan.li@umontreal.ca) |

---

## **Project Overview**
This project focuses on **analyzing NHL hockey data** using the NHL stats API. The primary tasks include:
1. **Data acquisition and caching** for regular season and playoff games.
2. **Processing raw event data** into tidy dataframes.
3. **Exploratory visualizations** to gain insights into player and team performance.
4. **Building interactive tools** to explore and debug play-by-play data.
5. **Creating advanced shot maps** for deeper analysis.
6. **Presenting results in a blog post** with static and interactive visualizations.

---

## **Project Structure**

```
IFT-6758B-Milestone-1-main/
│
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── setup.py                    # Installation setup script
├── environment.yml             # Conda environment configuration
│
├── figures/                    # Generated figures and outputs
│   ├── Advanced_Visualization.png
│   ├── Comparison_of_Shot_Types_with_Goals_Overlay_(Season_2016-2017).png
│   ├── Comparison_of_Shot_Types_with_Goals_Overlay_for_overall_data.png
│   ├── Goal_Percentage_by_Distance_Range_and_Shot_Type_(2018-19_Season).png
│   ├── Goal_Percentage_by_Distance_Range_and_Shot_Type_(2018-19).png
│   ├── Goal-to-Shot_Ratio_for_All_Shot_Types_in_overall_data.png
│   ├── Interactive_Debugging_Output.png
│   ├── Interactive_debugging.png
│   ├── Shot_Distance_vs_Goal_Probability.png
│   ├── Shot_Distance_Distribution_by_Goal_Outcome.png
│   ├── Shot_on_goal_probability.png
│   ├── nhl_rink.png            # Ice rink image for plotting events
│   └── raw_Downloaded_Data_-_Json_Files_in_Drive.pdf
│
├── ift6758/                    # Main code modules
│   ├── data/
│   │   ├── 1_data_acquisition.py
│   │   ├── 2_data_acquisition_method_2.py
│   │   ├── Final_Dataframe.zip
│   │   └── Sample_Json_Downloaded.json
│   │
│   ├── features/
│   │   ├── 2_interactive_debugging_nhl_data.py
│   │   ├── exploring_the_json_files(_additional_eda).py
│   │   └── tidy_data.py
│   │
│   └── visualizations/
│       ├── 5_advanced_visualization.py
│       └── simple__visualization_.py
│
├── notebooks/                 # Jupyter Notebooks
│   ├── 1_Data_Acquisition.ipynb
│   ├── 2_Data_Acquisition_Method_2.ipynb
│   ├── 2_Interactive_Debugging_NHL_Data.ipynb
│   ├── 5_Advanced_Visualization_.zip
│   ├── Exploring_the_Json_Files(_Additional_EDA).ipynb
│   ├── Simple__visualizations.ipynb
│   └── Tidy_Data.ipynb
```

---

## **Setup and Installation**

### **1. Clone the Repository**
```bash
git clone <your-repo-url>
cd IFT-6758B-Milestone-1-main
```

### **2. Set up the Environment**
Install dependencies using either **pip** or **Conda**.

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
Use **`1_data_acquisition.py`** to download and cache game data.

```python
from ift6758.data import data_acquisition

# Download data for a game
data = data_acquisition.download_game_data(game_id="2022030411")
```

---

### **2. Interactive Debugging Tool**
Launch the **interactive tool** from `2_interactive_debugging_nhl_data.py`.

```python
from ift6758.features import interactive_debugging

# Launch the interactive tool
interactive_debugging.launch_tool(season="2019", game_type="regular")
```

---

### **3. Tidy Data Creation**
Convert raw events into a **Pandas DataFrame** using `tidy_data.py`.

```python
from ift6758.features import tidy_data

# Create a tidy DataFrame for shots and goals
df = tidy_data.process_events(["shots", "goals"])
print(df.head())
```

---

### **4. Visualizations**
Generate visualizations using `simple__visualization_.py` and `5_advanced_visualization.py`.

- **Simple Visualizations**:
    ```python
    from ift6758.visualizations import simple_visualization

    # Plot shot types with goals overlay
    simple_visualization.plot_shot_types_with_goals()
    ```

- **Advanced Visualizations**:
    ```python
    from ift6758.visualizations import advanced_visualization

    # Create an advanced shot map
    advanced_visualization.plot_shot_map(team="Colorado Avalanche", season="2016-17")
    ```

---

## **Figure Overview**

| **Figure Name** | **Description** |
|----------------|-----------------|
| **Advanced_Visualization.png** | KDE-based shot map for a team. |
| **Comparison_of_Shot_Types_with_Goals_Overlay_(Season_2016-2017).png** | Comparison of shot types with goals overlay for the 2016-17 season. |
| **Comparison_of_Shot_Types_with_Goals_Overlay_for_overall_data.png** | Comparison of shot types across all seasons. |
| **Goal_Percentage_by_Distance_Range_and_Shot_Type_(2018-19_Season).png** | Goal percentage by distance and shot type for 2018-19. |
| **Goal-to-Shot_Ratio_for_All_Shot_Types_in_overall_data.png** | Goal-to-shot ratio showing dangerous shot types. |
| **Interactive_Debugging_Output.png** | Screenshot of the interactive tool output. |
| **Shot_Distance_vs_Goal_Probability.png** | Relationship between shot distance and goal probability. |
| **Shot_Distance_Distribution_by_Goal_Outcome.png** | Distribution of shot distances by goal outcome. |
| **Shot_on_goal_probability.png** | Probability of shots leading to goals. |
| **nhl_rink.png** | Ice rink image used for plotting events. |
| **raw_Downloaded_Data_-_Json_Files_in_Drive.pdf** | Report on raw data downloaded from the NHL API. |

---

## **Running Notebooks on Google Colab**
All notebooks are compatible with **Google Colab**. Open any notebook by:

1. Upload the notebook to [Google Colab](https://colab.research.google.com/).
2. Install the required dependencies in Colab by running:
   ```bash
   !pip install -r requirements.txt
   ```

**Notebooks Available**:
- **1_Data_Acquisition.ipynb**: Data download and caching logic.
- **2_Data_Acquisition_Method_2.ipynb**: Alternative data retrieval.
- **2_Interactive_Debugging_NHL_Data.ipynb**: Interactive debugging tool.
- **Exploring_the_Json_Files(_Additional_EDA).ipynb**: Exploratory Data Analysis.
- **Simple__visualizations.ipynb**: Generate basic visualizations.
- **Tidy_Data.ipynb**: Data cleaning and tidying logic.

---

## **Acknowledgments**
- NHL stats API for providing the data.
- Inspired by HockeyViz for visualization techniques.
- Special thanks to the IFT 6758 course team for their guidance.

---

## **Contact Information**
| Name                    | Email                                    |
|-------------------------|------------------------------------------|
| Kiruthika Subramani     | [kiruthika.subramani@umontreal.ca](mailto:kiruthika.subramani@umontreal.ca) |
| Tikshan Kumar Soobanah  | [tikshan.kumar.soobanah@umontreal.ca](mailto:tikshan.kumar.soobanah@umontreal.ca) |
| Yizhan Li               | [yizhan.li@umontreal.ca](mailto:yizhan.li@umontreal.ca) |


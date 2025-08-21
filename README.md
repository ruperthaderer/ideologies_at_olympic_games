# Olympic Medal Efficiency and Political Systems

This project explores the relationship between Olympic medal efficiency and different political systems throughout the 20th and early 21st centuries. Using athlete-level Olympic data combined with custom-labeled political regime periods per country, we investigate whether certain systems tend to produce higher medal efficiency relative to the number of participants.

## Overview

- **Dataset**: The project uses the [Kaggle Olympic Athlete Events dataset](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results).
- **Objective**: Analyze and visualize Olympic medal efficiency over time and across political systems.
- **Efficiency Definition**: Weighted medal points (Gold = 3, Silver = 2, Bronze = 1) divided by the number of athletes sent.
- **Period Mapping**: Countries are manually labeled with political regimes (e.g., democracy, monarchy, socialism) by year.

## Main Script

- `final.py`: Runs the entire pipeline:
  - Data loading and preprocessing
  - Merging Olympic data with political periods
  - Computing efficiency metrics
  - Creating all four plots:
    - Circular barplot
    - Streamgraph
    - Treemap
    - Violin plot

## Supporting Files

The following Python files contain helper functions used by `final.py`:

- `csv_action.py`
- `efficiency_weighted_medals.py`
- `efficiency_total_medals.py`
- `medaillen_gleichwertig.py`

These files should remain in the project folder to ensure that `final.py` executes correctly.

## Visualizations

- **Treemap**: Weighted medal points by country and political system.
- **Circular Bar Plot**: Average medal efficiency per system.
- **Streamgraph**: Temporal development of medal efficiency.
- **Violin Plot**: Distribution of yearly efficiency values by system.

## Technologies Used

- Python: `pandas`, `matplotlib`, `seaborn`, `squarify`, `numpy`
- Plot export with `matplotlib.pyplot.savefig()`
- Script-based execution (no notebook dependency)

## How to Run

1. Ensure that `athlete_events.csv` and `noc_periods_sorted.csv` are in the root directory.
2. Run:

   ```bash
   python final.py
   ```

3. Output plots will be saved in the root or `plots/` directory.

## Report

A detailed report including political regime mapping, methodology, and interpretation of the results is available in `haderer_rupert.pdf`.

## Author

Rupert Haderer  
Bachelor of Computer Science  
This project was originally developed as part of a university data analysis course and later refined as a portfolio piece.

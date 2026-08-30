# GlucoView
#### Description:
This project is a web application using Streamlit that lets users upload continuous glucose monitor (CGM) data as a CSV file and see a visual analysis of it. The data should have two main columns: a timestamp column and a glucose value column (in mg/dL), which the user selects after uploading.

The analysis includes calculating the rate of change and visualizing it with red lines marking the threshold the change must exceed (2, -2) to be flagged as rapid — a warning is shown if it does. The project also calculates the percentage of time glucose levels are in the normal range (70-180), low (<70), or high (>180). Finally, it plots the glucose value distribution over time.

## Files

- **`project.py`** — the main application file. Contains `main()`, which builds the Streamlit interface, along with the core functions: `load_data()` (reads the CSV and lets the user pick columns), `validate()` (cleans and checks the data), `calculate_rate_of_change()` (computes glucose change per minute), `rapid_rate_of_change()` (flags rapid swings), `percentage_of_time_in_range()` (calculates Low/In Range/High percentages), and two plotting functions for the charts.
- **`test_project.py`** — pytest tests for `validate`, `calculate_rate_of_change`, `rapid_rate_of_change`, and `percentage_of_time_in_range`.
- **`requirements.txt`** — lists the dependencies needed to run the project (`streamlit`, `pandas`, `plotly`, `pytest`).
- **`test_data.csv`** — a small sample CGM file

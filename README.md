    # GlucoView
    #### Description:
    This project is a web application using Streamlit that lets users upload continuous glucose monitor (CGM) data as a CSV file and see a visual analysis of it. The data should have two main columns: a timestamp column and a glucose value column (in mg/dL), which the user selects after uploading.

    The analysis includes calculating the rate of change and visualizing it with red lines marking the threshold the change must exceed (2, -2) to be flagged as rapid — a warning is shown if it does. The project also calculates the percentage of time glucose levels are in the normal range (70-180), low (<70), or high (>180). Finally, it plots the glucose value distribution over time.
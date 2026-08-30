import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    #page setup
    st.set_page_config(page_title="Glucose Data Analysis", layout="wide")
    st.title("Glucose Data Analysis")
    file_uploaded = st.file_uploader("Choose a CSV file with \"timestamp\" and \"glucose_value_mg_dl\" columns", type="csv")

    if file_uploaded:
        df = load_data(file_uploaded)
        st.success("File uploaded successfully!")

        # display the first 5 rows
        st.subheader("Data Preview")
        st.data_editor(df.head(), hide_index=True,)

        # calculate rate of change
        df = calculate_rate_of_change(df)
        st.subheader("Rate of Change")
        st.plotly_chart(plot_rate_of_change(df), use_container_width=True)
        if(rapid_rate_of_change(df).any()):
            st.warning("Rapid changes in glucose levels detected!")

        # calculate Percentage of Time in Range and Plot Glucose/Time
        s = percentage_of_time_in_range(df)
        st.subheader("Percentage of Time in Range")
        st.data_editor(s, 
                       width="content",
                       column_config=
                       {
                           "count": st.column_config.NumberColumn("Percentage", format="%d%%"),
                       })

        st.plotly_chart(plot_glucose_distribution(df), use_container_width=True)

    else:
        st.info("Upload a CSV file to begin.")

def load_data(file_uploaded):
    raw_data = pd.read_csv(file_uploaded)
    st.subheader("Select your columns")
    timestamp_col = st.selectbox("Select the timestamp column", raw_data.columns)
    glucose_col = st.selectbox("Select the glucose value column", raw_data.columns)
    data = validate(raw_data, timestamp_col, glucose_col)
    return data


def validate(df, timestamp_col, glucose_col):
    if timestamp_col not in df.columns or glucose_col not in df.columns:
        raise ValueError("Selected columns are not in the DataFrame.")
    if timestamp_col == glucose_col:
        raise ValueError("Timestamp and glucose value columns must be different.")

    data = df[[timestamp_col, glucose_col]].copy()
    data.columns = ["timestamp", "glucose_value_mg_dl"]
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data["glucose_value_mg_dl"] = pd.to_numeric(data["glucose_value_mg_dl"])
    data = data.drop_duplicates(subset = ["timestamp"]).reset_index(drop=True)

    if data.empty:
        raise ValueError("The DataFrame is empty after selecting the columns.")
    
    return data
        

def calculate_rate_of_change(df):
    denominator = df["timestamp"].diff().dt.total_seconds() / 60 
    denominator = denominator.replace(0, pd.NA)
    df["BG Rate of Change"] = df["glucose_value_mg_dl"].diff()/denominator
    return df

def rapid_rate_of_change(df):
    df = df.copy()
    df["rapid_change"] = df["BG Rate of Change"].abs() > 2.0
    return df["rapid_change"]

def plot_rate_of_change(df):
    fig = px.line(df,
                  x="timestamp",
                  y="BG Rate of Change",
                  title="Rate of Change of Glucose")
    fig.add_hline(y=2.0, line_dash="dash", line_color="red")
    fig.add_hline(y=-2.0, line_dash="dash", line_color="red")
    return fig

def percentage_of_time_in_range(df):
    ranges = [-1, 69, 180, 1000] #0-70 -> Low, 70-180 -> In Range 180+ -> High
    labels = pd.cut(df["glucose_value_mg_dl"], bins=ranges, labels=["Low", "In Range", "High"])
    result = labels.value_counts()
    return result / result.sum() * 100

def plot_glucose_distribution(df):
    fig = px.line(df, x="timestamp", y="glucose_value_mg_dl", title="Glucose Value Distribution Over Time")
    return fig


if __name__ == "__main__":
    main()
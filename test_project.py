from project import validate 
from project import calculate_rate_of_change 
from project import percentage_of_time_in_range
from project import rapid_rate_of_change
import pandas as pd
import pytest

df = pd.read_csv("test_data.csv")
df = validate(df, "time", "bg")

def test_validate():
    assert "timestamp" in df.columns
    assert "glucose_value_mg_dl" in df.columns
    assert df.duplicated(subset=["timestamp"]).sum() == 0
    assert list(df.columns) == ["timestamp", "glucose_value_mg_dl"]
    with pytest.raises(ValueError):
        validate(df, "time", "time")



def test_calculate_rate_of_change():
    test_ROC = calculate_rate_of_change(df)
    assert test_ROC["BG Rate of Change"].isnull().sum() == 1
    assert test_ROC["BG Rate of Change"].iloc[1] == -4 #180-200/5

def test_rapid_rate_of_change():
    test_RoC = rapid_rate_of_change(df)
    # This assertion changes based on the dataset, but for this dataset, there are rapid changes in glucose levels detected
    assert list(test_RoC) == [False, True, False, True]

def test_percentage_of_time_in_range():
    test_TIR = percentage_of_time_in_range(df)
    # asserting with known values from the dataset, these values change if the dataset changes
    assert test_TIR["Low"] == 0.0
    assert test_TIR["High"] == 25.0
    assert test_TIR["In Range"] == 75.0
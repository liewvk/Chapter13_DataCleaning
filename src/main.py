import pandas as pd
import numpy as np
from pathlib import Path


def get_grade(score):
    if score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"


def min_max_scale(column):
    minimum = column.min()
    maximum = column.max()

    if maximum == minimum:
        return column * 0

    return (column - minimum) / (maximum - minimum)


def main():
    data_file = Path("data") / "students_dirty.csv"
    output_file = Path("outputs") / "students_cleaned.csv"

    output_file.parent.mkdir(exist_ok=True)

    df = pd.read_csv(data_file)

    print("Original Data")
    print("-------------")
    print(df)

    print()
    print("Missing Values Before Cleaning")
    print("------------------------------")
    print(df.isnull().sum())

    # Remove extra spaces from text columns
    df["Name"] = df["Name"].str.strip()
    df["Gender"] = df["Gender"].str.strip()

    # Convert Score column to numeric values
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")

    # Replace invalid score and attendance values with missing values
    df.loc[(df["Score"] < 0) | (df["Score"] > 100), "Score"] = np.nan
    df.loc[(df["Attendance"] < 0) | (df["Attendance"] > 100), "Attendance"] = np.nan

    # Fill missing numerical values with averages
    df["Score"] = df["Score"].fillna(df["Score"].mean())
    df["Attendance"] = df["Attendance"].fillna(df["Attendance"].mean())

    # Round numerical values
    df["Score"] = df["Score"].round(2)
    df["Attendance"] = df["Attendance"].round(2)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Standardize gender categories
    df["Gender"] = df["Gender"].str.lower()

    df["Gender"] = df["Gender"].replace({
        "f": "Female",
        "female": "Female",
        "m": "Male",
        "male": "Male"
    })

    # Create new columns
    df["Result"] = np.where(df["Score"] >= 50, "Pass", "Fail")
    df["Grade"] = df["Score"].apply(get_grade)

    # Encode gender as numbers
    df["GenderCode"] = df["Gender"].map({
        "Female": 0,
        "Male": 1
    })

    # Scale numerical columns
    df["ScoreScaled"] = min_max_scale(df["Score"]).round(3)
    df["AttendanceScaled"] = min_max_scale(df["Attendance"]).round(3)

    print()
    print("Cleaned Data")
    print("------------")
    print(df)

    print()
    print("Missing Values After Cleaning")
    print("-----------------------------")
    print(df.isnull().sum())

    print()
    print("Summary")
    print("-------")
    print(f"Number of rows after cleaning: {len(df)}")
    print(f"Average score: {df['Score'].mean():.2f}")
    print(f"Average attendance: {df['Attendance'].mean():.2f}")
    print(f"Students passed: {(df['Result'] == 'Pass').sum()}")
    print(f"Students failed: {(df['Result'] == 'Fail').sum()}")

    df.to_csv(output_file, index=False)

    print()
    print(f"Cleaned data saved to: {output_file}")


main()


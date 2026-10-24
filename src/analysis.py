import pandas as pd


def average_unemployment_by_year(df):
    """
    Calculate the average unemployment rate for each year.
    """
    result = (
        df
        .groupby("year", as_index=False)["unemployment_rate"]
        .mean()
        .sort_values("year")
    )

    return result


def average_unemployment_by_sex(df):
    """
    Calculate the average unemployment rate for each sex.
    """
    result = (
        df
        .groupby("sex", as_index=False)["unemployment_rate"]
        .mean()
        .sort_values("unemployment_rate", ascending=False)
    )

    return result


def average_unemployment_by_age(df):
    """
    Calculate the average unemployment rate for each age group.
    """
    result = (
        df
        .groupby("age_group", as_index=False)["unemployment_rate"]
        .mean()
        .sort_values("unemployment_rate", ascending=False)
    )

    return result


def average_unemployment_by_education(df):
    """
    Calculate the average unemployment rate for each education level.
    """
    result = (
        df
        .groupby("education_level", as_index=False)["unemployment_rate"]
        .mean()
        .sort_values("unemployment_rate", ascending=False)
    )

    return result


def latest_year_data(df):
    """
    Return data for the most recent year available.
    """
    latest_year = df["year"].max()

    result = df[df["year"] == latest_year]

    return result


def calculate_change(df, start_year, end_year):
    """
    Calculate the change in average unemployment rate
    between two years.
    """
    start_data = df[df["year"] == start_year]
    end_data = df[df["year"] == end_year]

    if start_data.empty or end_data.empty:
        return None

    start_rate = start_data["unemployment_rate"].mean()
    end_rate = end_data["unemployment_rate"].mean()

    change = end_rate - start_rate

    return {
        "start_year": start_year,
        "end_year": end_year,
        "start_rate": start_rate,
        "end_rate": end_rate,
        "change": change
    }
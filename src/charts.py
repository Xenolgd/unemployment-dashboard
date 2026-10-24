import pandas as pd
import plotly.express as px



# ---------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------


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



def average_unemployment_by_duration(df):
    """
    Calculate the average unemployment rate by unemployment duration.
    """
    if "unemployment_duration" not in df.columns:
        return pd.DataFrame()


    result = (
        df
        .groupby("unemployment_duration", as_index=False)["unemployment_rate"]
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



# ---------------------------------------------------------
# Visualization functions
# ---------------------------------------------------------


def create_year_trend_chart(df):
    """
    Create a line chart showing the unemployment rate over time.
    """
    fig = px.line(
        df,
        x="year",
        y="unemployment_rate",
        markers=True,
        title="Unemployment rate over time",
        labels={
            "year": "Year",
            "unemployment_rate": "Unemployment rate (%)"
        }
    )


    fig.update_layout(
        template="plotly_white",
        title_x=0.05
    )


    return fig



def create_sex_comparison_chart(df):
    """
    Create a bar chart comparing unemployment by sex.
    """
    fig = px.bar(
        df,
        x="sex",
        y="unemployment_rate",
        color="sex",
        title="Average unemployment rate by sex",
        labels={
            "sex": "Sex",
            "unemployment_rate": "Unemployment rate (%)"
        }
    )


    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        title_x=0.05
    )


    return fig



def create_age_comparison_chart(df):
    """
    Create a bar chart comparing unemployment by age group.
    """
    fig = px.bar(
        df,
        x="age_group",
        y="unemployment_rate",
        color="age_group",
        title="Average unemployment rate by age group",
        labels={
            "age_group": "Age group",
            "unemployment_rate": "Unemployment rate (%)"
        }
    )


    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        title_x=0.05
    )


    return fig



def create_education_comparison_chart(df):
    """
    Create a bar chart comparing unemployment by education level.
    """
    fig = px.bar(
        df,
        x="education_level",
        y="unemployment_rate",
        color="education_level",
        title="Average unemployment rate by education level",
        labels={
            "education_level": "Education level",
            "unemployment_rate": "Unemployment rate (%)"
        }
    )


    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        title_x=0.05
    )


    return fig



def create_duration_comparison_chart(df):
    """
    Create a bar chart comparing unemployment by duration.
    """
    fig = px.bar(
        df,
        x="unemployment_duration",
        y="unemployment_rate",
        color="unemployment_duration",
        title="Average unemployment rate by duration",
        labels={
            "unemployment_duration": "Unemployment duration",
            "unemployment_rate": "Unemployment rate (%)"
        }
    )


    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        title_x=0.05
    )


    return fig


# ---------------------------------------------------------
# Cross-dimensional analysis functions
# ---------------------------------------------------------


def average_unemployment_by_sex_age(df):
    """
    Calculate the average unemployment rate
    for each combination of sex and age group.
    """
    result = (
        df
        .groupby(["sex", "age_group"], as_index=False)["unemployment_rate"]
        .mean()
    )


    return result



def average_unemployment_by_sex_education(df):
    """
    Calculate the average unemployment rate
    for each combination of sex and education level.
    """
    result = (
        df
        .groupby(["sex", "education_level"], as_index=False)["unemployment_rate"]
        .mean()
    )


    return result



def average_unemployment_by_age_education(df):
    """
    Calculate the average unemployment rate
    for each combination of age group and education level.
    """
    result = (
        df
        .groupby(["age_group", "education_level"], as_index=False)["unemployment_rate"]
        .mean()
    )


    return result



# ---------------------------------------------------------
# Cross-dimensional visualization functions
# ---------------------------------------------------------


def create_sex_age_grouped_chart(df):
    """
    Create a grouped bar chart comparing unemployment
    by sex and age group.
    """
    fig = px.bar(
        df,
        x="age_group",
        y="unemployment_rate",
        color="sex",
        barmode="group",
        title="Average unemployment rate by sex and age group",
        labels={
            "age_group": "Age group",
            "unemployment_rate": "Unemployment rate (%)",
            "sex": "Sex"
        }
    )


    fig.update_layout(
        template="plotly_white",
        title_x=0.05
    )


    return fig



def create_sex_education_grouped_chart(df):
    """
    Create a grouped bar chart comparing unemployment
    by sex and education level.
    """
    fig = px.bar(
        df,
        x="education_level",
        y="unemployment_rate",
        color="sex",
        barmode="group",
        title="Average unemployment rate by sex and education level",
        labels={
            "education_level": "Education level",
            "unemployment_rate": "Unemployment rate (%)",
            "sex": "Sex"
        }
    )


    fig.update_layout(
        template="plotly_white",
        title_x=0.05
    )


    return fig



def create_age_education_heatmap(df):
    """
    Create a heatmap showing unemployment rate
    by age group and education level.
    """
    heatmap_data = df.pivot(
        index="age_group",
        columns="education_level",
        values="unemployment_rate"
    )


    fig = px.imshow(
        heatmap_data,
        text_auto=".1f",
        aspect="auto",
        color_continuous_scale="Reds",
        title="Average unemployment rate by age group and education level",
        labels={
            "x": "Education level",
            "y": "Age group",
            "color": "Unemployment rate (%)"
        }
    )


    fig.update_layout(
        template="plotly_white",
        title_x=0.05
    )


    return fig
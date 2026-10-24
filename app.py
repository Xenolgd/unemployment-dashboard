import streamlit as st
import pandas as pd


from src.charts import (
    average_unemployment_by_year,
    average_unemployment_by_sex,
    average_unemployment_by_age,
    average_unemployment_by_education,
    average_unemployment_by_duration,
    average_unemployment_by_sex_age,
    average_unemployment_by_sex_education,
    average_unemployment_by_age_education,
    latest_year_data,
    calculate_change,
    create_year_trend_chart,
    create_sex_comparison_chart,
    create_age_comparison_chart,
    create_education_comparison_chart,
    create_duration_comparison_chart,
    create_sex_age_grouped_chart,
    create_sex_education_grouped_chart,
    create_age_education_heatmap
)


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------


st.set_page_config(
    page_title="Unemployment Rate Dashboard",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------


DATA_PATH = "data/processed/unemployment_clean.csv"

DATA_SOURCE_URL = "https://www.data.gouv.fr/datasets/activite-emploi-et-chomage-series-longues?resource_id=03c6dc89-35e9-4f1c-8d0b-aabc018cff02"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


df = load_data()


# ---------------------------------------------------------
# Sidebar : student information
# ---------------------------------------------------------


st.sidebar.image(
    "assets/images/image.png",
    width=240
)


st.sidebar.subheader("Alexandre Le Galliard")


st.sidebar.markdown(
    """
    🎓 **Program:** Engineering Degree  
    📅 **Year:** Second Year of Engineering Studies  
    📧 **Email:** [alexandre.le-galliard@efrei.net](mailto:alexandre.le-galliard@efrei.net)  
    💼 **LinkedIn:** [My LinkedIn profile](https://www.linkedin.com/in/alexandre-le-galliard)  
    💻 **GitHub:** [My GitHub](https://github.com/Xenolgd/unemployment-dashboard)


    📚 **Course:** Data Analysis & Visualization  
    👨‍🏫 **Project proposed by:** Prof. Mano Mathew  
    📧 **Professor contact:** [mano.mathew@efrei.fr](mailto:mano.mathew@efrei.fr)
    """
)


st.sidebar.markdown("---")


# ---------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------


st.sidebar.header("Filters")


year_min = int(df["year"].min())
year_max = int(df["year"].max())


year_range = st.sidebar.slider(
    "Select year range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)


sex_options = df["sex"].dropna().unique().tolist()
selected_sex = st.sidebar.multiselect(
    "Select sex",
    options=sex_options,
    default=sex_options
)


age_options = df["age_group"].dropna().unique().tolist()
selected_age = st.sidebar.multiselect(
    "Select age group",
    options=age_options,
    default=age_options
)


education_options = df["education_level"].dropna().unique().tolist()
selected_education = st.sidebar.multiselect(
    "Select education level",
    options=education_options,
    default=education_options
)


duration_options = df["unemployment_duration"].dropna().unique().tolist()
selected_duration = st.sidebar.multiselect(
    "Select unemployment duration",
    options=duration_options,
    default=duration_options
)


# ---------------------------------------------------------
# Apply filters
# ---------------------------------------------------------


df_filtered = df[
    (df["year"].between(year_range[0], year_range[1]))
    & (df["sex"].isin(selected_sex))
    & (df["age_group"].isin(selected_age))
    & (df["education_level"].isin(selected_education))
]


if duration_options:
    df_filtered = df_filtered[
        df_filtered["unemployment_duration"].isin(selected_duration)
    ]


# ---------------------------------------------------------
# Title and introduction
# ---------------------------------------------------------


st.markdown(
    """
    <h1 style="text-align: center;">
        📊 Why do unemployment rates in France differ by sex, age group, 
        education level and unemployment duration?
    </h1>
    """,
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns([1, 2, 1])


with col2:
    st.image(
        "assets/images/banner.png",
        width=700
    )


st.markdown(
    """
    ### 🎯 Why does this matter?

    Unemployment is a key indicator of economic and social well-being.  
    This dashboard explores why unemployment rates differ across sex, age groups, 
    education levels and unemployment durations in France.


    **Data source:** [data.gouv.fr — Activité, emploi et chômage, séries longues](https://www.data.gouv.fr/datasets/activite-emploi-et-chomage-series-longues?resource_id=03c6dc89-35e9-4f1c-8d0b-aabc018cff02)
    """
)


# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------


latest_data = latest_year_data(df_filtered)


col1, col2, col3 = st.columns(3)


with col1:
    if not latest_data.empty:
        latest_rate = latest_data["unemployment_rate"].mean()
        latest_year = int(latest_data["year"].max())


        st.metric(
            label=f"Average unemployment rate in {latest_year}",
            value=f"{latest_rate:.1f}%"
        )
    else:
        st.metric(
            label="Latest unemployment rate",
            value="No data"
        )


with col2:
    global_rate = df_filtered["unemployment_rate"].mean()


    st.metric(
        label="Average unemployment rate over selected period",
        value=f"{global_rate:.1f}%"
    )


with col3:
    change_result = calculate_change(
        df_filtered,
        year_range[0],
        year_range[1]
    )


    if change_result:
        change_value = change_result["change"]


        st.metric(
            label=f"Change from {year_range[0]} to {year_range[1]}",
            value=f"{change_value:+.1f} pp"
        )
    else:
        st.metric(
            label="Change over period",
            value="No data"
        )


# ---------------------------------------------------------
# Year trend
# ---------------------------------------------------------


st.markdown(
    """
    <h2 style="
        color: #1E88E5;
        border-left: 6px solid #1E88E5;
        padding-left: 12px;
        margin-top: 30px;
    ">
        📈 Unemployment rate over time
    </h2>
    """,
    unsafe_allow_html=True
)


year_data = average_unemployment_by_year(df_filtered)


if not year_data.empty:
    year_chart = create_year_trend_chart(year_data)
    st.plotly_chart(year_chart, use_container_width=True)


    max_row = year_data.loc[year_data["unemployment_rate"].idxmax()]
    min_row = year_data.loc[year_data["unemployment_rate"].idxmin()]


    st.markdown(
        f"""
        ### 📌 Interpretation


        - The highest average unemployment rate was reached in **{int(max_row['year'])}**, 
          with **{max_row['unemployment_rate']:.1f}%**.
        - The lowest was observed in **{int(min_row['year'])}**, 
          with **{min_row['unemployment_rate']:.1f}%**.


        Unemployment rose after the 2008 financial crisis, peaked in 2015, then 
        gradually decreased until 2022. The COVID-19 pandemic may have temporarily 
        affected the labour market in 2020, without reversing the overall downward trend.
        """
    )
else:
    st.info("No data available for the selected filters.")


# ---------------------------------------------------------
# Sex comparison
# ---------------------------------------------------------


st.markdown(
    """
    <h2 style="
        color: #1E88E5;
        border-left: 6px solid #1E88E5;
        padding-left: 12px;
        margin-top: 30px;
    ">
        ⚧️ Unemployment by sex
    </h2>
    """,
    unsafe_allow_html=True
)


sex_data = average_unemployment_by_sex(df_filtered)


if not sex_data.empty:
    sex_chart = create_sex_comparison_chart(sex_data)
    st.plotly_chart(sex_chart, use_container_width=True)


    highest_sex = sex_data.iloc[0]["sex"]
    highest_rate = sex_data.iloc[0]["unemployment_rate"]


    lowest_sex = sex_data.iloc[-1]["sex"]
    lowest_rate = sex_data.iloc[-1]["unemployment_rate"]


    difference = highest_rate - lowest_rate


    st.markdown(
        f"""
        ### 📌 Interpretation


        - **{highest_sex}** have the highest average unemployment rate: 
          **{highest_rate:.1f}%**.
        - **{lowest_sex}** have the lowest rate: **{lowest_rate:.1f}%**.
        - The difference is **{difference:.1f} percentage points**.


        This gap may reflect career interruptions related to maternity and childcare, 
        a higher prevalence of part-time work among women, and possible discrimination 
        in recruitment or career progression.
        """
    )
else:
    st.info("No sex data available.")


# ---------------------------------------------------------
# Age comparison
# ---------------------------------------------------------


st.markdown(
    """
    <h2 style="
        color: #1E88E5;
        border-left: 6px solid #1E88E5;
        padding-left: 12px;
        margin-top: 30px;
    ">
        👥 Unemployment by age group
    </h2>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <p style="color: #555555; font-size: 14px;">
        <b>Legend:</b> <code>Y</code> = Years, <code>T</code> = To, 
        <code>GE</code> = Greater than or Equal to, 
        <code>_T</code> = Total.
    </p>
    """,
    unsafe_allow_html=True
)


age_data = average_unemployment_by_age(df_filtered)


if not age_data.empty:
    age_chart = create_age_comparison_chart(age_data)
    st.plotly_chart(age_chart, use_container_width=True)


    highest_age = age_data.iloc[0]["age_group"]
    highest_age_rate = age_data.iloc[0]["unemployment_rate"]


    lowest_age = age_data.iloc[-1]["age_group"]
    lowest_age_rate = age_data.iloc[-1]["unemployment_rate"]


    st.markdown(
        f"""
        ### 📌 Interpretation


        - The **{highest_age}** group has the highest average unemployment rate: 
          **{highest_age_rate:.1f}%**.
        - The **{lowest_age}** group has the lowest rate: 
          **{lowest_age_rate:.1f}%**.


        The 15–24 age group is particularly relevant because it represents the 
        transition from education to employment. Young adults often have less 
        professional experience and more temporary contracts, which can make access 
        to stable jobs more difficult.
        """
    )
else:
    st.info("No age group data available.")


# ---------------------------------------------------------
# Education comparison
# ---------------------------------------------------------


st.markdown(
    """
    <h2 style="
        color: #1E88E5;
        border-left: 6px solid #1E88E5;
        padding-left: 12px;
        margin-top: 30px;
    ">
        🎓 Unemployment by education level
    </h2>
    """,
    unsafe_allow_html=True
)


education_data = average_unemployment_by_education(df_filtered)


if not education_data.empty:
    education_chart = create_education_comparison_chart(education_data)
    st.plotly_chart(education_chart, use_container_width=True)


    highest_education = education_data.iloc[0]["education_level"]
    highest_education_rate = education_data.iloc[0]["unemployment_rate"]


    lowest_education = education_data.iloc[-1]["education_level"]
    lowest_education_rate = education_data.iloc[-1]["unemployment_rate"]


    st.markdown(
        f"""
        ### 📌 Interpretation


        - People with **{highest_education}** have the highest average unemployment rate: 
          **{highest_education_rate:.1f}%**.
        - People with **{lowest_education}** have the lowest rate: 
          **{lowest_education_rate:.1f}%**.


        A higher education level is generally associated with better access to more 
        qualified and more stable jobs.
        """
    )
else:
    st.info("No education data available.")


# ---------------------------------------------------------
# Unemployment duration
# ---------------------------------------------------------


st.markdown(
    """
    <h2 style="
        color: #1E88E5;
        border-left: 6px solid #1E88E5;
        padding-left: 12px;
        margin-top: 30px;
    ">
        ⏳ Unemployment by duration
    </h2>
    """,
    unsafe_allow_html=True
)


duration_data = average_unemployment_by_duration(df_filtered)


if not duration_data.empty:
    duration_chart = create_duration_comparison_chart(duration_data)
    st.plotly_chart(duration_chart, use_container_width=True)


    highest_duration = duration_data.iloc[0]["unemployment_duration"]
    highest_duration_rate = duration_data.iloc[0]["unemployment_rate"]


    st.markdown(
        f"""
        ### 📌 Interpretation


        - The highest average unemployment rate is observed for **{highest_duration}**.


        Long-term unemployment can make returning to work more difficult, because 
        professional skills may become less up to date and recruiters may focus more 
        on recent experience.
        """
    )
else:
    st.info("No unemployment duration data available.")


# ---------------------------------------------------------
# Sex and age group
# ---------------------------------------------------------


st.markdown(
    """
    <h2 style="
        color: #1E88E5;
        border-left: 6px solid #1E88E5;
        padding-left: 12px;
        margin-top: 30px;
    ">
        🔎 Unemployment by sex and age group
    </h2>
    """,
    unsafe_allow_html=True
)


sex_age_data = average_unemployment_by_sex_age(df_filtered)


if not sex_age_data.empty:
    sex_age_chart = create_sex_age_grouped_chart(sex_age_data)
    st.plotly_chart(sex_age_chart, use_container_width=True)


    worst_profile = sex_age_data.loc[
        sex_age_data["unemployment_rate"].idxmax()
    ]


    st.markdown(
        f"""
        ### 📌 Interpretation


        - The highest average unemployment rate is observed for 
          **{worst_profile['sex']} aged {worst_profile['age_group']}**, 
          with **{worst_profile['unemployment_rate']:.1f}%**.


        Comparing men and women within the same age group shows whether the gender 
        gap remains constant across generations. A large gap suggests that age and 
        sex interact in access to stable employment.
        """
    )
else:
    st.info("No sex and age data available.")


# ---------------------------------------------------------
# Sex and education level
# ---------------------------------------------------------


st.markdown(
    """
    <h2 style="
        color: #1E88E5;
        border-left: 6px solid #1E88E5;
        padding-left: 12px;
        margin-top: 30px;
    ">
        🔎 Unemployment by sex and education level
    </h2>
    """,
    unsafe_allow_html=True
)


sex_education_data = average_unemployment_by_sex_education(df_filtered)


if not sex_education_data.empty:
    sex_education_chart = create_sex_education_grouped_chart(sex_education_data)
    st.plotly_chart(sex_education_chart, use_container_width=True)


    worst_education_profile = sex_education_data.loc[
        sex_education_data["unemployment_rate"].idxmax()
    ]


    st.markdown(
        f"""
        ### 📌 Interpretation


        - The most affected profile is 
          **{worst_education_profile['sex']} with {worst_education_profile['education_level']}**, 
          with **{worst_education_profile['unemployment_rate']:.1f}%**.


        This chart shows whether education protects men and women in the same way 
        against unemployment. A persistent gender gap across education levels suggests 
        that education alone does not explain the difference.
        """
    )
else:
    st.info("No sex and education data available.")


# ---------------------------------------------------------
# Age group and education level
# ---------------------------------------------------------


st.markdown(
    """
    <h2 style="
        color: #1E88E5;
        border-left: 6px solid #1E88E5;
        padding-left: 12px;
        margin-top: 30px;
    ">
        🔎 Unemployment by age group and education level
    </h2>
    """,
    unsafe_allow_html=True
)


age_education_data = average_unemployment_by_age_education(df_filtered)


if not age_education_data.empty:
    age_education_chart = create_age_education_heatmap(age_education_data)
    st.plotly_chart(age_education_chart, use_container_width=True)


    worst_age_education = age_education_data.loc[
        age_education_data["unemployment_rate"].idxmax()
    ]


    st.markdown(
        f"""
        ### 📌 Interpretation


        - The most affected combination is 
          **{worst_age_education['age_group']} with {worst_age_education['education_level']}**, 
          with **{worst_age_education['unemployment_rate']:.1f}%**.


        This heatmap shows whether a higher education level reduces unemployment 
        equally for young, middle-aged and older workers. It helps identify profiles 
        that combine several risk factors.
        """
    )
else:
    st.info("No age and education data available.")


# ---------------------------------------------------------
# Filtered data
# ---------------------------------------------------------


st.markdown(
    """
    <h2 style="
        color: #1E88E5;
        border-left: 6px solid #1E88E5;
        padding-left: 12px;
        margin-top: 30px;
    ">
        🗂️ Filtered data
    </h2>
    """,
    unsafe_allow_html=True
)


st.dataframe(df_filtered)


# ---------------------------------------------------------
# Data quality & limitations
# ---------------------------------------------------------


st.markdown(
    """
    <h2 style="
        color: #1E88E5;
        border-left: 6px solid #1E88E5;
        padding-left: 12px;
        margin-top: 30px;
    ">
        🧪 Data quality & limitations
    </h2>
    """,
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        label="Missing values",
        value=f"{df_filtered.isna().sum().sum():,}"
    )


with col2:
    st.metric(
        label="Duplicate rows",
        value=f"{df_filtered.duplicated().sum():,}"
    )


with col3:
    st.metric(
        label="Rows after filtering",
        value=f"{len(df_filtered):,}"
    )


st.info(
    f"""
    The dataset comes from
    [data.gouv.fr — Activité, emploi et chômage, séries longues]({DATA_SOURCE_URL})
    and was cleaned before analysis. The metrics above report missing values
    and duplicate rows in the cleaned, filtered dataset; they do not measure
    all possible data quality issues.

    Methodological limitation: the dashboard calculates unweighted averages
    of the selected published unemployment rates, rather than
    population-weighted rates. Some selections may combine total categories
    and overlapping subgroups. The displayed averages should therefore not
    be interpreted as official national unemployment rates.

    The analysis describes observed differences and trends; it does not
    establish causal relationships. Comparisons over time may also be
    affected by changes in survey methods and population coverage.

    A future improvement would be to select consistent statistical series
    for each chart, keeping totals separate from subgroups.
    """
)


# ---------------------------------------------------------
# Key insights & next steps
# ---------------------------------------------------------


st.markdown(
    """
    <h2 style="
        color: #1E88E5;
        border-left: 6px solid #1E88E5;
        padding-left: 12px;
        margin-top: 30px;
    ">
        💡 Key insights & next steps
    </h2>
    """,
    unsafe_allow_html=True
)


st.success(
    """
    **Key insights**


    - Unemployment increased after the 2008 financial crisis, peaked in 2015, then 
      gradually decreased until 2022.
    - Unemployment is not evenly distributed across sex, age groups and education levels.
    - Young people and people with lower education levels tend to be more exposed to 
      unemployment.
    - Long-term unemployment remains an important challenge because it can make 
      returning to work more difficult.


    **Next steps**


    - Compare unemployment trends across French regions.
    - Analyse the impact of economic crises on specific age groups.
    - Study the relationship between education, training and access to stable jobs.
    """
)
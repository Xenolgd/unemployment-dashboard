import os
import pandas as pd


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "extracted")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

DATA_FILE = os.path.join(RAW_DATA_DIR, "DD_EEC_SERIES_data.csv")
METADATA_FILE = os.path.join(RAW_DATA_DIR, "DD_EEC_SERIES_metadata.csv")

OUTPUT_FILE = os.path.join(PROCESSED_DATA_DIR, "unemployment_clean.csv")


# ---------------------------------------------------------
# Create output folder
# ---------------------------------------------------------

os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)


# ---------------------------------------------------------
# Load raw data
# ---------------------------------------------------------

def load_csv(path):
    """
    Load a CSV file and try common encodings.
    """
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            df = pd.read_csv(
                path,
                sep=";",
                encoding=encoding,
                low_memory=False
            )
            print(f"File loaded successfully with encoding: {encoding}")
            return df
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Could not read the file: {path}")


# ---------------------------------------------------------
# Basic exploration
# ---------------------------------------------------------

def explore_data(df, name="Dataset"):
    """
    Print basic information about the dataset.
    """
    print(f"\n===== {name} =====")
    print("Shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst rows:")
    print(df.head())

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nDuplicated rows:")
    print(df.duplicated().sum())


# ---------------------------------------------------------
# Cleaning functions
# ---------------------------------------------------------

def clean_column_names(df):
    """
    Standardize column names.
    """
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.upper()
        .str.replace(" ", "_")
    )
    return df


def remove_duplicates(df):
    """
    Remove exact duplicated rows.
    """
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    print(f"\nDuplicates removed: {before - after}")
    return df


def convert_data_types(df):
    """
    Convert columns to the correct data types.
    """
    df = df.copy()

    if "TIME_PERIOD" in df.columns:
        df["TIME_PERIOD"] = pd.to_numeric(
            df["TIME_PERIOD"],
            errors="coerce"
        )

    if "OBS_VALUE" in df.columns:
        df["OBS_VALUE"] = pd.to_numeric(
            df["OBS_VALUE"],
            errors="coerce"
        )

    return df


def filter_valid_observations(df):
    """
    Keep only normal observations.
    """
    if "OBS_STATUS" in df.columns:
        before = len(df)
        df = df[df["OBS_STATUS"] == "A"].copy()
        after = len(df)

        print(f"\nNon-significant observations removed: {before - after}")

    return df


def handle_missing_values(df):
    """
    Remove rows without an observed value.
    """
    before = len(df)
    df = df.dropna(subset=["OBS_VALUE"])
    after = len(df)

    print(f"\nRows with missing OBS_VALUE removed: {before - after}")
    return df


def filter_unemployment_rate(df):
    """
    Keep only unemployment rate observations.
    """
    print("\nAvailable indicators:")
    print(df["EEC_MEASURE"].unique())

    unemployment_codes = [
        "UNEMPRATE",
        "UNEMPRATE_EDUC"
    ]

    df_filtered = df[df["EEC_MEASURE"].isin(unemployment_codes)].copy()

    if df_filtered.empty:
        print("\nNo unemployment rate found.")
        return df_filtered

    print(f"\nUnemployment rate rows kept: {len(df_filtered)}")
    return df_filtered


def create_clean_columns(df):
    """
    Create clear column names for Streamlit.
    """
    df = df.copy()

    column_mapping = {
        "TIME_PERIOD": "year",
        "SEX": "sex",
        "AGE": "age_group",
        "EDUC": "education_level",
        "EEC_MEASURE": "indicator",
        "UNIT_MEASURE": "unit",
        "UNEMPDUR": "unemployment_duration",
        "OBS_VALUE": "unemployment_rate"
    }

    df = df.rename(columns=column_mapping)

    useful_columns = [
        "year",
        "sex",
        "age_group",
        "education_level",
        "indicator",
        "unit",
        "unemployment_duration",
        "unemployment_rate"
    ]

    existing_columns = [
        col for col in useful_columns if col in df.columns
    ]

    df = df[existing_columns]

    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    print(
        f"\nDuplicates removed after selecting useful columns: "
        f"{before - after}"
    )

    return df


def create_readable_labels(df):
    """
    Replace Eurostat codes with readable labels.
    """
    df = df.copy()

    education_labels = {
        "EEC0T1": "No diploma / middle school",
        "EEC2": "CAP / BEP",
        "EEC3": "High school diploma",
        "EEC4T5": "2-year higher education",
        "EEC6T8": "Higher education degree",
        "_T": "Total"
    }

    duration_labels = {
        "ST": "Short-term unemployment",
        "LT": "Long-term unemployment",
        "_T": "Total"
    }

    sex_labels = {
        "M": "Men",
        "F": "Women",
        "_T": "Total"
    }

    if "education_level" in df.columns:
        df["education_level"] = df["education_level"].map(education_labels)

    if "unemployment_duration" in df.columns:
        df["unemployment_duration"] = df["unemployment_duration"].map(duration_labels)

    if "sex" in df.columns:
        df["sex"] = df["sex"].map(sex_labels)

    return df


def validate_data(df):
    """
    Validate the cleaned dataset.
    """
    print("\n===== Validation =====")
    print("Shape:", df.shape)

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nDuplicated rows:")
    print(df.duplicated().sum())

    if "unemployment_rate" in df.columns:
        print("\nUnemployment rate statistics:")
        print(df["unemployment_rate"].describe())


# ---------------------------------------------------------
# Main cleaning pipeline
# ---------------------------------------------------------

def main():
    print("Loading metadata...")
    metadata = load_csv(METADATA_FILE)
    explore_data(metadata, name="Metadata")

    print("\nLoading raw data...")
    data = load_csv(DATA_FILE)
    explore_data(data, name="Raw data")

    print("\nCleaning data...")

    data = clean_column_names(data)
    data = remove_duplicates(data)
    data = convert_data_types(data)
    data = filter_valid_observations(data)
    data = handle_missing_values(data)
    data = filter_unemployment_rate(data)
    data = create_clean_columns(data)
    data = create_readable_labels(data)

    validate_data(data)

    if data.empty:
        print("\nNo data to save. Please check the indicator filter.")
        return

    data.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    print(f"\nClean dataset saved here:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()


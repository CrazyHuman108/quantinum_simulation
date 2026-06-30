import pandas as pd
import os

def CSV_cleanner_and_manger(filepath):
    # Layer 1: clear message for missing file
    if not os.path.isfile(filepath):
        raise FileNotFoundError(
            f"No file found at: {os.path.abspath(filepath)}\n"
            f"Check spelling and that the file exists."
        )

    # Layer 2: catch read/parse errors
    try:
        df = pd.read_csv(filepath)
    except pd.errors.EmptyDataError:
        raise ValueError(f"File is empty: {filepath}")
    except pd.errors.ParserError as e:
        raise ValueError(f"File is not valid CSV: {filepath}\n{e}")
    except PermissionError:
        raise PermissionError(f"No permission to read: {filepath}")

    # Step 1: keep only Pink Morsel rows
    df_filtered = df.query("product == 'pink morsel'").copy()

    # Step 2: changing price from object to int.
    df_filtered['price'] = pd.to_numeric(
        df_filtered['price'].str.replace("$", "", regex=False)
    )

    # step 3: Price * product
    df_filtered["sales"] = (df_filtered["quantity"] * df_filtered["price"]).round(2)

    # filtering column and dropping columns that are not needed
    df_filtered = df_filtered[["sales", "date", "region"]]

    return df_filtered

def CSV_merger(df_1, df_2, df_3):
    merged_df = pd.concat([df_1, df_2, df_3], ignore_index = True)
    return merged_df
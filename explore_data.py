
# Import Pandas, the library we'll use to work with CSV data
import pandas as pd

# --------------------------------------------------
# LOAD OUR DATASETS
# --------------------------------------------------

# Read the main DWTS contestant dataset
dwts = pd.read_csv("data/2026_MCM_Problem_C_Data.csv")

# Read the estimated fan support dataset
fan_votes = pd.read_csv("data/estimated_fan_votes.csv")

# --------------------------------------------------
# EXPLORE THE MAIN DATASET
# --------------------------------------------------

# Display the number of rows and columns
print("MAIN DATASET SHAPE:")
print(dwts.shape)

# Show all the column names
# This will help us identify which columns to use
print("\nMAIN DATASET COLUMNS:")
print(dwts.columns.tolist())

# Show the first five contestants
print("\nFIRST FIVE CONTESTANTS:")
print(dwts.head())

# --------------------------------------------------
# EXPLORE THE FAN SUPPORT DATASET
# --------------------------------------------------

# Display the number of rows and columns
print("\nFAN SUPPORT DATASET SHAPE:")
print(fan_votes.shape)

# Show the column names
print("\nFAN SUPPORT COLUMNS:")
print(fan_votes.columns.tolist())

# --------------------------------------------------
# CHECK OUR SEASONS
# --------------------------------------------------

# Find the earliest and latest seasons in the dataset
print("\nSEASON RANGE:")
print(dwts["season"].min(), "to", dwts["season"].max())

# Count how many different seasons are included
print("\nNUMBER OF SEASONS:")
print(dwts["season"].nunique())


# --------------------------------------------------
# CHECK FINAL PLACEMENTS
# --------------------------------------------------

# Display the different placement values and their counts.
# This helps us verify how winners are represented.
print("\nPLACEMENT VALUES:")
print(dwts["placement"].value_counts(dropna=False).sort_index())

# Show the first few winning contestants and their partners.
print("\nFIRST PLACE CONTESTANTS:")
print(
    dwts.loc[
        dwts["results"] == "1st Place",
        ["celebrity_name", "ballroom_partner", "season", "placement"]
    ].head(10)
)

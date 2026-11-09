
# --------------------------------------------------
# IMPORT LIBRARIES
# --------------------------------------------------

# Streamlit creates the interactive web page.
import streamlit as st

# Pandas helps us read, filter, and analyze our dataset.
import pandas as pd

# Plotly Express creates interactive charts.
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

# Configure this page's title, icon, and layout.
st.set_page_config(
    page_title="Season Explorer | Dancing with the Data",
    page_icon="🪩",
    layout="wide"
)


# --------------------------------------------------
# LOAD THE DATA
# --------------------------------------------------

# Cache the dataset so Streamlit doesn't need to
# reload the CSV every time someone changes a filter.
@st.cache_data
def load_data():
    return pd.read_csv("data/2026_MCM_Problem_C_Data.csv")


dwts = load_data()

# Create a cleaned professional dancer name column.
# Remove temporary substitution notes in parentheses.
dwts["pro_name"] = (
    dwts["ballroom_partner"]
    .str.split("(", n=1, regex=False)
    .str[0]
    .str.strip()
)


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🪩 DWTS Season Explorer")

st.write(
    "Explore contestants, professional partners, "
    "winners, and results from every season of "
    "Dancing with the Stars!"
)


# --------------------------------------------------
# SEASON SELECTOR
# --------------------------------------------------

# Find the seasons that actually exist in our dataset.
# Sorting in reverse puts the newest season first.
available_seasons = sorted(
    dwts["season"].dropna().unique(),
    reverse=True
)

# Create a dropdown for visitors to choose a season.
selected_season = st.selectbox(
    "Choose a season to explore:",
    available_seasons
)

# Filter the dataset to include only the selected season.
season_data = dwts[
    dwts["season"] == selected_season
].copy()


# --------------------------------------------------
# SEASON OVERVIEW
# --------------------------------------------------

st.header(f"Season {selected_season} Overview")

# Count the number of contestants in this season.
contestant_count = len(season_data)

# Find the winning couple using final placement.
winner_data = season_data[
    season_data["placement"] == 1
]

# Display two summary metrics side by side.
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Total Contestants",
        value=contestant_count
    )

with col2:
    st.metric(
        label="Winning Couple",
        value=(
            winner_data.iloc[0]["celebrity_name"]
            if not winner_data.empty
            else "Not Available"
        )
    )

# Show the winning professional separately.
if not winner_data.empty:
    winning_pro = winner_data.iloc[0]["pro_name"]
    st.success(f"🏆 Winning Professional Dancer: {winning_pro}")


# --------------------------------------------------
# CONTESTANT STANDINGS
# --------------------------------------------------

st.header("🏅 Contestant Standings")

# Keep the columns most useful to visitors.
standings = season_data[
    [
        "placement",
        "celebrity_name",
        "pro_name",
        "celebrity_industry",
        "results"
    ]
].copy()

# Sort contestants by their final placement.
standings = standings.sort_values(
    by="placement",
    ascending=True
)

# Give columns more readable names.
standings = standings.rename(
    columns={
        "placement": "Placement",
        "celebrity_name": "Celebrity",
        "pro_name": "Professional Partner",
        "celebrity_industry": "Industry",
        "results": "Result"
    }
)

# Display an interactive table.
st.dataframe(
    standings,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# WEEKLY JUDGES' SCORE ANALYSIS
# --------------------------------------------------

st.header("📈 Weekly Judges' Scores")

st.write(
    "See how contestants' average judges' scores changed "
    "throughout the season. Missing scores and zero "
    "placeholders are excluded from the averages."
)

# Create a list to store the weekly scores for each contestant.
weekly_scores = []

# Loop through every contestant in the selected season.
for _, contestant in season_data.iterrows():

    # Our dataset contains score columns for up to 11 weeks.
    for week in range(1, 12):

        # Build the four possible judge column names for this week.
        judge_columns = [
            f"week{week}_judge{judge}_score"
            for judge in range(1, 5)
        ]

        # Get this contestant's scores for the current week.
        scores = pd.to_numeric(
            contestant[judge_columns],
            errors="coerce"
        )

        # Ignore missing scores and zero placeholders.
        valid_scores = scores[(scores.notna()) & (scores > 0)]

        # Only add a record when at least one valid score exists.
        if not valid_scores.empty:
            weekly_scores.append(
                {
                    "Celebrity": contestant["celebrity_name"],
                    "Week": week,
                    "Average Judge Score": valid_scores.mean()
                }
            )

# Convert the list of weekly records into a DataFrame.
weekly_df = pd.DataFrame(weekly_scores)

# --------------------------------------------------
# INTERACTIVE SCORE CHART
# --------------------------------------------------

if not weekly_df.empty:

    # Allow visitors to select which contestants to compare.
    contestants = sorted(weekly_df["Celebrity"].unique())

    selected_contestants = st.multiselect(
        "Choose contestants to compare:",
        options=contestants,
        default=contestants
    )

    # Only show scores for the selected contestants.
    chart_data = weekly_df[
        weekly_df["Celebrity"].isin(selected_contestants)
    ]

    if not chart_data.empty:

        
        # Create one line per contestant.
        fig = px.line(
            chart_data,
            x="Week",
            y="Average Judge Score",
            color="Celebrity",
            markers=True,
            title=f"Season {selected_season}: Weekly Score Trends"
        )

        # Customize the chart's axes and tooltip.
        fig.update_layout(
            yaxis_range=[0, 10],
            xaxis=dict(dtick=1),

            # Show all contestants' scores for the hovered week.
            hovermode="x unified",

            height=550
        )

        # Display the interactive chart.
        st.plotly_chart(
            fig,
            use_container_width=True
        )


    else:
        st.info("Select at least one contestant to view the chart.")

else:
    st.info("No weekly judges' scores are available for this season.")


# --------------------------------------------------
# WEEKLY SCORING LEADERBOARD
# --------------------------------------------------

st.header("🏆 Weekly Scoring Leaderboard")

st.write(
    "Choose a competition week to see how contestants "
    "ranked based on their average judges' scores."
)

# Find all weeks with at least one valid score.
available_weeks = sorted(weekly_df["Week"].unique()) if not weekly_df.empty else []

if available_weeks:

    # Let visitors choose which week to explore.
    selected_week = st.selectbox(
        "Choose a week:",
        available_weeks
    )

    # Keep only the scores for the selected week.
    week_data = weekly_df[
        weekly_df["Week"] == selected_week
    ].copy()

    # Sort contestants from highest to lowest score.
    week_data = week_data.sort_values(
        by="Average Judge Score",
        ascending=False
    )

    # Create ranking numbers, giving tied scores
    # the same rank.
    week_data["Rank"] = (
        week_data["Average Judge Score"]
        .rank(method="min", ascending=False)
        .astype(int)
    )

    # Reorder the columns for a cleaner table.
    leaderboard = week_data[
        ["Rank", "Celebrity", "Average Judge Score"]
    ].copy()

    # Display the scores to two decimal places.
    st.dataframe(
        leaderboard,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Average Judge Score": st.column_config.NumberColumn(
                "Average Judge Score",
                format="%.2f"
            )
        }
    )

else:
    st.info("No weekly scoring data is available.")

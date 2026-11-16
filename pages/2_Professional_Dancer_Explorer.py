
import streamlit as st
import pandas as pd
import plotly.express as px

# Configure the page.
st.set_page_config(
    page_title="Professional Dancer Explorer | Dancing with the Data",
    page_icon=":material/steps:",
    layout="wide"
)

# Load the DWTS dataset.
# Update this path if your CSV is stored somewhere different.
@st.cache_data
def load_data():
    return pd.read_csv("data/2026_MCM_Problem_C_Data.csv")

df = load_data()

# Page heading.
st.markdown(
    "<p style='color: #D4AF37; font-weight: 700; "
    "letter-spacing: 3px; margin-bottom: 0;'>MEET THE PROFESSIONALS</p>",
    unsafe_allow_html=True
)

st.title("Professional Dancer Explorer")

st.write(
    "Explore the careers of the professional dancers who have "
    "competed for the Mirrorball Trophy."
)

st.divider()


# Clean professional dancer names.
# Remove notes in parentheses, such as special guest appearances.
df["professional_dancer"] = (
    df["ballroom_partner"]
    .str.replace(r"\s*\(.*?\)", "", regex=True)
    .str.strip()
)

# Create an alphabetical list of professional dancers.
professional_dancers = sorted(
    df["professional_dancer"].dropna().unique()
)

# Let visitors choose which professional dancer to explore.
selected_dancer = st.selectbox(
    "Select a Professional Dancer",
    professional_dancers,
    index=professional_dancers.index("Derek Hough")
    if "Derek Hough" in professional_dancers else 0
)

# Filter the dataset to the selected dancer.
dancer_data = df[
    df["professional_dancer"] == selected_dancer
].copy()

# Display the selected dancer's name.
st.subheader(selected_dancer)


# Calculate career statistics for the selected professional dancer.

# Count the number of unique seasons the dancer competed in.
seasons_competed = dancer_data["season"].nunique()

# Count top-three finishes as a measure of finale success.
finale_appearances = (dancer_data["placement"] <= 3).sum()

# Count Mirrorball Trophy wins (1st place finishes).
mirrorball_wins = (dancer_data["placement"] == 1).sum()

# Find the dancer's best placement (lower numbers are better).
best_placement = dancer_data["placement"].min()

# Display the career statistics in four columns.
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Seasons Competed", seasons_competed)

with col2:
    st.metric("Top 3 Finishes", finale_appearances)

with col3:
    st.metric("Mirrorball Wins", mirrorball_wins)

with col4:
    st.metric("Best Placement", f"#{best_placement:.0f}")


# Career history section.
st.divider()
st.subheader("Career History")

st.write(
    f"Explore {selected_dancer}'s celebrity partnerships "
    "and competition results across the seasons."
)

# Select the columns we want to display.
career_history = dancer_data[
    ["season", "celebrity_name", "placement", "results"]
].copy()

# Rename columns to make the table easier to read.
career_history = career_history.rename(
    columns={
        "season": "Season",
        "celebrity_name": "Celebrity Partner",
        "placement": "Final Placement",
        "results": "Result"
    }
)

# Show the most recent seasons first.
career_history = career_history.sort_values(
    by="Season",
    ascending=False
)

# Display the interactive table.
st.dataframe(
    career_history,
    hide_index=True,
    use_container_width=True
)


# Career placement visualization.
st.divider()
st.subheader("Career Placement Trends")

st.write(
    f"Explore {selected_dancer}'s final placements "
    "throughout their Dancing with the Stars career."
)

# Prepare the data for the placement chart.
placement_data = dancer_data[
    ["season", "placement", "celebrity_name"]
].copy()

# Sort seasons chronologically.
placement_data = placement_data.sort_values("season")

# Create a line chart showing placement across seasons.
fig = px.line(
    placement_data,
    x="season",
    y="placement",
    markers=True,
    custom_data=["celebrity_name"],
    title=f"{selected_dancer}: Placement by Season"
)

# Apply DWTS-inspired styling.
fig.update_traces(
    line=dict(color="#D4AF37", width=3),
    marker=dict(size=10, color="#D4AF37"),
    hovertemplate=(
        "<b>Season %{x}</b>"
        "<br>Celebrity: %{customdata[0]}"
        "<br>Placement: #%{y}"
        "<extra></extra>"
    )
)

fig.update_layout(
    xaxis_title="Season",
    yaxis_title="Final Placement",
    yaxis=dict(
        autorange="reversed",
        dtick=1
    ),
    xaxis=dict(dtick=1),
    height=450,
    hovermode="closest"
)

# Highlight Mirrorball-winning seasons with larger markers.
# A placement of 1 indicates a first-place finish.
winning_seasons = placement_data[
    placement_data["placement"] == 1
]

fig.add_scatter(
    x=winning_seasons["season"],
    y=winning_seasons["placement"],
    mode="markers",
    marker=dict(
        size=15,
        color="#F3D98B",  # Champagne gold
        line=dict(color="#D4AF37", width=2)
    ),
    name="Mirrorball Win",
    hoverinfo="skip"
)


# Display the chart.
st.plotly_chart(fig, use_container_width=True)

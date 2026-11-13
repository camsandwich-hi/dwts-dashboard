
# --------------------------------------------------
# IMPORT LIBRARIES
# --------------------------------------------------

# Streamlit builds our interactive website.
import streamlit as st

# Pandas reads and analyzes our DWTS dataset.
import pandas as pd

# Plotly Express creates interactive charts.
import plotly.express as px


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

# Configure the browser tab and page layout.
st.set_page_config(
    page_title="Dancing with the Data",
    page_icon="🏆",
    layout="wide"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

# Load our contestant dataset.
dwts = pd.read_csv("data/2026_MCM_Problem_C_Data.csv")


# --------------------------------------------------
# CLEAN PROFESSIONAL DANCER NAMES
# --------------------------------------------------

# Some partner names contain notes in parentheses,
# such as temporary substitutions during a season.
#
# Remove these notes so we can count dancers and
# calculate Mirrorball wins more consistently.
#
# Keep the original ballroom_partner column unchanged.

dwts["pro_name"] = (
    dwts["ballroom_partner"]
    .str.split("(", n=1, regex=False)
    .str[0]
    .str.strip()
)


# --------------------------------------------------
# CALCULATE DASHBOARD STATISTICS
# --------------------------------------------------

# Count the number of unique seasons.
total_seasons = dwts["season"].nunique()

# Count contestant records in the dataset.
total_contestants = len(dwts)

# Count unique professional dancer names after cleaning.
total_pros = dwts["pro_name"].nunique()


# --------------------------------------------------
# HOMEPAGE HEADER
# --------------------------------------------------

# Use gold text and letter spacing for a professional,
# ballroom-inspired introduction.

st.markdown(
    "<p style='color: #D4AF37; font-size: 14px; "
    "font-weight: 600; letter-spacing: 3px;'>"
    "WELCOME TO THE BALLROOM"
    "</p>",
    unsafe_allow_html=True
)

st.title("Dancing with the Data")

st.subheader("The Statistics Behind the Mirrorball Trophy")

st.write(
    "Explore the celebrities, professional dancers, "
    "judges' scores, and unforgettable moments from "
    "Dancing with the Stars."
)

st.divider()


# --------------------------------------------------
# EXPLORE THE BALLROOM
# --------------------------------------------------

# Give visitors an easy way to navigate the dashboard.
st.header("Explore the Ballroom")

st.write(
    "Discover the stories behind the statistics. "
    "Start by exploring individual seasons, contestants, "
    "and weekly performances."
)

# Create a section for our Season Explorer page.
with st.container(border=True):

    st.subheader("Season Explorer")

    st.write(
        "Explore every season's contestants, professional "
        "partners, final standings, and weekly judges' scores."
    )

    # Open our existing Season Explorer page.
    st.page_link(
        "pages/1_Season_Explorer.py",
        label="Explore Seasons",
        icon=":material/arrow_forward:"
    )

st.divider()


# --------------------------------------------------
# DASHBOARD OVERVIEW
# --------------------------------------------------

# Display three statistics side by side.
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Seasons",
        value=total_seasons
    )

with col2:
    st.metric(
        label="Contestant Records",
        value=total_contestants
    )

with col3:
    st.metric(
        label="Professional Dancers",
        value=total_pros
    )

st.divider()


# --------------------------------------------------
# MIRRORBALL TROPHY LEADERBOARD
# --------------------------------------------------

# Keep only contestants who finished in first place.
# Each row represents a winning celebrity and their
# professional dance partner.
winners = dwts[dwts["placement"] == 1].copy()

# Count how many winning seasons each professional
# dancer has appeared in.
pro_wins = (
    winners["pro_name"]
    .value_counts()
    .reset_index()
)

# Rename the columns for the chart.
pro_wins.columns = [
    "Professional Dancer",
    "Mirrorball Wins"
]

# Display the leaderboard heading.
st.header("Mirrorball Trophy Leaderboard")


# --------------------------------------------------
# MIRRORBALL LEADERBOARD CHART
# --------------------------------------------------

# Display only the top 10 dancers on the homepage.
# The complete results remain available in pro_wins.
top_pros = pro_wins.head(10).copy()

# Create a horizontal bar chart using our gold theme.
fig = px.bar(
    top_pros,
    x="Mirrorball Wins",
    y="Professional Dancer",
    orientation="h",
    text="Mirrorball Wins",
    title="Professional Dancers with the Most Wins"
)

# Style the chart to match our DWTS-inspired theme.
fig.update_traces(
    marker_color="#D4AF37",
    textposition="outside",
    hovertemplate=(
        "<b>%{y}</b>"
        "<br>Mirrorball Wins: %{x}"
        "<extra></extra>"
    )
)

# Keep the highest number of wins at the top.
fig.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_title="Mirrorball Wins",
    yaxis_title=None,
    height=450,
    margin=dict(l=10, r=45, t=60, b=30),
    showlegend=False
)

# Give the labels a little extra space.
fig.update_xaxes(
    range=[0, top_pros["Mirrorball Wins"].max() + 1],
    dtick=1
)

# Display the interactive chart.
st.plotly_chart(
    fig,
    use_container_width=True
)



# --------------------------------------------------
# INTERACTIVE BUTTON
# --------------------------------------------------

# Keep our original interactive button for now.
# We can replace this with homepage navigation later.
if st.button("Let's Dance!"):
    st.balloons()

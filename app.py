
# Import Streamlit, the library we use to build our web app
import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
# Set the browser tab title, icon, and page width.
st.set_page_config(
    page_title="Dancing with the Data",
    page_icon="💃",
    layout="wide"
)


# --------------------------------------------------
# HOMEPAGE HEADER
# --------------------------------------------------

# Introduce visitors to the dashboard with a
# ballroom-inspired welcome message.
st.markdown("### ✨ WELCOME TO THE BALLROOM")

st.title("Dancing with the Data 🪩")

st.subheader("The statistics behind the Mirrorball Trophy")

st.write(
    "Step into the ballroom and explore the celebrities, "
    "professional dancers, judges' scores, and unforgettable "
    "moments from Dancing with the Stars!"
)

# Add a divider between the introduction and statistics.
st.divider()


# --------------------------------------------------
# DASHBOARD OVERVIEW
# --------------------------------------------------

# Import Pandas to work with our DWTS dataset.
import pandas as pd

# Import Plotly Express to create interactive charts.
import plotly.express as px

# Load our contestant dataset.
dwts = pd.read_csv("data/2026_MCM_Problem_C_Data.csv")

# Calculate statistics directly from the dataset.
total_seasons = dwts["season"].nunique()
total_contestants = len(dwts)
total_pros = dwts["ballroom_partner"].nunique()

# Display three statistics side by side.
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🪩 Seasons", total_seasons)

with col2:
    st.metric("⭐ Contestant Records", total_contestants)

with col3:
    st.metric("💃 Professional Dancers", total_pros)

st.divider()

# --------------------------------------------------
# MIRRORBALL TROPHY LEADERBOARD
# --------------------------------------------------


# --------------------------------------------------
# CLEAN PROFESSIONAL DANCER NAMES
# --------------------------------------------------

# Some professional dancer names contain extra information
# in parentheses, such as temporary partner substitutions.
#
# Create a new column with only the dancer's name.
# Keep the original column so we don't lose that information.
dwts["pro_name"] = (
    dwts["ballroom_partner"]
    .str.split("(", n=1, regex=False)
    .str[0]
    .str.strip()
)

# Keep only contestants who finished in first place.
# Each row represents a celebrity and their professional partner.
winners = dwts[dwts["placement"] == 1].copy()

# Count how many winning seasons each professional dancer has.
# value_counts() counts the number of times each name appears.
pro_wins = (
    winners["pro_name"]
    .value_counts()
    .reset_index()
)

# Give the resulting columns easier-to-understand names.
pro_wins.columns = ["Professional Dancer", "Mirrorball Wins"]

# Display a heading above our chart.
st.header("🏆 Mirrorball Trophy Leaderboard")

# Create an interactive horizontal bar chart.
fig = px.bar(
    pro_wins,
    x="Mirrorball Wins",
    y="Professional Dancer",
    orientation="h",
    color="Mirrorball Wins",
    color_continuous_scale="Purples",
    title="Professional Dancers with the Most Wins"
)

# Put the dancers with the most wins at the top.
fig.update_layout(
    yaxis={"categoryorder": "total ascending"},
    coloraxis_showscale=False,
    height=650
)

# Display the chart on our Streamlit website.
st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# INTERACTIVE BUTTON
# --------------------------------------------------
# When clicked, Streamlit displays balloons!
if st.button("Let's Dance!"):
    st.balloons()

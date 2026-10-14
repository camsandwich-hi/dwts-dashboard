
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
# WEBSITE HEADER
# --------------------------------------------------
# Display the main title and description.
st.title("Dancing with the Data 🪩")

st.subheader("The statistics behind the Mirrorball Trophy")

st.write(
    "Explore the celebrities, professional dancers, "
    "judges' scores, and results from Dancing with the Stars!"
)

# --------------------------------------------------
# INTERACTIVE SEASON FILTER
# --------------------------------------------------
# Create a dropdown menu with seasons 1 through 34.
# range(1, 35) includes 1 but stops before 35.
# We'll connect this to real data later.

season = st.selectbox(
    "Choose a season:",
    ["All Seasons"] + list(range(1, 35))
)

# Show the user's selected season.
st.write(f"You selected: {season}")


# --------------------------------------------------
# MIRRORBALL TROPHY LEADERBOARD
# --------------------------------------------------

# Import Pandas to read and analyze our DWTS dataset.
import pandas as pd

# Import Plotly Express to create interactive charts.
import plotly.express as px

# Load the contestant dataset from our data folder.
dwts = pd.read_csv("data/2026_MCM_Problem_C_Data.csv")

# Keep only contestants who finished in first place.
# Each row represents a celebrity and their professional partner.
winners = dwts[dwts["placement"] == 1].copy()

# Count how many winning seasons each professional dancer has.
# value_counts() counts the number of times each name appears.
pro_wins = (
    winners["ballroom_partner"]
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


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
# PLACEHOLDER FOR FUTURE STATISTICS
# --------------------------------------------------
# This message will eventually be replaced by charts.
st.info("DWTS statistics are coming soon!")

# --------------------------------------------------
# INTERACTIVE BUTTON
# --------------------------------------------------
# When clicked, Streamlit displays balloons!
if st.button("Let's Dance!"):
    st.balloons()

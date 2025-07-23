import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import os
from datetime import datetime, timedelta

# === Load Athlete Profiles ===
df_profiles = pd.read_csv("fake_athlete_profiles.csv")

# === Page Config ===
st.set_page_config(layout="wide")
st.title("🏈 Athlete Profile Dashboard")

# === MULTI-SELECT SECTION ===
st.markdown("### 📋 Select Players")
selected_players = st.multiselect(
    "Choose one or more athletes to view/export",
    options=df_profiles["Name"].tolist(),
    default=[df_profiles["Name"].iloc[0]]
)

# === Filter Data ===
selected_df = df_profiles[df_profiles["Name"].isin(selected_players)]

# === Display Table of Selected Players ===
if not selected_df.empty:
    st.dataframe(selected_df, use_container_width=True)

# === Download Button ===
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

if not selected_df.empty:
    csv = convert_df_to_csv(selected_df)
    st.download_button(
        label="📥 Download Selected Profiles as CSV",
        data=csv,
        file_name="selected_athletes.csv",
        mime="text/csv"
    )

# === SINGLE PLAYER VIEW (if only one selected) ===
if len(selected_players) == 1:
    player_data = selected_df.iloc[0]

    with st.container():
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader(f"{player_data['Name']}")
            st.markdown(f"**High School:** {player_data['High School']}")
            st.markdown(f"**Graduation Year:** {player_data['Graduation Year']}")
            st.markdown(f"**Height:** {player_data['Height']}")
            st.markdown(f"**Weight:** {player_data['Weight']}")

        with col2:
            st.subheader("📊 Athletic Profile")

            categories = ['Speed', 'Agility', 'Strength', 'Vertical', 'Endurance']
            player_values = [player_data[c] for c in categories]
            hover_labels = [f"{cat}: {val}" for cat, val in zip(categories, player_values)]

            # Mock comparison groups
            ucla_avg = [88, 82, 90, 84, 85]
            hs_avg = [72, 75, 74, 70, 73]
            combine_avg = [80, 78, 82, 76, 80]

            fig = go.Figure()

            # Player
            fig.add_trace(go.Scatterpolar(
                r=player_values,
                theta=categories,
                mode='lines+markers',
                name=player_data['Name'],
                line=dict(color='crimson', width=3),
                marker=dict(size=8),
                hoverinfo='text',
                hovertext=hover_labels
            ))

            # UCLA Avg
            fig.add_trace(go.Scatterpolar(
                r=ucla_avg,
                theta=categories,
                mode='lines',
                name='UCLA Avg',
                line=dict(color='dodgerblue', width=2, dash='dash')
            ))

            # HS Avg
            fig.add_trace(go.Scatterpolar(
                r=hs_avg,
                theta=categories,
                mode='lines',
                name='HS Avg',
                line=dict(color='darkorange', width=2, dash='dot')
            ))

            # Combine Avg
            fig.add_trace(go.Scatterpolar(
                r=combine_avg,
                theta=categories,
                mode='lines',
                name='Combine Avg',
                line=dict(color='gray', width=2, dash='dashdot')
            ))

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                hovermode='closest',
                margin=dict(t=20, b=20)
            )

            st.plotly_chart(fig, use_container_width=True)

    # === BOTTOM METRIC + OFFERS SECTION ===
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📝 Combine & Metric Scores")
        metric_data = {
            "Metric": ["Speed", "Agility", "Strength", "Vertical", "Endurance"],
            "Value": [player_data["Speed"], player_data["Agility"], player_data["Strength"],
                      player_data["Vertical"], player_data["Endurance"]]
        }
        df_metrics = pd.DataFrame(metric_data)
        st.dataframe(df_metrics, height=300, use_container_width=True)

    with col4:
        st.subheader("🎓 Offers")

        possible_schools = [
            "Alabama", "Ohio State", "Georgia", "LSU", "UCLA", "Florida State", "Texas", "Michigan",
            "Penn State", "Oregon", "Tennessee", "USC", "Notre Dame", "Miami", "Clemson", "Washington",
            "TCU", "Oklahoma", "Wisconsin", "North Carolina", "Texas A&M", "Kentucky", "Arkansas", "Auburn", "Minnesota"
        ]
        offer_list = random.sample(possible_schools, k=20)
        df_offers = pd.DataFrame(offer_list, columns=["Offer"])
        st.dataframe(df_offers, height=300, use_container_width=True)

    # === PLAYER SCHEDULE SECTION ===
    st.subheader("📅 2026 Game Schedule")

    # Generate mock schedule
    opponents = random.sample([
        "Lincoln HS", "Central Catholic", "Oak Hill", "Liberty Prep", "St. John Bosco",
        "IMG Academy", "Mater Dei", "De La Salle", "Eastside", "Northwestern", "Edison", "Poly HS"
    ], 10)

    start_date = datetime(2026, 8, 28)
    schedule_data = []

    for i, opponent in enumerate(opponents):
        game_date = (start_date + timedelta(weeks=i)).strftime('%b %d, %Y')
        location = random.choice(["Home", "Away"])
        result = random.choice(["W", "L", ""])  # Leave blank for upcoming games
        schedule_data.append({
            "Date": game_date,
            "Opponent": opponent,
            "Location": location,
            "Result": result
        })

    df_schedule = pd.DataFrame(schedule_data)
    st.dataframe(df_schedule, height=350, use_container_width=True)

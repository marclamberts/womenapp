import streamlit as st
import pandas as pd
import altair as alt

file_path = "Database Women.xlsx"
df = pd.read_excel(file_path)

# Drop duplicate columns from the DataFrame
df = df.loc[:, ~df.columns.duplicated()]

def main():
    st.title("Top Performers App")

    # Create a sidebar column on the left for filters
    st.sidebar.title("Filters")

    # Set the minimal minutes to 500 using the slider in the sidebar
    min_minutes_played = st.sidebar.slider("Minimum Minutes Played", min_value=0, max_value=2000, value=500, step=100)

    # Create a dropdown for the user to select a league in the sidebar
    leagues = df["League"].unique()
    selected_league = st.sidebar.selectbox("Select League", leagues)

    # Create a dropdown for the user to select a team within the selected league in the sidebar
    teams_in_selected_league = df[df["League"] == selected_league]["Team"].unique()
    selected_team = st.sidebar.selectbox("Select Team", teams_in_selected_league)

    # Create a dropdown for the user to select a metric for the bar graph in the sidebar
    available_metrics = [col for col in df.columns if col not in ["League", "Minutes played", "Player", "Team"]]
    selected_metric = st.sidebar.selectbox("Select Performance Metric for Bar Graph", available_metrics)

    # Calculate percentile rank for the selected metric based on the total dataset and convert to 100.0 scale
    df["Percentile Rank"] = df[selected_metric].rank(pct=True) * 100.0

    # Subset the DataFrame based on the selected league, team, and minimal minutes
    filtered_df = df[(df["League"] == selected_league) & (df["Team"] == selected_team) & (df["Minutes played"] >= min_minutes_played)]

    # Sort the filtered DataFrame based on the selected metric in descending order
    sorted_df = filtered_df.sort_values(by=selected_metric, ascending=False)

    # Display the top performers in a table and a bar graph side by side
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"Top Performers in {selected_team} ({selected_league}) with at least {min_minutes_played} Minutes Played:")
        table_columns = ["Player", "Team", "Age", "Minutes played", selected_metric]
        st.dataframe(sorted_df[table_columns].head(15), height=400)

    with col2:
        chart_data = sorted_df.head(15)
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X(selected_metric, title=selected_metric),
            y=alt.Y("Player", sort="-x", title="Player"),
            tooltip=["Player", "Team", "Age", "Minutes played", selected_metric, alt.Tooltip("Percentile Rank:Q", format=".1f")],
            color=alt.Color("Percentile Rank:Q", title="Percentile Rank", scale=alt.Scale(scheme='viridis'))
        ).properties(width=500, height=400, title=f"Top 15 Performers in {selected_team} ({selected_league}) for {selected_metric}")
        st.altair_chart(chart)

    # Add the text at the bottom of the app
    st.markdown("@lambertsmarc | collected at 22-07-2023 | Wyscout")

if __name__ == "__main__":
    main()

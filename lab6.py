import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# PAGE CONFIGURATION

st.set_page_config(
    page_title="Football Analytics",
    page_icon="⚽",
    layout="wide"
)


# LOAD DATASET

df = pd.read_csv("players_data-2025_2026.csv")


# SELECT REQUIRED COLUMNS

df = df[[
    "Player", "Nation", "Pos", "Squad", "Comp",
    "Age", "MP", "Starts", "Min",
    "Gls", "Ast", "G+A",
    "Sh", "SoT", "SoT%",
    "TklW", "Int", "CrdY", "CrdR"
]]

# Convert numerical columns
numeric_columns = [
    "Age", "MP", "Starts", "Min",
    "Gls", "Ast", "G+A", "Sh", "SoT",
    "SoT%", "TklW", "Int", "CrdY", "CrdR"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Remove records without important information
df = df.dropna(
    subset=["Player", "Pos", "Squad", "Comp", "Age"]
)


# DASHBOARD TITLE

st.title("⚽ Football Player Performance Analytics")

st.write(
    "An interactive dashboard to explore and analyse "
    "football player performance during the 2025-2026 season."
)


# SIDEBAR FILTERS

st.sidebar.header("Filter Options")

# Competition Filter
competition_list = sorted(df["Comp"].unique().tolist())

selected_competition = st.sidebar.selectbox(
    "Select Competition",
    ["All"] + competition_list
)

# Position Filter
position_list = sorted(df["Pos"].unique().tolist())

selected_positions = st.sidebar.multiselect(
    "Select Player Position",
    position_list,
    default=position_list
)

# Age Filter
minimum_age = int(df["Age"].min())
maximum_age = int(df["Age"].max())

selected_age = st.sidebar.slider(
    "Select Age Range",
    minimum_age,
    maximum_age,
    (minimum_age, maximum_age)
)


# APPLY FILTERS

filtered_df = df[
    (df["Pos"].isin(selected_positions)) &
    (df["Age"] >= selected_age[0]) &
    (df["Age"] <= selected_age[1])
]

if selected_competition != "All":

    filtered_df = filtered_df[
        filtered_df["Comp"] == selected_competition
    ]


# DASHBOARD KPIs

st.header("Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Players",
    len(filtered_df)
)

col2.metric(
    "Total Goals",
    int(filtered_df["Gls"].sum())
)

col3.metric(
    "Total Assists",
    int(filtered_df["Ast"].sum())
)

if len(filtered_df) > 0:
    average_goals = filtered_df["Gls"].mean()
else:
    average_goals = 0

col4.metric(
    "Average Goals",
    round(average_goals, 2)
)


# APPLICATION TABS

tab1, tab2, tab3, tab4 = st.tabs([
    "Dataset Overview",
    "Data Analysis",
    "Visualizations",
    "Insights"
])


# TAB 1: DATASET OVERVIEW

with tab1:

    st.subheader("Football Player Records")

    st.dataframe(filtered_df, hide_index=True)

    st.subheader("Position-wise Player Count")

    position_count = filtered_df.groupby("Pos").size()

    st.dataframe(
        position_count.rename("Number of Players")
    )

    st.subheader("Competition-wise Player Count")

    competition_count = filtered_df.groupby("Comp").size()

    st.dataframe(
        competition_count.rename("Number of Players")
    )

    with st.expander("View Dataset Information"):

        st.write("Total Records:", len(df))
        st.write("Total Columns:", len(df.columns))

        st.write("Selected Columns:")
        st.write(df.columns.tolist())

        st.write("Missing Values:")
        st.write(df.isnull().sum())


# TAB 2: DATA ANALYSIS

with tab2:

    st.subheader("Statistical Summary")

    st.dataframe(
        filtered_df[numeric_columns].describe()
    )

    st.subheader("Average Goals by Position")

    average_goals_position = filtered_df.groupby("Pos")["Gls"].mean()

    st.dataframe(
        average_goals_position.rename("Average Goals")
    )

    st.subheader("Average Assists by Position")

    average_assists_position = filtered_df.groupby("Pos")["Ast"].mean()

    st.dataframe(
        average_assists_position.rename("Average Assists")
    )


# TAB 3: VISUALIZATIONS

with tab3:

    if len(filtered_df) > 0:

        # BAR CHART

        st.subheader("Bar Chart - Average Goals by Position")

        average_goals_position = filtered_df.groupby("Pos")["Gls"].mean()

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.bar(
            average_goals_position.index,
            average_goals_position.values,
            label="Average Goals"
        )

        ax.set_title("Average Goals by Player Position")
        ax.set_xlabel("Player Position")
        ax.set_ylabel("Average Goals")
        ax.legend()

        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

        st.write(
            "Interpretation: This chart compares the average goals "
            "scored by players across different playing positions."
        )


        # LINE CHART

        st.subheader("Line Chart - Top 10 Goal Scorers")

        top_players = filtered_df.nlargest(10, "Gls")

        fig, ax = plt.subplots(figsize=(9, 5))

        ax.plot(
            top_players["Player"],
            top_players["Gls"],
            marker="o",
            label="Goals Scored"
        )

        ax.set_title("Top 10 Players by Goals")
        ax.set_xlabel("Player Name")
        ax.set_ylabel("Goals Scored")
        ax.legend()

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

        st.write(
            "Interpretation: This chart compares the goal-scoring "
            "performance of the top 10 players. It helps identify "
            "the leading goal scorers."
        )


        # SCATTER PLOT

        st.subheader("Scatter Plot - Goals vs Assists")

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.scatter(
            filtered_df["Gls"],
            filtered_df["Ast"],
            label="Players"
        )

        ax.set_title("Relationship Between Goals and Assists")
        ax.set_xlabel("Goals Scored")
        ax.set_ylabel("Assists")
        ax.legend()

        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

        st.write(
            "Interpretation: This chart shows the relationship "
            "between goals and assists. It helps identify players "
            "with high goal-scoring and assisting contributions."
        )

    else:

        st.warning("No records available for the selected filters.")


# TAB 4: INSIGHTS

with tab4:

    st.subheader("Key Performance Insights")

    if len(filtered_df) > 0:

        highest_scorer = filtered_df.loc[
            filtered_df["Gls"].idxmax()
        ]

        highest_assists = filtered_df.loc[
            filtered_df["Ast"].idxmax()
        ]

        st.write("### Highest Goal Scorer")

        st.write("Player:", highest_scorer["Player"])
        st.write("Club:", highest_scorer["Squad"])
        st.write("Goals:", highest_scorer["Gls"])

        st.divider()

        st.write("### Highest Assist Provider")

        st.write("Player:", highest_assists["Player"])
        st.write("Club:", highest_assists["Squad"])
        st.write("Assists:", highest_assists["Ast"])

        st.divider()

        st.write("### Overall Statistics")

        st.write("Players Analysed:", len(filtered_df))
        st.write("Total Goals:", filtered_df["Gls"].sum())
        st.write("Total Assists:", filtered_df["Ast"].sum())

    else:

        st.warning("No data available for generating insights.")
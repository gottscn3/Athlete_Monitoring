import streamlit as st
import pandas as pd
from main import build_athlete_summary


# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------

st.set_page_config(
    page_title="Athlete Monitoring",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #F4F6F5;
    }

    /* Remove some default top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    /* Header */
    .header {
        background: linear-gradient(
            135deg,
            #006A4D 0%,
            #00543E 100%
        );

        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;

        box-shadow:
            0 4px 12px rgba(0, 0, 0, 0.10);
    }

    .header-title {
        color: white;
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        line-height: 1.1;
        margin: 0;
    }

    .header-subtitle {
        color: #DDEEE8;
        font-size: 1.05rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* Section titles */
    .section-title {
        color: #006A4D;
        font-size: 1.25rem;
        font-weight: 750;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: white;
        border-radius: 10px;

        padding: 1rem 1.2rem;

        border-top: 4px solid #006A4D;

        box-shadow:
            0 2px 8px rgba(0, 0, 0, 0.07);
    }

    div[data-testid="metric-container"] label {
        color: #5F6B66 !important;
        font-weight: 600;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #1F2925 !important;
        font-weight: 750;
    }

    /* Team comparison cards */
    .team-card {
        background-color: white;
        border-radius: 10px;

        padding: 1rem 1.2rem;

        border-top: 4px solid #006A4D;

        box-shadow:
            0 2px 8px rgba(0, 0, 0, 0.07);

        min-height: 105px;
    }

    .team-card-title {
        color: #5F6B66;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }

    .team-card-value {
        color: #1F2925;
        font-size: 1.8rem;
        font-weight: 750;
        line-height: 1.1;
    }

    .team-card-comparison {
        color: #66716C;
        font-size: 0.82rem;
        margin-top: 0.35rem;
    }

    /* Date selector card */
    .date-card {
        background-color: white;
        padding: 1rem 1.25rem 0.4rem 1.25rem;
        border-radius: 10px;

        box-shadow:
            0 2px 8px rgba(0, 0, 0, 0.06);

        margin-bottom: 1.5rem;
    }

    /* Guide cards */
    .guide-card {
        background-color: white;

        padding: 0.9rem 1rem;

        border-radius: 10px;

        box-shadow:
            0 2px 8px rgba(0, 0, 0, 0.06);

        min-height: 65px;
    }

    .guide-title {
        font-weight: 700;
        color: #1F2925;
        font-size: 0.95rem;
    }

    .guide-description {
        color: #66716C;
        font-size: 0.82rem;
        margin-top: 0.2rem;
    }

    /* Table explanation */
    .table-note {
        color: #66716C;
        font-size: 0.82rem;
        margin-top: 0.6rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #7A8580;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="header">
        <div class="header-title">
            Athlete Monitoring Dashboard (Synthetic Data)
        </div>
        <div class="header-subtitle">
            Load Management • Readiness
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# FILE
# ---------------------------------------------------------

file_path = "Generic Data.xlsx"


# ---------------------------------------------------------
# DATE SELECTOR
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Monitoring Date</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="date-card">',
    unsafe_allow_html=True
)

date_col, load_col = st.columns(2)


with date_col:

    selected_date = st.date_input(
        "Monitoring date",
        value=pd.Timestamp("2026-09-09")
    )


with load_col:

    load_calculation = st.radio(
        "Load calculation",
        ["Cumulative", "Average / Session"],
        horizontal=True
    )


st.markdown(
    '</div>',
    unsafe_allow_html=True
)

selected_date = pd.Timestamp(selected_date)


# ---------------------------------------------------------
# BUILD ATHLETE SUMMARY
# ---------------------------------------------------------

athlete_summary = build_athlete_summary(
    file_path,
    selected_date
)


# ---------------------------------------------------------
# HELPER FUNCTION
# ---------------------------------------------------------

def percent_change(current, previous):

    if pd.isna(current) or pd.isna(previous) or previous == 0:
        return None

    return (
        (current - previous)
        / previous
    ) * 100


def format_team_comparison(
    current,
    previous,
    decimals=0
):

    if pd.isna(current):

        current_text = "—"

    else:

        current_text = f"{current:,.{decimals}f}"


    if pd.isna(previous):

        comparison_text = "Previous 7 Days: —"

    else:

        previous_text = f"{previous:,.{decimals}f}"

        change = percent_change(
            current,
            previous
        )

        if change is not None:

            comparison_text = (
                f"Previous 7 Days: "
                f"{previous_text} "
                f"({change:+.1f}%)"
            )

        else:

            comparison_text = (
                f"Previous 7 Days: "
                f"{previous_text}"
            )


    return current_text, comparison_text


def format_athlete_comparison(
    current,
    previous,
    decimals=0
):

    if pd.isna(current):

        return "—"

    current_text = f"{current:,.{decimals}f}"

    # Make the current value visually bold
    bold_map = str.maketrans(
        "0123456789",
        "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"
    )

    current_bold = current_text.translate(
        bold_map
    )

    if pd.isna(previous) or previous == 0:

        return current_bold

    previous_text = f"{previous:,.{decimals}f}"

    change = percent_change(
        current,
        previous
    )

    if change is None:

        return (
            f"{current_bold}\n"
            f"({previous_text})"
        )

    return (
        f"{current_bold}\n"
        f"({previous_text}, {change:+.1f}%)"
    )


# ---------------------------------------------------------
# TEAM METRICS
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Team Overview</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# LOAD CALCULATION VIEW
# ---------------------------------------------------------

if load_calculation == "Cumulative":

    # Current 7-day totals
    total_trimp = athlete_summary[
        "Current_7Day_Trimp"
    ].sum(
        min_count=1
    )

    total_movement_load = athlete_summary[
        "Current_7Day_Movement_Load"
    ].sum(
        min_count=1
    )

    # Previous 7-day totals
    previous_total_trimp = athlete_summary[
        "Previous_7Day_Trimp"
    ].sum(
        min_count=1
    )

    previous_total_movement_load = athlete_summary[
        "Previous_7Day_Movement_Load"
    ].sum(
        min_count=1
    )

    trimp_label = "Team 7-Day TRIMP"
    movement_label = "Team 7-Day Movement Load"


else:

    # Current average session load
    total_trimp = athlete_summary[
        "Current_Avg_Trimp"
    ].mean()

    total_movement_load = athlete_summary[
        "Current_Avg_Movement_Load"
    ].mean()

    # Previous average session load
    previous_total_trimp = athlete_summary[
        "Previous_Avg_Trimp"
    ].mean()

    previous_total_movement_load = athlete_summary[
        "Previous_Avg_Movement_Load"
    ].mean()

    trimp_label = "Avg TRIMP / Session"
    movement_label = "Avg Movement Load / Session"


# Current and previous average ACWR
average_acwr = athlete_summary[
    "Current_ACWR"
].mean()


previous_average_acwr = athlete_summary[
    "Previous_ACWR"
].mean()


# Current Movement Efficiency
if (
    pd.notna(total_trimp)
    and total_trimp != 0
):

    movement_efficiency = (
        total_movement_load
        / total_trimp
    )

else:

    movement_efficiency = float("nan")


# Previous Movement Efficiency
if (
    pd.notna(previous_total_trimp)
    and previous_total_trimp != 0
):

    previous_movement_efficiency = (
        previous_total_movement_load
        / previous_total_trimp
    )

else:

    previous_movement_efficiency = float("nan")


# Format cards
trimp_current, trimp_comparison = format_team_comparison(
    total_trimp,
    previous_total_trimp,
    decimals=0
)


movement_current, movement_comparison = format_team_comparison(
    total_movement_load,
    previous_total_movement_load,
    decimals=0
)


acwr_current, acwr_comparison = format_team_comparison(
    average_acwr,
    previous_average_acwr,
    decimals=2
)


efficiency_current, efficiency_comparison = format_team_comparison(
    movement_efficiency,
    previous_movement_efficiency,
    decimals=2
)


# Team cards
col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="team-card">
            <div class="team-card-title">
                {trimp_label}
            </div>
            <div class="team-card-value">
                {trimp_current}
            </div>
            <div class="team-card-comparison">
                {trimp_comparison}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""
        <div class="team-card">
            <div class="team-card-title">
                {movement_label}
            </div>
            <div class="team-card-value">
                {movement_current}
            </div>
            <div class="team-card-comparison">
                {movement_comparison}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="team-card">
            <div class="team-card-title">
                Average ACWR
            </div>
            <div class="team-card-value">
                {acwr_current}
            </div>
            <div class="team-card-comparison">
                {acwr_comparison}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="team-card">
            <div class="team-card-title">
                Movement Efficiency
            </div>
            <div class="team-card-value">
                {efficiency_current}
            </div>
            <div class="team-card-comparison">
                {efficiency_comparison}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ---------------------------------------------------------
# ACWR GUIDE
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">ACWR Guide</div>',
    unsafe_allow_html=True
)


acwr1, acwr2, acwr3, acwr4, acwr5 = st.columns(5)


with acwr1:

    st.markdown(
        """
        <div class="guide-card">
            <div class="guide-title">🟡 &lt; 0.80</div>
            <div class="guide-description">
                Low Load
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with acwr2:

    st.markdown(
        """
        <div class="guide-card">
            <div class="guide-title">🟢 0.80–1.30</div>
            <div class="guide-description">
                Sweet Spot
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with acwr3:

    st.markdown(
        """
        <div class="guide-card">
            <div class="guide-title">🟡 1.30–1.50</div>
            <div class="guide-description">
                Elevated
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with acwr4:

    st.markdown(
        """
        <div class="guide-card">
            <div class="guide-title">🟠 1.50–1.80</div>
            <div class="guide-description">
                Danger Zone
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with acwr5:

    st.markdown(
        """
        <div class="guide-card">
            <div class="guide-title">🔴 &gt; 1.80</div>
            <div class="guide-description">
                Danger Zone 2
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# CMJ GUIDE
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">CMJ Guide</div>',
    unsafe_allow_html=True
)


cmj1, cmj2, cmj3, cmj4 = st.columns(4)


with cmj1:

    st.markdown(
        """
        <div class="guide-card">
            <div class="guide-title">🟢 Above</div>
            <div class="guide-description">
                Above baseline
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with cmj2:

    st.markdown(
        """
        <div class="guide-card">
            <div class="guide-title">🟡 Within</div>
            <div class="guide-description">
                Within baseline
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with cmj3:

    st.markdown(
        """
        <div class="guide-card">
            <div class="guide-title">🔴 Below</div>
            <div class="guide-description">
                Below baseline
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with cmj4:

    st.markdown(
        """
        <div class="guide-card">
            <div class="guide-title">⚪ No Baseline</div>
            <div class="guide-description">
                Baseline not established
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# ATHLETE TABLE
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Athlete Monitoring</div>',
    unsafe_allow_html=True
)


# Make a copy
display_data = athlete_summary.copy()


# Create readable athlete name
display_data["Name"] = (
    display_data["Name Key"]
    .str.replace("|", " ", regex=False)
)


# ---------------------------------------------------------
# SAVE CMJ STATUS FOR COLORING
# ---------------------------------------------------------

status_lookup = dict(
    zip(
        display_data["Name"],
        display_data["CMJ Status"]
    )
)


# ---------------------------------------------------------
# CREATE ATHLETE COMPARISON COLUMNS
# ---------------------------------------------------------

# ---------------------------------------------------------
# TRIMP AND MOVEMENT LOAD DISPLAY
# ---------------------------------------------------------

if load_calculation == "Cumulative":

    display_data["7-Day TRIMP"] = display_data.apply(
        lambda row: format_athlete_comparison(
            row["Current_7Day_Trimp"],
            row["Previous_7Day_Trimp"],
            decimals=0
        ),
        axis=1
    )

    display_data["7-Day Movement Load"] = display_data.apply(
        lambda row: format_athlete_comparison(
            row["Current_7Day_Movement_Load"],
            row["Previous_7Day_Movement_Load"],
            decimals=0
        ),
        axis=1
    )

else:

    display_data["7-Day TRIMP"] = display_data.apply(
        lambda row: format_athlete_comparison(
            row["Current_Avg_Trimp"],
            row["Previous_Avg_Trimp"],
            decimals=1
        ),
        axis=1
    )

    display_data["7-Day Movement Load"] = display_data.apply(
        lambda row: format_athlete_comparison(
            row["Current_Avg_Movement_Load"],
            row["Previous_Avg_Movement_Load"],
            decimals=1
        ),
        axis=1
    )

# Change column names for average view
if load_calculation == "Average / Session":

    display_data = display_data.rename(
        columns={
            "7-Day TRIMP": "Avg TRIMP / Session",
            "7-Day Movement Load": "Avg Movement Load / Session"
        }
    )


display_data["ACWR"] = display_data.apply(
    lambda row: format_athlete_comparison(
        row["Current_ACWR"],
        row["Previous_ACWR"],
        decimals=2
    ),
    axis=1
)


display_data["Movement Efficiency"] = display_data.apply(
    lambda row: format_athlete_comparison(
        row["Current_Movement_Efficiency"],
        row["Previous_Movement_Efficiency"],
        decimals=2
    ),
    axis=1
)


# ---------------------------------------------------------
# COMBINE CMJ VALUE + DATE
# ---------------------------------------------------------

def format_cmj(row):

    current_cmj = row["Latest Avg (in)"]
    current_date = row["Latest Date"]


    if pd.isna(current_cmj):

        return "—"


    cmj_text = f"{current_cmj:.1f}"


    if pd.isna(current_date):

        return cmj_text


    current_date = pd.to_datetime(
        current_date
    )


    date_text = (
        f"{current_date.month}/"
        f"{current_date.day}/"
        f"{current_date.year}"
    )


    return (
        f"{cmj_text}\n"
        f"{date_text}"
    )


display_data["Latest CMJ"] = display_data.apply(
    format_cmj,
    axis=1
)


# ---------------------------------------------------------
# COMBINE BASELINE RANGE
# ---------------------------------------------------------

def format_baseline(row):

    low = row["Baseline Low (in)"]
    high = row["Baseline High (in)"]


    if pd.isna(low) or pd.isna(high):

        return "—"


    if low == 0 and high == 0:

        return "—"


    return (
        f"{low:.1f}–"
        f"{high:.1f}"
    )


display_data["Baseline"] = display_data.apply(
    format_baseline,
    axis=1
)


# ---------------------------------------------------------
# SELECT TABLE COLUMNS
# ---------------------------------------------------------

if load_calculation == "Cumulative":

    display_data = display_data[
        [
            "Name",
            "7-Day TRIMP",
            "7-Day Movement Load",
            "ACWR",
            "Movement Efficiency",
            "Latest CMJ",
            "Baseline"
        ]
    ]

else:

    display_data = display_data[
        [
            "Name",
            "Avg TRIMP / Session",
            "Avg Movement Load / Session",
            "ACWR",
            "Movement Efficiency",
            "Latest CMJ",
            "Baseline"
        ]
    ]

# ---------------------------------------------------------
# ACWR COLOR FUNCTION
# ---------------------------------------------------------

def color_acwr(value):

    if pd.isna(value):

        return ""


    try:

        current_value = float(
            str(value).split("\n")[0]
        )

    except (ValueError, TypeError):

        return ""


    if current_value < 0.80:

        return (
            "background-color: #FFF3CD;"
            "color: #856404;"
            "font-weight: 700;"
        )


    elif current_value <= 1.30:

        return (
            "background-color: #D4EDDA;"
            "color: #155724;"
            "font-weight: 700;"
        )


    elif current_value <= 1.50:

        return (
            "background-color: #FFF3CD;"
            "color: #856404;"
            "font-weight: 700;"
        )


    elif current_value <= 1.80:

        return (
            "background-color: #FFE0B2;"
            "color: #7A4B00;"
            "font-weight: 700;"
        )


    else:

        return (
            "background-color: #F8D7DA;"
            "color: #721C24;"
            "font-weight: 700;"
        )


# ---------------------------------------------------------
# CMJ COLOR FUNCTION
# ---------------------------------------------------------

def color_latest_cmj(row):

    status = status_lookup.get(
        row["Name"],
        "No Baseline"
    )


    if status == "Above":

        style = (
            "background-color: #D4EDDA;"
            "color: #155724;"
            "font-weight: 700;"
        )


    elif status == "Within":

        style = (
            "background-color: #FFF3CD;"
            "color: #856404;"
            "font-weight: 700;"
        )


    elif status == "Below":

        style = (
            "background-color: #F8D7DA;"
            "color: #721C24;"
            "font-weight: 700;"
        )


    else:

        style = (
            "background-color: #E9ECEF;"
            "color: #6C757D;"
            "font-weight: 700;"
        )


    return pd.Series(
        [
            style
            if column == "Latest CMJ"
            else ""
            for column in row.index
        ],
        index=row.index
    )


# ---------------------------------------------------------
# STYLE TABLE
# ---------------------------------------------------------

styled_data = display_data.style


# Color ACWR
styled_data = styled_data.map(
    color_acwr,
    subset=["ACWR"]
)


# Color Latest CMJ
styled_data = styled_data.apply(
    color_latest_cmj,
    axis=1
)


# ---------------------------------------------------------
# DISPLAY TABLE
# ---------------------------------------------------------

st.dataframe(
    styled_data,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Name": st.column_config.TextColumn(
            "Athlete",
            width="medium"
        ),

        (
    "Avg TRIMP / Session"
    if load_calculation == "Average / Session"
    else "7-Day TRIMP"
): st.column_config.TextColumn(
    (
        "Avg TRIMP / Session"
        if load_calculation == "Average / Session"
        else "7-Day TRIMP"
    ),
    width="medium"
),

(
    "Avg Movement Load / Session"
    if load_calculation == "Average / Session"
    else "7-Day Movement Load"
): st.column_config.TextColumn(
    (
        "Avg Movement Load / Session"
        if load_calculation == "Average / Session"
        else "7-Day Movement Load"
    ),
    width="medium"
),

        "ACWR": st.column_config.TextColumn(
            "ACWR",
            width="medium"
        ),

        "Movement Efficiency": st.column_config.TextColumn(
            "Movement Efficiency",
            width="medium"
        ),

        "Latest CMJ": st.column_config.TextColumn(
            "Latest CMJ",
            width="medium"
        ),

        "Baseline": st.column_config.TextColumn(
            "Baseline",
            width="small"
        )
    }
)


# ---------------------------------------------------------
# TABLE NOTE
# ---------------------------------------------------------

st.markdown(
    """
    <div class="table-note">
        <strong>All data displayed in this dashboard is synthetic, and randomly generated for demonstration purposes only. It does not represent actual athlete performance data.</strong>
        Current values are shown in bold.
        Values in parentheses show the previous 7-day value followed by
        the percentage change from the previous 7-day period.
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        Athlete Monitoring Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

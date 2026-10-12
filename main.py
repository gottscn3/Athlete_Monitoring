import pandas as poe


def build_athlete_summary(file_path, selected_date):

    firstbeat = poe.read_excel(
        file_path,
        sheet_name="Firstbeat"
    )

    # Clean numeric Firstbeat columns
    for column in ["Trimp", "Movement Load", "ACWR"]:
        firstbeat[column] = poe.to_numeric(
            firstbeat[column],
            errors="coerce"
        )

    # --------------------------------------------------
    # CURRENT 7-DAY WINDOW
    # --------------------------------------------------

    current_start = selected_date - poe.Timedelta(days=6)

    current_7 = firstbeat[
        (firstbeat["Date"] >= current_start) &
        (firstbeat["Date"] <= selected_date)
    ]

    current_summary = current_7.groupby("Name Key").agg(
        Current_7Day_Trimp=(
            "Trimp",
            lambda x: x.sum(min_count=1)
        ),
        Current_7Day_Movement_Load=(
            "Movement Load",
            lambda x: x.sum(min_count=1)
        ),

        # Count days with actual TRIMP data
        Current_Session_Days=(
            "Trimp",
            lambda x: x.notna().sum()
        )
    ).reset_index()

    # --------------------------------------------------
    # PREVIOUS 7-DAY WINDOW
    # --------------------------------------------------

    previous_end = selected_date - poe.Timedelta(days=7)
    previous_start = selected_date - poe.Timedelta(days=13)

    previous_7 = firstbeat[
        (firstbeat["Date"] >= previous_start) &
        (firstbeat["Date"] <= previous_end)
    ]

    previous_summary = previous_7.groupby("Name Key").agg(
        Previous_7Day_Trimp=(
            "Trimp",
            lambda x: x.sum(min_count=1)
        ),
        Previous_7Day_Movement_Load=(
            "Movement Load",
            lambda x: x.sum(min_count=1)
        ),

        # Count days with actual TRIMP data
        Previous_Session_Days=(
            "Trimp",
            lambda x: x.notna().sum()
        )
    ).reset_index()

    # --------------------------------------------------
    # COMBINE CURRENT + PREVIOUS
    # --------------------------------------------------

    athlete_summary = current_summary.merge(
        previous_summary,
        on="Name Key",
        how="outer"
    )

    # --------------------------------------------------
    # CURRENT ACWR
    # --------------------------------------------------

    current_day = firstbeat[
        firstbeat["Date"] == selected_date
    ]

    athlete_summary = athlete_summary.merge(
        current_day[["Name Key", "ACWR"]],
        on="Name Key",
        how="left"
    )

    athlete_summary = athlete_summary.rename(
        columns={
            "ACWR": "Current_ACWR"
        }
    )

    # --------------------------------------------------
    # PREVIOUS ACWR
    # Use the ACWR from one week earlier
    # --------------------------------------------------

    previous_acwr_date = selected_date - poe.Timedelta(days=7)

    previous_acwr = firstbeat[
        firstbeat["Date"] == previous_acwr_date
    ][["Name Key", "ACWR"]].copy()

    previous_acwr = previous_acwr.rename(
        columns={
            "ACWR": "Previous_ACWR"
        }
    )

    athlete_summary = athlete_summary.merge(
        previous_acwr,
        on="Name Key",
        how="left"
    )

    # --------------------------------------------------
    # MOVEMENT EFFICIENCY
    # --------------------------------------------------

    athlete_summary["Current_Movement_Efficiency"] = (
        athlete_summary["Current_7Day_Movement_Load"]
        / athlete_summary["Current_7Day_Trimp"]
    )

    athlete_summary["Previous_Movement_Efficiency"] = (
        athlete_summary["Previous_7Day_Movement_Load"]
        / athlete_summary["Previous_7Day_Trimp"]
    )

    # --------------------------------------------------
    # AVERAGE LOAD PER SESSION
    # --------------------------------------------------

    athlete_summary["Current_Avg_Trimp"] = (
        athlete_summary["Current_7Day_Trimp"]
        / athlete_summary["Current_Session_Days"]
    )

    athlete_summary["Current_Avg_Movement_Load"] = (
        athlete_summary["Current_7Day_Movement_Load"]
        / athlete_summary["Current_Session_Days"]
    )

    athlete_summary["Previous_Avg_Trimp"] = (
        athlete_summary["Previous_7Day_Trimp"]
        / athlete_summary["Previous_Session_Days"]
    )

    athlete_summary["Previous_Avg_Movement_Load"] = (
        athlete_summary["Previous_7Day_Movement_Load"]
        / athlete_summary["Previous_Session_Days"]
    )

    # --------------------------------------------------
    # CMJ DATA
    # --------------------------------------------------

    master = poe.read_excel(
        file_path,
        sheet_name="MASTER",
        header=1
    )

    cmj_data = master[
        [
            "Match Key",
            "Latest Avg (in)",
            "Latest Date",
            "Baseline Low (in)",
            "Baseline High (in)"
        ]
    ].copy()

    athlete_summary = athlete_summary.merge(
        cmj_data,
        left_on="Name Key",
        right_on="Match Key",
        how="left"
    )

    # --------------------------------------------------
    # CMJ STATUS
    # --------------------------------------------------

    def classify_cmj(row):

        if (
            row["Baseline Low (in)"] == 0
            and row["Baseline High (in)"] == 0
        ):
            return "No Baseline"

        elif row["Latest Avg (in)"] < row["Baseline Low (in)"]:
            return "Below"

        elif row["Latest Avg (in)"] > row["Baseline High (in)"]:
            return "Above"

        else:
            return "Within"

    athlete_summary["CMJ Status"] = athlete_summary.apply(
        classify_cmj,
        axis=1
    )

    # --------------------------------------------------
    # CLEAN UP
    # --------------------------------------------------

    athlete_summary = athlete_summary.drop(
        columns=["Match Key"]
    )

    return athlete_summary


# ---------------------------------
# Run the function
# ---------------------------------

if __name__ == "__main__":

    file_path = "WSOC OVR Jump Data Copy.xlsx"

    selected_date = poe.Timestamp("2026-09-15")

    print("\nSelected date:")
    print(selected_date)

    athlete_summary = build_athlete_summary(
        file_path,
        selected_date
    )

    print("\nFinal Athlete Summary:")
    print(athlete_summary)
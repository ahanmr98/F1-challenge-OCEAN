"""
Tyre strategies during a race
=============================
"""

from matplotlib import pyplot as plt

import fastf1
import fastf1.plotting

races  = ['Australian Grand Prix', 'Austrian Grand Prix',
       'Bahrain Grand Prix', 'Belgian Grand Prix', 'British Grand Prix',
       'Canadian Grand Prix', 'Chinese Grand Prix', 'Dutch Grand Prix',
       'Emilia Romagna Grand Prix', 'Hungarian Grand Prix',
       'Japanese Grand Prix', 'Miami Grand Prix', 'Monaco Grand Prix',
       'Saudi Arabian Grand Prix', 'Spanish Grand Prix', 'Italian Grand Prix']

for race in races:
    session = fastf1.get_session(2024, race, 'R')
    session.load()
    laps = session.laps

    ###############################################################################
    # Get the list of driver numbers
    drivers = session.drivers
    print(drivers)

    ###############################################################################
    # Convert the driver numbers to three letter abbreviations
    drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]
    print(drivers)

    ###############################################################################
    # We need to find the stint length and compound used
    # for every stint by every driver.
    stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
    stints = stints.groupby(["Driver", "Stint", "Compound"])
    stints = stints.count().reset_index()

    ###############################################################################
    # The number in the LapNumber column now stands for the number of observations
    # in that group aka the stint length.
    stints = stints.rename(columns={"LapNumber": "StintLength"})
    print(stints)

    ###############################################################################
    # Now we can plot the strategies for each driver
    fig, ax = plt.subplots(figsize=(5, 10))

    # Create a list to store legend handles
    legend_elements = []

    for driver in drivers:
        driver_stints = stints.loc[stints["Driver"] == driver]

        previous_stint_end = 0
        for idx, row in driver_stints.iterrows():
            compound_color = fastf1.plotting.get_compound_color(row["Compound"],
                                                                session=session)
            bar = plt.barh(
                y=driver,
                width=row["StintLength"],
                left=previous_stint_end,
                color=compound_color,
                edgecolor="black",
                fill=True
            )

            # Add text to display stint length on each bar
            plt.text(
                x=previous_stint_end + row["StintLength"]/2,
                y=driver,
                s=str(row["StintLength"]),
                va='center',
                ha='center',
                color='black',
                fontweight='bold'
            )

            # Add compound to legend if not already present
            if row["Compound"] not in [l.get_label() for l in legend_elements]:
                legend_elements.append(plt.Rectangle((0,0),1,1,fc=compound_color,label=row["Compound"]))

            previous_stint_end += row["StintLength"]

    # Add the legend
    ax.legend(handles=legend_elements, title="Tire Compounds", loc="lower right")

    ###############################################################################
    # Make the plot more readable and intuitive
    plt.title("2024 {race} Strategies".format(race=race))
    plt.xlabel("Lap Number")
    plt.grid(False)
    # invert the y-axis so drivers that finish higher are closer to the top
    ax.invert_yaxis()

    ###############################################################################
    # Plot aesthetics
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()
    
    # Save the figure
    plt.savefig(f'/home/ubuntu/desights/f1/2024_final/tyre_strategy/2024_{race.replace(" ", "_")}_Strategies_random_pretty.png', dpi=300, bbox_inches='tight')
    
    plt.show()

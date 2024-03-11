
# Project Abstract: Optimizing Home Energy Management through AI-Based Predictive Control

## Background
The project addresses the increasing demand for cost-effective and sustainable energy management systems, particularly in the context of rising investments in renewable energy sources. With the global shift towards green energy and the integration of smart grid technologies in residential environments, the need for advanced energy prediction and management solutions is becoming more urgent. This research aims to improve energy management efficiency in households, aiming to reduce operational costs while contributing to a more sustainable energy supply.

## Collaboration
The research is conducted in collaboration with "iLumen," a leading company in the renewable energy solutions sector. iLumen focuses on developing innovative products and systems in solar energy, energy storage, and smart energy management technologies. This project marks a significant step forward in developing advanced, AI-based energy management solutions for households.

## Research Questions
1. How can AI-based machine learning be utilized to predict and optimize energy consumption in households, aiming for cost savings and more efficient use of renewable energy sources?
2. How can we develop a realistic and effective simulation environment for testing and validating energy management systems in household settings?
3. How can accurate predictions of household energy consumption be made based on variables such as grid injection and withdrawal, weather conditions, and dynamic energy prices?
4. How can decision-making algorithms be developed to respond to predicted energy needs, energy prices, and weather conditions to minimize costs while meeting household energy demands?
5. What are the potential cost savings and efficiency improvements that can be achieved by implementing AI-based energy management systems in households with solar panels?

## Objectives
1. Develop a simulation environment enabling realistic simulation of energy consumption and production in household settings, accurately modeling the behavior of components like home batteries, hot water boilers, electric vehicle charging stations, and solar panels.
2. Develop a model capable of accurately predicting household energy consumption based on historical data and current variables such as grid injection and withdrawal, weather conditions, and dynamic energy prices.
3. Implement energy management systems in households with solar panels to result in demonstrable cost savings in the energy expenditures of participating households compared to previous energy management practices.









## TODO
    # add function to choose dates on solcast api
    # add the fluvius live prices and try to show it
    # use PyBamm instead of simple battery models
    # make a startup screen for user to fill in all simulation params
    # find better way to showcase results instead of tkinter
    # Peukert's law or the coulombic efficiency model
    # add more items like car charger and try to make them work together
    # adding function to choose ac or dc charging
    # add database to store simulations or simulation params

## KEEP IN MIND
    # battery will never be fully charged or discharged
    # depending on the soc the battery charge and discharge is not linear
    # efficiency is depending on the soc
    # verschil ac en dc laden toevoegen

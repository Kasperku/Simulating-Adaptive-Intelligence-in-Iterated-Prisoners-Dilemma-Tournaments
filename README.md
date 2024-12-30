# Iterated prisoners dilemma tournament

## Sensitivity Analysis of payoff dynamics in a Prisoner's dilemma tournament played by Adaptive AI and other traditional strategies

## Background and Context

In organizations, team dynamics play a crucial role in determining collective performance, productivity, and morale. Teams often consist of individuals with diverse behavioral tendencies, ranging from cooperative, altruistic workers to self-serving or even toxic counterparts. Individuals might be tempted to undermine the other, take full credit, or subtly sabotage the other’s effort to appear more competent, perhaps to compete for a promotion, though creating a harmonious work environment would make everyone better off. Understanding how these behaviors influence one another is essential for fostering an effective and harmonious workplace. The Prisoner's Dilemma, a fundamental concept in game theory, offers a robust framework for analyzing such interactions. It models the choices between cooperation and defection, mirroring the tension between collective goals and individual incentives. By applying this framework, this research examines how different behavioral archetypes—cooperative, competitive, and conditional—interact and influence team dynamics in workplace-like scenarios.

## Project Overview
This project simulates repeated interactions between bots playing the Prisoner's Dilemma, a fundamental game theory scenario. It models workplace dynamics where agents with varying behavioral strategies compete or cooperate over multiple rounds. The simulator allows for analyzing how different strategies influence individual and collective outcomes and evaluates the effects of adding or removing specific behaviors (e.g., toxic, overly cooperative).


## Features

- **Adaptive Learning Agent**: Implements Q-Learning agent that leanrs optimal strategy through the Bellman Equation (reinforcement learning)
- **Tournament Simulation**: Bots compete in a round-robin format, with multiple matches per pair and rounds per tournament
- **Data exported as a csv**: The tournament is run several times and exported as a csv for analysis.


## How to use

- **Run the Tournament:** Initialize the tournament with desired bots, number of rounds, and matches per pair.
- **Analyze Results:** Retrieve detailed match results or aggregated statistics to understand strategy performance.
- **Experiment:** Add or remove bots, change strategies, or modify the payoff matrix to explore dynamics.

# Fantasy Football Application

## Introduction

This is a simple Fantasy Football application built using Python, Tkinter for the GUI, and MySQL for the database. Users can log in, create their own team by selecting players, and see a leaderboard based on the points scored by their selected players.

## Features

* User login and creation.
* Selection of 5 players to form a team.
* Points calculation based on player statistics.
* Leaderboard display with ranking based on points.

## Requirements

* Python 3.x
* MySQL Server
* Tkinter (Pre-installed with Python)
* mysql-connector-python (Python package)

## Installation

1. Clone this repository.

   ```bash
   git clone <repository_url>
   ```

2. Install the MySQL Connector package:

   ```bash
   pip install mysql-connector-python
   ```

3. Set up the MySQL Server and create a database with the following credentials:

   * Host: localhost
   * User: root
   * Password: root123

## How to Run

1. Ensure your MySQL Server is running.
2. Run the Python script:

   ```bash
   python main.py
   ```

## Usage

* Enter your username to log in or create a new account.
* Select exactly 5 players from the list.
* View your team and points.
* Check the leaderboard to see the top performers.

## Database Structure

* `users`: Stores user information.
* `players`: Stores player information.
* `user_teams`: Stores user-player relationships (teams).
* `player_stats`: Stores player statistics for each match.
* `user_points`: Stores total points for each user.

## Acknowledgments

* Tkinter for GUI
* MySQL for database management

## License

This project is open-source and available for anyone to use or modify.

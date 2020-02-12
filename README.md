# Qízza
The self-driving pizza delivery robot! This project is an exploration into the reinforcement learning algorithm, [Q-learning](https://en.wikipedia.org/wiki/Q-learning). Inspired by the OpenAI Gym's Smartcab simulation, in the simulationa self-driving pizza delivery car learns to navigate a simple grid and deliver pizzas to various destinations.

This project is being created by members of the [DVHackers](http://www.dvhackers.com), a Computer Science club at Diablo Valley College.


# Organization
This project is split into 3 main parts:
* The Frontend: Building a visually appealing graphical representation of the simulation in HTML/CSS
* The Backend: The Environment - Handles game state, and reward table, Python. The Agent - Handles the Q-learning algorithm (Q-table, Q-function)
* The Controller: A websocket to provide quick connection between the backend and frontend, Python

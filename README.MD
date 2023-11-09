# UNO Multiplayer Project

This is a Python project for playing the famous UNO game with two players using the sockets library for client-server communication. It also uses the termcolor library for better card visualization in the terminal.

## Requirements

- Python 3.x
- Libraries: socket and termcolor
  ## Installation commands
  ```sh
  pip install termcolor
  ```
  ```sh
  pip install socket
  ```

## How to Run

- Change the variable _'HOST'_ to match the IP of the machine that will be used as the server and the variable _'PORT'_ to an available port.
- Execute the following command to start the server.
  ```sh
  python3 server.py
  ```
- Each player needs to execute the following command on their own machine.
  ```sh
  python3 client.py
  ```
- Change the variable _'HOST'_ in client.py to match the server's IP and the variable _'PORT'_ to a different port than the server's.
- Connect with another player using the software _Hamachi_ or another method to connect the machines' IPs.
- _Play UNO!_

## How to Play

The UNO game is a card game in which players play cards from their hands, matching color or number with the top card on the pile. Players can also play action cards that affect the next player. The goal is to get rid of all the cards in your hand before the other player.

## Acknowledgments

This project was inspired by other UNO multiplayer projects in Python available on GitHub. It was created for educational and learning purposes. If you find any bugs or have suggestions for improvements, feel free to open an issue or pull request on the repository.

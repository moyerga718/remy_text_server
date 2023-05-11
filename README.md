# Remy: A Text-Based Adventure (back-end server)

## About
Remy is a retro-inspired text-based adventure game. This repo is for the server-side portion of the game. 

## Technologies Used
This backend server was created using Python and Django. SQLite3 was used to clear out some data in the database that was no longer needed.

## How it works
The basic flow for how the game functions is as follows:

1. The user creates a game object.
2. The user is prompted with a situation on the client side. Ex. "There is a tree to the north of you with a red ball underneath it."
3. The user is given a text input to respond to the situation with an action. An action is any two-word phrase consisting of a verb and a noun. Ex. "Go North" or "Walk 
Tree".
4. The action text is sent to the back-end server. This string is then broken into individual words, checked to see if the verb and noun match any of the 
verbs and nouns that are in the database, checked to see if that verb-noun combination is a valid action for the current situation, and then checked to see if that
action has any other requirements necessary to be completed.
5. Once an action is completed, the situation for the game is updated, the user is given a new text input, and the process starts over. Ex. "You are standing under the tree."

All text parsing and game updates are completed within the handle_action custom action within the GameView viewset. A detailed docstring on the custom_action describes 
every step of the process. 

### ERD
ERD Link: https://dbdiagram.io/d/630f78fb0911f91ba508b99a

## How to play:
This app is deployed on Heroku, so no need to download the repo yourself. You can play it here: 
https://remy-adventure.herokuapp.com/

I've done a little bit of play testing to make sure game flow is smooth, but I'm always up for critique or input (including other actions, situaitons, etc...). Feel free to contact me with any suggestions!

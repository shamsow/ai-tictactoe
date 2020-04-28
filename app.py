import os
import time
import json

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
# from helper import *
from helper import winner, terminal, minimax, initial_state, result

# Use /python3 app.py/ to run

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app, async_mode = None)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@socketio.on("reset")
def reset_board():
    """Send the empty state of the board to reset the game"""
    board = initial_state()
    emit("update", board)
    

@socketio.on("action")
def make_move(json):
    """Send the state of the board after the desired move is made"""
    res = result(json["board"], tuple(json["move"]))
    emit("update", res)
   

@socketio.on("check_status")
def board_status(board):
    """Check the board to see if the game is over and send the result"""
    if terminal(board):
        victor = winner(board)
        if victor is not None:
            emit("game_over", "winner: " + victor)
        else:
            emit("game_over", "Draw")


@socketio.on("get_ai_move")
def generate_ai_move(board):
    """Determine the optimal move for the AI to make and the send it"""
    if terminal(board): # if the game is over, do nothing
        pass
    else: 
        move = minimax(board) # use minimax algorithm to generate optimal move
        res = result(board, move[0])
        emit("update", res)

# @socketio.on("new_message")
# def sent_message(json):
#     """Handle a new message being sent"""
#     # Log the timestamp
#     my_time = time.strftime('%H:%M:%S on %d/%m/%y')
#     # Assemble data into a dict
#     my_data = {"user": json["user"], "msg" : json["msg"], "my_time": my_time}
#     # Add data to the messages of the channel
#     my_messages[json["channel"]].append(my_data)
#     # Store only the 100 most recent messages per channel
#     if len(my_messages[json["channel"]]) > 100:
#     	my_messages[json["channel"]].pop(0)
#     # Pass the timestamp, message and username to the template
#     emit("announce message", my_data)

# @socketio.on("get_messages")
# def all_messages(channel):
#     if channel in my_messages:
#         data = my_messages
#         emit("broadcast messages", data)

@app.route("/")
def index():
    return render_template("home.html")

if __name__ == "__main__":
	socketio.run(app, debug = True)

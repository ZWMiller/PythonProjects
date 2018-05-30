from pymongo import MongoClient
import os
import time

client = MongoClient("mongodb://game:password@34.228.44.16/server_game")
db = client.server_game
col = db.live_players


def update_player_positions(col):
    board = []
    for i in range(10):
        board.append(["." for _ in range(10)])
    for member in col.find():
        board[member['y']%10][member['x']%10] = member['label']
    return board

board = update_player_positions(col)

def draw_map(board):
    for i in board:
        print(''.join([j for j in i]))

my_label = input("One character to represent your token: ")
d = {'x':0, 'y':0, 'label':str(my_label)}
result = col.insert_one(d)
my_id = result.inserted_id
draw_map(board)
while True:
    key = input("Use WSAD to move. q to quit: ")
    if key=='d':
        col.update_one({"_id": my_id}, {'$inc': { 'x': 1}})
    if key=='a':
        col.update_one({"_id": my_id}, {'$inc': { 'x': -1}})
    if key=='w':
        col.update_one({"_id": my_id}, {'$inc': { 'y': -1}})
    if key=='s':
        col.update_one({"_id": my_id}, {'$inc': { 'y': 1}})
    if key=='q':
        col.delete_one({"_id": my_id})
        break
    os.system('clear')
    board = update_player_positions(col)
    draw_map(board)
    time.sleep(.05)

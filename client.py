import socket
import threading

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-"*5)

def recv_moves(sock, board, mark, opponent_mark):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                continue
            if data.startswith("START"):
                global player_mark
                player_mark = data.split(":")[1]
                print(f"Game started! You are {player_mark}")
            else:
                row, col = map(int, data.split(","))
                board[row][col] = opponent_mark
                print_board(board)
        except:
            print("Disconnected from server")
            break

server_ip = input("Enter server IP: ")  # cloud server IP or localhost
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_ip, 5555))

board = [[" "]*3 for _ in range(3)]
player_mark = ""
opponent_mark = "O"  # will swap once game starts

# Start thread to receive moves
threading.Thread(target=recv_moves, args=(sock, board, player_mark, opponent_mark), daemon=True).start()

while True:
    move = input("Your move (row,col): ")
    row, col = map(int, move.split(","))
    board[row][col] = player_mark
    sock.send(f"{row},{col}".encode())

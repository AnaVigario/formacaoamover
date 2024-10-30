import random
from flask import Flask
app = Flask(__name__)

@app.route("/")

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    # Verificar linhas, colunas e diagonais
    for i in range(3):
        if all([cell == player for cell in board[i]]):
            return True
        if all([board[j][i] == player for j in range(3)]):
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def is_full(board):
    return all([cell != " " for row in board for cell in row])

import random

def player_move(board, player):
    # Obter todas as posições vazias
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    if empty_cells:
        # Escolher uma posição vazia aleatoriamente
        move = random.choice(empty_cells)
        board[move[0]][move[1]] = player

def computer_move(board):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    move = random.choice(empty_cells)
    board[move[0]][move[1]] = "O"

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Bem-vindo ao Jogo do Galo!")
    print_board(board)

    while True:
        # Movimento do Jogador X
        player_move(board, "X")
        print_board(board)
        if check_winner(board, "X"):
            print("Jogador X venceu!")
            break
        if is_full(board):
            print("Empate!")
            break

        # Movimento do Computador (O)
        computer_move(board)
        print("Computador fez um movimento:")
        print_board(board)
        if check_winner(board, "O"):
            print("Computador venceu!")
            break
        if is_full(board):
            print("Empate!")
            break

if __name__ == "__main__":
    main()

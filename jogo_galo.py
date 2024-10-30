import random
from flask import Flask, jsonify, request

app = Flask(__name__)

# Inicializando o tabuleiro como uma variável global
board = [[" " for _ in range(3)] for _ in range(3)]
current_player = "X"  # Define o jogador inicial como "X"

def print_board(board):
    return "\n".join([" | ".join(row) + "\n" + "-" * 5 for row in board])

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

def player_move(board, move, player):
    if 0 <= move < 9 and board[move // 3][move % 3] == " ":
        board[move // 3][move % 3] = player
        return True
    return False

def computer_move(board):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    if empty_cells:
        move = random.choice(empty_cells)
        board[move[0]][move[1]] = "O"

@app.route("/move", methods=["POST"])
def make_move():
    global board, current_player

    data = request.json
    move = data.get("move")

    if current_player != "X":
        return jsonify({"error": "Aguarde o turno do computador."}), 400

    if move is None or not (0 <= move < 9):
        return jsonify({"error": "Movimento inválido. Escolha um número entre 1 e 9."}), 400

    if not player_move(board, move, "X"):
        return jsonify({"error": "Movimento inválido. A posição já está ocupada ou fora do limite."}), 400

    # Verifica se o jogador venceu
    if check_winner(board, "X"):
        board_state = print_board(board)
        board = [[" " for _ in range(3)] for _ in range(3)]  # Reinicia o tabuleiro
        current_player = "X"
        return jsonify({"board": board_state, "message": "Jogador X venceu!"})

    # Verifica empate
    if is_full(board):
        board_state = print_board(board)
        board = [[" " for _ in range(3)] for _ in range(3)]  # Reinicia o tabuleiro
        current_player = "X"
        return jsonify({"board": board_state, "message": "Empate!"})

    # Movimento do computador
    computer_move(board)
    if check_winner(board, "O"):
        board_state = print_board(board)
        board = [[" " for _ in range(3)] for _ in range(3)]  # Reinicia o tabuleiro
        current_player = "X"
        return jsonify({"board": board_state, "message": "Computador venceu!"})

    # Verifica empate após o movimento do computador
    if is_full(board):
        board_state = print_board(board)
        board = [[" " for _ in range(3)] for _ in range(3)]  # Reinicia o tabuleiro
        current_player = "X"
        return jsonify({"board": board_state, "message": "Empate!"})

    current_player = "X"  # Passa o turno de volta para o jogador
    board_state = print_board(board)
    return jsonify({"board": board_state, "message": "Movimento registrado. Turno do jogador."})

@app.route("/status", methods=["GET"])
def get_status():
    board_state = print_board(board)
    return jsonify({"board": board_state, "message": "Status atual do jogo"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

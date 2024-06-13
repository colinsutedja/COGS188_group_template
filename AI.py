import random
from math import inf
from piece import *
from mc2 import *
# from mc import *
import io
import pickle
import dill
import pstats
import math
from collections import deque
from datetime import time
import matplotlib.pyplot as plt

import time
import cProfile

@staticmethod
def minimax(board, depth, alpha, beta, maximizing_player, maximizing_color):
    if depth == 0 or board.gameover:
        return None, evaluate_board(board, maximizing_color)
    moves = board.get_moves()
    best_move = random.choice(moves)

    if maximizing_player:
        max_eval = -inf
        for move in moves:
            board.make_move(move[0], move[1])
            current_eval = minimax(board, depth-1, alpha, beta, False, maximizing_color)[1]
            board.unmake_move()
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break
        return best_move, max_eval
    else:
        min_eval = inf
        for move in moves:
            board.make_move(move[0], move[1])
            current_eval = minimax(board, depth-1, alpha, beta, True, maximizing_color)[1]
            board.unmake_move()
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
        return best_move, min_eval
    
@staticmethod

def no_pruning(board, depth, alpha, beta, maximizing, player_color):
    if depth == 0 or board.gameover:
        return None, evaluate_board(board, player_color)
    moves = board.get_moves()
    best_move = random.choice(moves)

    if maximizing:
        max_eval = -inf
        for move in moves:
            board.make_move(move[0], move[1])
            current_eval = minimax(board, depth-1, alpha, beta, False, player_color)[1]
            board.unmake_move()
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move
            alpha = max(alpha, current_eval)
            
        return best_move, max_eval
    else:
        min_eval = inf
        for move in moves:
            board.make_move(move[0], move[1])
            current_eval = minimax(board, depth-1, alpha, beta, True, player_color)[1]
            board.unmake_move()
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            beta = min(beta, current_eval)
            
        return best_move, min_eval
    
@staticmethod
def monte_carlo(board):
    mcts = MonteCarloTreeSearchNode(board)
    best_move = mcts.best_action()
    return best_move

def heuristic_ai(board, player_color):
    moves = board.get_moves()
    best_move = None
    best_eval = -inf if player_color == WHITE else inf

    for move in moves:
        try:
            board.make_move(move[0], move[1])
            eval_value = evaluate_board(board, player_color)

            if (player_color == WHITE and eval_value > best_eval) or (player_color == BLACK and eval_value < best_eval):
                best_eval = eval_value
                best_move = move
        except Exception as e:
            print(f"Error evaluating move {move}: {e}")
        finally:
            board.unmake_move()

    return best_move
    
@staticmethod
def evaluate_board(board, player_color):
    if player_color == WHITE:
        return board.whiteScore - board.blackScore
    else:
        return board.blackScore - board.whiteScore

@staticmethod
def random_move(board):
    moves = board.get_moves()
    if moves:
        return random.choice(moves)
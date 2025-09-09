from tictactoe import player, X, O, EMPTY, initial_state, actions, result, winner
from copy import deepcopy

test_board= initial_state()

def test_player_at_the_start():
    assert player(test_board) == X

def test_player_mid_stage():
    current_board = deepcopy(test_board) 
    current_board[0][1] =X
    current_board[1][2]=O
    current_board[1][0] = X 
    assert player(current_board) == O

def test_actions():    
    assert actions(test_board) == [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]

def test_result():
    current_board = [[X, EMPTY, EMPTY],
            [EMPTY, O, X],
            [EMPTY, EMPTY, EMPTY]]
    assert result(current_board, (2,0)) == [[X, EMPTY, EMPTY],
                                            [EMPTY, O, X],
                                            [O, EMPTY, EMPTY]] 

def test_winner_for_row_match():
    current_board = [[X, EMPTY, EMPTY],
            [O, O, O],
            [EMPTY, EMPTY, EMPTY]]
    assert winner(current_board) == O

def test_winner_for_column_match():
    current_board = [[X, EMPTY, EMPTY],
            [X, O, O],
            [X, EMPTY, EMPTY]]
    assert winner(current_board) == X

def test_winner_for_row_match():
    current_board = [[X, EMPTY, EMPTY],
            [O, X, O],
            [EMPTY, EMPTY, X]]
    assert winner(current_board) == X

def test_winner_for_row_match():
    current_board = [[X, EMPTY, O],
            [O, O, O],
            [O, EMPTY, EMPTY]]
    assert winner(current_board) == O

def test_winner_for_no_match():
    current_board = [[X, EMPTY, EMPTY],
            [O, EMPTY, O],
            [EMPTY, EMPTY, EMPTY]]
    assert winner(current_board) == None
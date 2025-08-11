from tictactoe import player, X, O, EMPTY, initial_state

test_board= initial_state()

def test_player_at_the_start():
    assert player(test_board) == X

def test_player_mid_stage():
    test_board[0][1] =X
    test_board[1][2]=O
    test_board[1][0] = X
    test_board[2][0] = O
    print(test_board)
    assert player(test_board) == X
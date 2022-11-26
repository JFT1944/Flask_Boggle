from flask import Flask, session, request, render_template, jsonify
from boggle import Boggle


app = Flask(__name__)
boggle_game = Boggle()
app.config['SECRET_KEY'] = 'Big Time Secret'

already_answered = []

@app.route('/')
def home():
    '''This is the homepage, where the board lives essentially'''
    
    boggle_board = boggle_game.make_board()
    session['gameboard'] = boggle_board

    return render_template('boggle.html', boggle_board=boggle_board)

@app.route('/answers/')
def checking_answers():
    '''This is how answers are checked'''
    bguess = request.args['guess']
    board = session['gameboard']
    # return jsonify(f'{guess}')
    
    
    if bguess in already_answered:
        return jsonify('already chosen')
    already_answered.append(bguess)
    print(f'bguess: {bguess}')
    
    is_answer = boggle_game.check_valid_word(board, bguess)
    print(is_answer)


    return jsonify(is_answer)
@app.route('/stats')
def stats():
    '''This is the route that is taken to record the stats of the player
    including highscore and times-played'''
    new_game_finished = request.args['finished']
    new_score = request.args['nscore']
    oldgame = session['games-played']
    if new_game_finished == 'true':
        oldgame = oldgame + 1
        session['games-played'] = oldgame
    if new_score >= session['score']:
        session['score'] = new_score


    return f"The stats of the player are {session['games-played']}, {session['score']}"
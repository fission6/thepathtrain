from flask import Flask, render_template, Response
app = Flask(__name__)

from data_import import times

@app.route('/from/<int:from_id>/to/<int:to_id>/')
def hello(from_id, to_id):

    if from_id and to_id:
        times_json = times(from_id, to_id)
        return Response(times_json, mimetype='application/json')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
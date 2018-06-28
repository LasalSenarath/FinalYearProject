from flask import Flask, render_template, request, jsonify
# from FlaskApp.src.SparqlQueries import runQuery
# from FlaskApp.src.SparqlQueries import runQuery
import Test.new as t

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/byMaterialSearch', methods=['POST'])
def byMatSearch():
    return jsonify(t.MyTest(request.form['message']))

app.run()
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def selectionScreen():
    return render_template('selectionScreen.html')


if __name__ == "__main__":
    app.run(debug=True)
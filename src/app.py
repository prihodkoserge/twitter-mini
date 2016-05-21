from flask import Flask
app = Flask("Mini Twitter")

@app.route('/')
def index():
    return "Main page"

if __name__ == '__main__':
    app.run()
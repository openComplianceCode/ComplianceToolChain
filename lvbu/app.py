from flask import Flask, render_template, request, jsonify
from src.compatibility import check_process

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])

def index(name=None):
    print("Hello!")
    return render_template('conflict.html', name = name)

@app.route('/conflict', methods=['GET', 'POST'])
def conflict():
    return render_template('conflict.html')

@app.route('/search_conflict', methods=['GET', 'POST'])
def search_conflict():
    print("Hello!")
    license_start = request.args.get('license_start')
    license_end = request.args.get('license_end')
    print("Hello!")
    usage = request.args.get('usage')
    json_data=check_process(license_start, license_end, usage)
    print(json_data)
    return jsonify(json_data)

if __name__ == '__main__':
    app.debug=True
    app.run()


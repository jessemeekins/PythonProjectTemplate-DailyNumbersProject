from flask import Flask, jsonify, send_file

app = Flask(__name__)



@app.route('/api/roster', methods=['GET'])
def get_data():
    roster = "/Users/jessemeekins/Documents/VS_CODE/mfd-numbers-nextjs/public/full_roster.json"
    return send_file(roster, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='192.168.1.162', port=5000, debug=True)

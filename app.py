from flask import Flask, render_template, request, jsonify
import csv
import os  # To read environment variables

app = Flask(__name__)

filename = 'college_branches_cutoff.csv'

def find_top_3_colleges(jee_rank, filename):
    eligible_options = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                college_name = row['College']
                branch = row['Branch']
                cutoff_rank_str = row['Rank']
                if cutoff_rank_str.isdigit():
                    cutoff_rank = int(cutoff_rank_str)
                    if jee_rank <= cutoff_rank:
                        eligible_options.append((college_name, branch, cutoff_rank))
        eligible_options.sort(key=lambda x: x[2])  # Sort by cutoff rank (ascending)
        return eligible_options[:3]  # Return top 3 options
    except FileNotFoundError:
        return None

@app.route('/api/colleges', methods=['POST'])
def api_colleges():
    try:
        data = request.get_json()
        jee_rank = int(data['jee_rank'])
        top_3_colleges = find_top_3_colleges(jee_rank, filename='college_branches_cutoff.csv')

        if top_3_colleges is None:
            return jsonify({"error": "File not found"}), 404

        response = [
            {"college": college, "branch": branch, "cutoff_rank": cutoff_rank}
            for college, branch, cutoff_rank in top_3_colleges
        ]
        return jsonify(response), 200

    except (ValueError, KeyError):
        return jsonify({"error": "Invalid input"}), 400

if __name__ == '__main__':
    # Ensure Flask uses the correct port set by Render (or default to port 5000)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

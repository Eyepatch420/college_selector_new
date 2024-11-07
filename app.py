from flask import Flask, render_template, request, jsonify
import csv
import os

app = Flask(__name__)

# Define the file path relative to the project root directory
filename = os.path.join(os.path.dirname(__file__), 'college_branches_cutoff')

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
        # Parse JSON request data
        data = request.get_json()
        jee_rank = int(data['jee_rank'])
        top_3_colleges = find_top_3_colleges(jee_rank, filename=filename)
        
        if top_3_colleges is None:
            return jsonify({"error": "File not found"}), 404

        # Prepare response
        response = [
            {"college": college, "branch": branch, "cutoff_rank": cutoff_rank}
            for college, branch, cutoff_rank in top_3_colleges
        ]
        return jsonify(response), 200
    except (ValueError, KeyError):
        return jsonify({"error": "Invalid input"}), 400

if __name__ == '__main__':
    app.run(debug=True)

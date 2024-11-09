from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS
import os
import csv

app = Flask(__name__)
CORS(app, origins=["https://rankbridge.onrender.com"])  # Enable CORS for the frontend URL

# Path to the static folder
static_folder = os.path.join(app.root_path, 'static')

# New filename pointing to the CSV inside the static folder
filename = os.path.join(static_folder, 'college_branches_cutoff.csv')

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

@app.route('/')
def home():
    return "Welcome to the College Selector API!"

@app.route('/', methods=['POST'])
def api_colleges():
    try:
        data = request.get_json()
        jee_rank = int(data['jee_rank'])
        top_3_colleges = find_top_3_colleges(jee_rank, filename)

        if top_3_colleges is None:
            return jsonify({"error": "File not found"}), 404

        response = [
            {"college": college, "branch": branch, "cutoff_rank": cutoff_rank}
            for college, branch, cutoff_rank in top_3_colleges
        ]
        return jsonify(response), 200

    except (ValueError, KeyError):
        return jsonify({"error": "Invalid input"}), 400

# Optional: Add a route to test accessing the static CSV file directly
@app.route('/test-csv')
def test_csv():
    try:
        return send_from_directory(static_folder, 'college_branches_cutoff.csv')
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)

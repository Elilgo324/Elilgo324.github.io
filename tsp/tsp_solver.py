from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/solve_tsp', methods=['POST'])
def solve_tsp_route():
    data = request.json
    points = data['points']

    points = set(points)
    nearest = points.pop()
    tour = [nearest]

    while points:
        nearest = min(points, key=lambda p: (nearest[0] - p[0])**2 + (nearest[1] - p[1])**2)
        tour.append(nearest)

    tour.append(tour[0])
    return jsonify(tour)

if __name__ == '__main__':
    app.run(debug=True)

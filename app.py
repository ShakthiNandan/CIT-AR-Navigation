import json, math
from heapq import heappush, heappop
from flask import Flask, request, jsonify, send_from_directory, render_template

app = Flask(__name__)

# Load scenes once
with open('static/scenes.json') as f:
    scenes = json.load(f)     # list of { title, latitude, longitude }

n = len(scenes)

# Haversine distance in kilometers
def haversine(i, j):
    lat1, lon1 = math.radians(scenes[i]['latitude']), math.radians(scenes[i]['longitude'])
    lat2, lon2 = math.radians(scenes[j]['latitude']), math.radians(scenes[j]['longitude'])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * 6371 * math.asin(math.sqrt(a))

# Build a k-nearest-neighbor graph
def build_graph(k=4):
    # Precompute all pairwise haversine distances
    dists = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            d = haversine(i, j)
            dists[i][j] = dists[j][i] = d

    graph = {i: [] for i in range(n)}
    for i in range(n):
        # find k smallest distances (excluding self)
        neighbors = sorted(
            [(dists[i][j], j) for j in range(n) if j != i],
            key=lambda x: x[0]
        )[:k]
        graph[i] = [j for (_, j) in neighbors]
    return graph

# Build graph with desired k (e.g., 4 nearest neighbors)
graph = build_graph(k=4)

# A* search over the graph
def astar(start, goal):
    open_set = [(haversine(start, goal), 0, start, [start])]
    g_score = {i: float('inf') for i in range(n)}
    g_score[start] = 0
    visited = set()

    while open_set:
        f_score, g, curr, path = heappop(open_set)
        if curr == goal:
            return path
        if curr in visited:
            continue
        visited.add(curr)

        for nbr in graph[curr]:
            tentative_g = g + haversine(curr, nbr)
            if tentative_g < g_score[nbr]:
                g_score[nbr] = tentative_g
                f = tentative_g + haversine(nbr, goal)
                heappush(open_set, (f, tentative_g, nbr, path + [nbr]))
    return []

@app.route('/')
def index():
    return render_template('ar_navigator.html')

@app.route('/scenes.json')
def scenes_route():
    return send_from_directory('static', 'scenes.json')

@app.route('/api/route')
def api_route():
    try:
        start_idx = int(request.args.get('from', 0))
        end_idx   = int(request.args.get('to',   0))
        if not (0 <= start_idx < n and 0 <= end_idx < n):
            raise ValueError(f"indices out of range: {start_idx}, {end_idx}")

        path_idx = astar(start_idx, end_idx)
        # fallback to direct if no path found or only trivial
        if not path_idx or path_idx == [start_idx]:
            path_idx = [start_idx, end_idx]

        path_scenes = [scenes[i] for i in path_idx]
        return jsonify(path_scenes)

    except Exception as e:
        app.logger.exception("Error in /api/route")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

'''
FastAPI app for FakeWaze
/route endpoint for route planning
Uses Dijkstra's algorithm to find the shortest path
Command to run the server: fastapi dev app.py
'''
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import networkx as nx
from typing import List
import asyncio
from citymap import load_city_map, create_graph, update_graph

class RouteRequest(BaseModel):
    start: int
    end: int

class RouteResponse(BaseModel):
    paths: List[List[int]]
    distance: float

# Global variables 
edges = load_city_map('citymap.txt')
G0 = create_graph(edges)
G = G0.copy()
returned_paths = []
request_count = 0
updating_lock = asyncio.Lock()

app = FastAPI()

@app.post("/route", response_model=RouteResponse)
def get_route(request: RouteRequest):
    print('request received:', request)
    start = request.start
    end = request.end
    try:
        paths = [p for p in nx.all_shortest_paths(G,source=start, target=end, weight='weight')]
        distance = nx.dijkstra_path_length(G, source=start, target=end)
        
        #store the paths for later use in a global variable
        returned_paths.extend(paths)

        return RouteResponse(paths=paths, distance=distance)
    except nx.NetworkXNoPath:
        raise HTTPException(status_code=404, detail="No path found between the specified nodes")
    except nx.NodeNotFound:
        raise HTTPException(status_code=404, detail="Node does not exist in the graph")

@app.get("/edges")
def get_edges():
    # Return all edges with their weights
    edges_with_weights = [
        {"source": u, "target": v, "weight": data["weight"]}
        for u, v, data in G.edges(data=True)
    ]
    return {"edges": edges_with_weights}


@app.middleware("http")
async def count_requests(request, call_next):
    global request_count, G, G0, returned_paths
    async with updating_lock:
        response = await call_next(request)
        # Only count POST requests to /route
        if request.method == "POST" and request.url.path == "/route":
            request_count += 1
            print(f"Request count: {request_count}")
            if request_count >= 10:
                G = update_graph(G, G0, returned_paths)
                request_count = 0
                returned_paths = []
        return response

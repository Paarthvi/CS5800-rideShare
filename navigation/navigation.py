from position import Position
from itertools import permutations
import osmnx as ox
import networkx as nx
import numpy as np


class Navigator(object):

    def __init__(self, left_top_position: Position, right_bottom_position: Position) -> None:
        self.left_top_position = left_top_position
        self.right_top_position = right_bottom_position
        self.graph = ox.graph_from_bbox(self.left_top_position.latitude, self.right_top_position.latitude,
                                        self.left_top_position.longitude, self.right_top_position.longitude,
                                        network_type='drive')
        self.projected_graph = ox.project_graph(self.graph)
        self.adjacency = nx.to_numpy_array(self.graph, weight='length')
        self.heuristic = np.copy(self.adjacency)
        self.i_to_point = {}
        self.point_to_i = {}
        count = 0
        self.edge_color = ['w'] * len(self.graph.edges())
        for point in self.graph.nodes:
            self.i_to_point[count] = point
            self.point_to_i[point] = count
            count += 1
        self.generate_heuristic()
        self.color = ['k'] * len(self.i_to_point)

    def generate_heuristic(self) -> None:
        length = len(self.heuristic)
        for i in range(length):
            for j in range(length):
                # if self.heuristic[i][j] == np.inf:
                #     continue
                pi = self.graph.nodes[self.i_to_point[i]]
                pj = self.graph.nodes[self.i_to_point[j]]
                point_i = Position(pi['y'], pi['x'])
                point_j = Position(pj['y'], pj['x'])
                self.heuristic[i][j] = point_i.euclid(point_j)

    def get_closest_point(self, location: Position) -> int:
        min_distance = float("inf")
        to_return = -1
        for point in self.graph.nodes:
            temp = Position(self.graph.nodes[point]['y'], self.graph.nodes[point]['x'])
            if location.euclid(temp) < min_distance:
                to_return = point
                min_distance = location.euclid(temp)
        return to_return

    def set_node_color(self, node: int, color: str) -> None:
        self.color[self.point_to_i[node]] = color

    def set_edge_color(self, node1: int, node2: int, color: str) -> None:
        # self.edge_color[self.graph[node1][node2][0]['key']] = color
        if (node1, node2) in self.graph.edges():
            self.edge_color[[node1, node2]] = color

    def plot_graph(self) -> None:
        # ox.plot_graph(self.graph, node_color=self.color, node_size=30, edge_color=self.edge_color)
        ox.plot_graph(self.graph, node_color=self.color, node_size=30)

    def plot_path(self, points) -> None:
        nodes = []
        for i in points:
            nodes.append(self.i_to_point[i])
        mark = []
        for i in range(len(nodes) - 1):
            if nodes[i] == nodes[i+1]:
                mark.append(i)
        mark.reverse()
        for i in mark:
            nodes.pop(i)
        ox.plot_graph_route(self.graph, nodes, 'r', route_linewidth=1, node_size=50,
                            node_color=self.color, route_alpha=0.5)

    def service_order(self, locations: list[Position], source: Position) -> list[Position]:
        min_cost = float("inf")
        ordered_path = None
        adjacency = [[0 for _ in range(len(locations) + 1)] for _ in range(len(locations) + 1)]
        for i in range(len(locations)):
            distance = source.euclid(locations[i])
            adjacency[0][i + 1] = distance
            adjacency[i + 1][0] = distance
        for i in range(len(locations)):
            for j in range(len(locations)):
                distance = locations[i].euclid(locations[j])
                adjacency[j + 1][i + 1] = distance
                adjacency[i + 1][j + 1] = distance
        # pprint(adjacency)
        points = list(range(1, len(locations) + 1))
        all_paths = permutations(points)
        for path in all_paths:
            broken = False
            current_cost = 0
            cur = 0
            for i in path:
                current_cost += adjacency[cur][i]
                if min_cost < current_cost:
                    broken = True
                    break
                cur = i
            if broken:
                continue
            current_cost += adjacency[cur][0]
            if min_cost > current_cost:
                min_cost = current_cost
                ordered_path = path
        path_to_traverse = [source]
        if ordered_path:
            for i in ordered_path:
                path_to_traverse.append(locations[i - 1])
        path_to_traverse.append(source)
        return path_to_traverse

    def generate_route(self, locations: list[Position]) -> list[int]:
        to_return = []
        for i in range(len(locations) - 1):
            point1 = self.point_to_i[self.get_closest_point(locations[i])]
            point2 = self.point_to_i[self.get_closest_point(locations[i + 1])]
            to_return.extend(self.path_between_2_points(point1, point2))
        return to_return

    def path_between_2_points(self, start: int, goal: int) -> list[int]:
        closed_set = set()
        open_set = {start}
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic[start][goal]}
        while open_set:
            current = min(open_set, key=lambda x: f_score[x])
            if current == goal:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return list(reversed(path))
            open_set.remove(current)
            closed_set.add(current)
            for neighbor in range(len(self.adjacency[current])):
                if self.adjacency[current][neighbor] == 0:
                    continue
                tentative_g_score = g_score[current] + self.adjacency[current][neighbor]
                if neighbor in closed_set and tentative_g_score >= g_score.get(neighbor, float('inf')):
                    continue
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic[neighbor][goal]
                    if neighbor not in open_set:
                        open_set.add(neighbor)
        return []



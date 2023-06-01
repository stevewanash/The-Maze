"""_summary_
"""
from collections import deque


class PathFinding:
    """_summary_
    """
    def __init__(self, game):
        """_summary_

        Args:
            game (_type_): _description_
        """
        self.game = game
        self.map = game.map.mini_map
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1],\
            [1, 1], [-1, 1]
        self.graph = {}
        self.get_graph()

    def get_path(self, start, goal):
        """_summary_

        Args:
            start (_type_): _description_
            goal (_type_): _description_

        Returns:
            _type_: _description_
        """
        self.visited = self.bfs(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]

    def bfs(self, start, goal, graph):
        """_summary_

        Args:
            start (_type_): _description_
            goal (_type_): _description_
            graph (_type_): _description_

        Returns:
            _type_: _description_
        """
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break
            next_nodes = graph[cur_node]

            for next_node in next_nodes:
                if next_node not in visited and next_node\
                        not in self.game.object_handler.CHR_positions:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return visited

    def get_next_nodes(self, x, y):
        """_summary_

        Args:
            x (_type_): _description_
            y (_type_): _description_

        Returns:
            _type_: _description_
        """
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy)
                not in self.game.map.world_map]

    def get_graph(self):
        """_summary_
        """
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) +\
                        self.get_next_nodes(x, y)

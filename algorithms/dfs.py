from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        frontier = [initial]          # pilha (LIFO)
        best_depth = {initial.tiles: 0}  # menor profundidade em que cada estado foi visto

        while frontier:
            node = frontier.pop()
            if node.is_goal:
                result.solution = node
                result.depth = node.cost
                return result
            if node.cost >= self.depth_limit:
                continue  # limite de profundidade atingido: não expande

            result.nodes_expanded += 1
            # empilha em ordem reversa para expandir na ordem UP, DOWN, LEFT, RIGHT
            for child in reversed(node.neighbors()):
                result.nodes_generated += 1
                seen = best_depth.get(child.tiles)
                if seen is not None and seen <= child.cost:
                    continue  # já visitado por um caminho igual ou mais curto
                best_depth[child.tiles] = child.cost
                frontier.append(child)
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result

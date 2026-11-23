import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

# posição (linha, coluna) de cada peça no estado objetivo
GOAL_POS = {tile: divmod(i, 3) for i, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan: soma das distâncias de cada peça até sua posição final.
        É admissível (nunca superestima), pois cada movimento desloca uma peça em uma casa."""
        total = 0
        for i, tile in enumerate(state.tiles):
            if tile != 0:
                r, c = divmod(i, 3)
                gr, gc = GOAL_POS[tile]
                total += abs(r - gr) + abs(c - gc)
        return total

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        tie = count()  # desempate estável entre nós com mesmo f e h
        h0 = self.heuristic(initial)
        frontier = [(initial.cost + h0, h0, next(tie), initial)]
        best_g = {initial.tiles: 0}

        while frontier:
            f, h, _, node = heapq.heappop(frontier)
            if node.cost > best_g.get(node.tiles, float("inf")):
                continue  # entrada desatualizada na fila
            if node.is_goal:  # teste de objetivo na expansão (garante otimalidade)
                result.solution = node
                result.depth = node.cost
                return result

            result.nodes_expanded += 1
            for child in node.neighbors():
                result.nodes_generated += 1
                if child.cost < best_g.get(child.tiles, float("inf")):
                    best_g[child.tiles] = child.cost
                    hc = self.heuristic(child)
                    heapq.heappush(frontier, (child.cost + hc, hc, next(tie), child))
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result

// Sergey Voronov, 2015.

#ifndef AHO_CORASICK_BREADWIDTHSERACH_H
#define AHO_CORASICK_BREADWIDTHSERACH_H

#include <queue>
#include <unordered_set>

template<class Visitor, class Graph, class Vertex>
void BreadthFirstSearch(Vertex origin_vertex, const Graph &graph,
                        Visitor visitor) {
  std::queue<Vertex> queue;
  std::unordered_set<Vertex> visited_vertexes;

  visited_vertexes.insert(origin_vertex);

  visitor.DiscoverVertex(origin_vertex);
  queue.push(origin_vertex);

  while (!queue.empty()) {
    Vertex current_vertex = queue.front();
    queue.pop();

    visitor.ExamineVertex(current_vertex);

    for (const auto &edge : graph.OutgoingEdges(current_vertex)) {
      visitor.ExamineEdge(edge);

      Vertex child_vertex = edge.target;

      bool first_appearance = visited_vertexes.insert(child_vertex).second;

      if (first_appearance) {
        visitor.DiscoverVertex(child_vertex);
        queue.push(child_vertex);
      }
    }
  }
}

#endif //AHO_CORASICK_BREADWIDTHSERACH_H

// Sergey Voronov, 2015.

#include <vector>

#include "AutomatonGraph.h"

std::vector<AutomatonGraph::Edge> AutomatonGraph::OutgoingEdges
    (AutomatonNode *vertex) const {
  std::vector<Edge> edges;
  for (auto &item : vertex->trie_transitions) {
    edges.emplace_back(Edge(vertex, &item.second, item.first));
  }

  return edges;
}

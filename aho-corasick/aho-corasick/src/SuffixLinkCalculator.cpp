// Sergey Voronov, 2015.

#include "SuffixLinkCalculator.h"

void SuffixLinkCalculator::ExamineEdge(const AutomatonGraph::Edge &edge) {
  AutomatonNode *parent = edge.source;

  while (parent->suffix_link != nullptr) {
    auto it = parent->suffix_link->trie_transitions.find(edge.character);
    if (it != parent->suffix_link->trie_transitions.end()) {
      edge.target->suffix_link = &it->second;
      break;
    } else {
      parent = parent->suffix_link;
    }
  }

  if (edge.target->suffix_link == nullptr) {
    edge.target->suffix_link = parent;
  }
}
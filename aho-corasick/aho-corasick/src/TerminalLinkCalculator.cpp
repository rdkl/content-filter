// Sergey Voronov, 2015.

#include "TerminalLinkCalculator.h"

void TerminalLinkCalculator::DiscoverVertex(AutomatonNode *node) {
  AutomatonNode *current_node = node->suffix_link;
  if (current_node == nullptr) {
    // Root.
    node->terminal_link = nullptr;
  } else {
    if (current_node->matched_string_ids.size() > 0) {
      node->terminal_link = current_node;
    } else {
      node->terminal_link = current_node->terminal_link;
    }
  }
}
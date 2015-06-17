// Sergey Voronov, 2015.

#include <queue>
#include <iostream>
#include <iomanip>

#include "Automaton.h"


void Automaton::Print() {
  std::queue<AutomatonNode *> q;
  q.push(&root_);

  AutomatonNode *node;
  while (!q.empty()) {
    node = q.front();

    std::cerr << "Id: " << std::setw(2) << node->id_;
    std::cerr << " Sfx: " << std::setw(2);
    if (node->suffix_link == nullptr) {
      std::cerr << " -1 ";
    } else {
      std::cerr << node->suffix_link->id_;
    }
    std::cerr << " Trm: " << std::setw(2);
    if (node->terminal_link == nullptr) {
      std::cerr << " -1 ";
    } else {
      std::cerr << node->terminal_link->id_;
    }
    std::cerr << " edges: ";

    for (auto iter = node->trie_transitions.begin();
         iter != node->trie_transitions.end(); ++iter) {
      std::cerr << iter->second.id_ << "(" << iter->first << ") ";
      q.push(&(iter->second));
    }

    std::cerr << "\n";
    q.pop();
  }
}

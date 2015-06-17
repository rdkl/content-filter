// Sergey Voronov, 2015.

#ifndef AHO_CORASICK_AUTOMATONNODE_H
#define AHO_CORASICK_AUTOMATONNODE_H

#include <vector>
#include <map>

struct AutomatonNode {
  AutomatonNode() :
      suffix_link(nullptr),
      terminal_link(nullptr) {
    id_ = counter++;
  }

  std::vector<size_t> matched_string_ids;
  // Stores tree structure of nodes
  std::map<char, AutomatonNode> trie_transitions;

  // Stores pointers to the elements of trie_transitions
  // std::map<char, AutomatonNode*> automaton_transitions;
  AutomatonNode *suffix_link;
  AutomatonNode *terminal_link;

  // Debug data.
  int id_;
  static int counter;
};


// Returns nullptr if there is no such transition
AutomatonNode *GetTrieTransition(AutomatonNode *node, char character);

// Performs transition in automaton
AutomatonNode *GetNextNode(AutomatonNode *node, AutomatonNode *root,
                           char character);

#endif //AHO_CORASICK_AUTOMATONNODE_H

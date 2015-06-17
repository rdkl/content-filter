// Sergey Voronov, 2015.

#include <map>
#include <vector>

#include "AutomatonNode.h"

int AutomatonNode::counter = 0;

AutomatonNode *GetTrieTransition(AutomatonNode *node, char character) {
  auto key = node->trie_transitions.find(character);
  if (key == node->trie_transitions.end()) {
    return nullptr;
  }
  return &key->second;
}

AutomatonNode *GetNextNode(AutomatonNode *node, AutomatonNode *root,
                           char character) {
  if (node == nullptr) {
    return root;
  }

  auto it = node->trie_transitions.find(character);

  return it == node->trie_transitions.end() ?
         GetNextNode(node->suffix_link, root, character) : &it->second;
}
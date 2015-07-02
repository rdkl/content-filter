// Sergey Voronov, 2015.

#ifndef AHO_CORASICK_AUTOMATON_H
#define AHO_CORASICK_AUTOMATON_H

#include "AutomatonNode.h"
#include "NodeReference.h"

class Automaton {
public:
  Automaton() = default;

  NodeReference Root() {
    return NodeReference(&root_, &root_);
  }

  // Calls on_match(string_id) for every string ending at
  // this node, i.e. collects all string ids reachable by
  // terminal links.
  template<class Callback>
  void GenerateMatches(NodeReference node, Callback on_match) {
    NodeReference terminal_state = node;

    while (terminal_state) {
      for (auto id : terminal_state.matchedStringIds()) {
        on_match(id);
      }

      terminal_state = terminal_state.terminalLink();
    }
  }

  // Simple debug function, that shouldn't fail on tree.
  void Print();

private:
  AutomatonNode root_;

  Automaton(const Automaton &) = delete;

  Automaton &operator=(const Automaton &) = delete;

  friend class AutomatonBuilder;
};


#endif //AHO_CORASICK_AUTOMATON_H

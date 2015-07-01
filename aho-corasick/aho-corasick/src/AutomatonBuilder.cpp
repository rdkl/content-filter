// Sergey Voronov, 2015.

#include <string>
#include <vector>
#include <memory>

#include "AutomatonBuilder.h"
#include "AutomatonGraph.h"
#include "BreadWidthSearch.h"
#include "SuffixLinkCalculator.h"
#include "TerminalLinkCalculator.h"

template<typename T, typename... Args>
std::unique_ptr<T> make_unique(Args &&... args) {
  return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}

std::unique_ptr<Automaton> AutomatonBuilder::Build() {
  auto automaton = make_unique<Automaton>();
  BuildTrie(words_, ids_, automaton.get());
  BuildSuffixLinks(automaton.get());
  BuildTerminalLinks(automaton.get());
  return automaton;
}

void AutomatonBuilder::BuildTrie(const std::vector<std::string> &words,
                      const std::vector<size_t> &ids,
                      Automaton *automaton) {
  for (size_t i = 0; i < words.size(); ++i) {
    AddString(&automaton->root_, ids[i], words[i]);
  }
}

void AutomatonBuilder::Add(const std::string &string, size_t id) {
  words_.push_back(string);
  ids_.push_back(id);
}

void AutomatonBuilder::AddString(AutomatonNode *root, size_t string_id,
                                 const std::string &string) {
  AutomatonNode *current_node = root;

  for (char symbol : string) {
    current_node = &current_node->trie_transitions[symbol];
  }

  current_node->matched_string_ids.push_back(string_id);
}

void AutomatonBuilder::BuildSuffixLinks(Automaton *automaton) {
  BreadthFirstSearch(&automaton->root_, AutomatonGraph(),
                     SuffixLinkCalculator(&automaton->root_));
}

void AutomatonBuilder::BuildTerminalLinks(Automaton *automaton) {
  BreadthFirstSearch(&automaton->root_, AutomatonGraph(),
                     TerminalLinkCalculator(&automaton->root_));
}

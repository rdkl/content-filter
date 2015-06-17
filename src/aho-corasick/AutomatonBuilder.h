//
// Created by rdkl on 17.06.15.
//

#ifndef AHO_CORASICK_AUTOMATONBUILDER_H
#define AHO_CORASICK_AUTOMATONBUILDER_H

#include <memory>

#include "Automaton.h"

class AutomatonBuilder {
public:
  void Add(const std::string &string, size_t id);

  std::unique_ptr<Automaton> Build();

private:
  static void BuildTrie(const std::vector<std::string> &words,
                        const std::vector<size_t> &ids,
                        Automaton *automaton);

  static void AddString(AutomatonNode *root, size_t string_id,
                        const std::string &string);

  static void BuildSuffixLinks(Automaton *automaton);

  static void BuildTerminalLinks(Automaton *automaton);

  std::vector<std::string> words_;
  std::vector<size_t> ids_;
};


#endif //AHO_CORASICK_AUTOMATONBUILDER_H

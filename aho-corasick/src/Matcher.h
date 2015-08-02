// Sergey Voronov, 2015.

#ifndef AHO_CORASICK_MATRCHER_H
#define AHO_CORASICK_MATRCHER_H

#include "AutomatonBuilder.h"


// Wildcard is a character that may be substituted
// for any of all possible characters
class Matcher {
public:
  Matcher() { };

  void Init(const std::vector<std::string> &words);

  // Resets matcher to start scanning new stream
  void Reset();

  // Scans new character and calls on_match() if
  // suffix of scanned characters matches pattern
  void Scan(char character);
  void Print();

  std::vector<size_t> words_occurrences_by_id_;
  // By end position.
  std::vector<std::vector<size_t>> words_occurrences_by_pos_;
private:
  size_t text_pos_;
  std::vector<std::string> words_;
  NodeReference state_;
  std::unique_ptr<Automaton> aho_corasick_automaton_;
};


#endif //AHO_CORASICK_MATRCHER_H

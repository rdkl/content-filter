// Sergey Voronov, 2015.

#include <iostream>
#include <vector>

#include "Matcher.h"

void Matcher::Init(const std::vector<std::string> &words) {
  AutomatonBuilder builder;

  size_t number = 0;
  for (auto word: words) {
    builder.Add(word, number++);
  }

  words_occurrences_by_id_.assign(words.size(), 0);
  words_occurrences_by_pos_.resize(words.size());
  text_pos_ = 0;

  aho_corasick_automaton_ = builder.Build();
  state_ = aho_corasick_automaton_->Root();
  // aho_corasick_automaton_->Print();
}

void Matcher::Print() {
  for (size_t i: words_occurrences_by_id_) {
    std::cerr << i << " ";
  }
  std::cerr << "\n";
}

void Matcher::Scan(char character) {
  text_pos_++;
  state_ = state_.Next(character);

  aho_corasick_automaton_->GenerateMatches(state_,
       [this](int string_id) {
         words_occurrences_by_id_[string_id]++;
         words_occurrences_by_pos_[string_id].push_back(text_pos_);

         // std::cout << string_id << " |" << words_[string_id] << "| found\n";
       });
}

void Matcher::Reset() {
  state_ = aho_corasick_automaton_->Root();
  words_occurrences_by_id_.assign(words_occurrences_by_id_.size(), 0);
}

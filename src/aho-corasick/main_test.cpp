// Sergey Voronov, 2015.

#include <iostream>
#include <vector>
#include <fstream>

#include "Matcher.h"

std::vector<size_t> FindMatches(std::vector<std::string> &words,
                                std::string &text) {
  Matcher matcher;
  matcher.Init(words);
  std::vector<size_t> occurrences;

  for (size_t offset = 0; offset < text.size(); ++offset) {
    matcher.Scan(text[offset]);
  }

  return matcher.words_occurrences_by_id_;
}

void Print(const std::vector<size_t> &sequence, std::vector<std::string>& words
) {
  std::cout << sequence.size() << std::endl;
  for (size_t pos = 0; pos < sequence.size(); ++pos) {
    if (sequence[pos] > 0) {
      std::cout << pos << " " << sequence[pos];
      std::cout << " " << words[pos];
      std::cout << "\n";
    }
  }

  std::cout << std::endl;
}

std::string ReadString(std::istream &input_stream) {
  std::string input_string;
  input_stream >> input_string;
  return input_string;
}

int main() {
  std::vector<std::string> words;
  words.reserve(20000);

  std::string word;
  std::ifstream infile("file.txt");
  while (std::getline(infile, word)) {
    if (word.size() > 4) {
      word.pop_back();
      words.push_back(word);
      // std::cout << word << " " << word.size() << "\n";
    }
  }

  std::string text = ReadString(std::cin);
  Print(FindMatches(words, text), words);
  return 0;
}

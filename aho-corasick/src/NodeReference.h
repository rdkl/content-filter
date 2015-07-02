// Sergey Voronov, 2015.

#ifndef AHO_CORASICK_NODEREFERENCE_H
#define AHO_CORASICK_NODEREFERENCE_H

#include "AutomatonNode.h"

template<class Iterator>
class IteratorRange {
public:
  IteratorRange(Iterator begin, Iterator end) :
      begin_(begin), end_(end) { }

  Iterator begin() const {
    return begin_;
  }

  Iterator end() const {
    return end_;
  }

private:
  Iterator begin_, end_;
};

class NodeReference {
public:
  typedef std::vector<size_t>::const_iterator MatchedStringIterator;
  typedef IteratorRange<MatchedStringIterator> MatchedStringIteratorRange;

  NodeReference() :
      node_(nullptr),
      root_(nullptr) {
  }

  NodeReference(AutomatonNode *node, AutomatonNode *root) :
      node_(node), root_(root) {}

  NodeReference Next(char character) const;
  NodeReference suffixLink() const;
  NodeReference terminalLink() const;
  MatchedStringIteratorRange matchedStringIds() const;

  explicit operator bool() const {
    return node_ != nullptr;
  }

  bool operator==(NodeReference other) const;

private:
  AutomatonNode *node_;
  AutomatonNode *root_;
};

#endif //AHO_CORASICK_NODEREFERENCE_H

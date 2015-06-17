// Sergey Voronov, 2015.

#include "NodeReference.h"

NodeReference NodeReference::Next(char character) const {
  return NodeReference(GetNextNode(node_, root_, character), root_);
}

NodeReference NodeReference::suffixLink() const {
  // node_->suffix_link may be nullptr.
  return NodeReference(node_->suffix_link, root_);
}

NodeReference NodeReference::terminalLink() const {
  if (node_->terminal_link != nullptr) {
    return NodeReference(node_->terminal_link, root_);
  }

  return NodeReference(nullptr, root_);
}

IteratorRange<std::vector<size_t>::const_iterator>
NodeReference::matchedStringIds() const {
  return MatchedStringIteratorRange(node_->matched_string_ids.cbegin(),
                                    node_->matched_string_ids.cend());
};

bool NodeReference::operator==(NodeReference other) const {
  return node_ == other.node_ && root_ == other.root_;
}

// Sergey Voronov, 2015.

#ifndef AHO_CORASICK_SUFFIXLINKCALCULATOR_H
#define AHO_CORASICK_SUFFIXLINKCALCULATOR_H

#include "BfsVisitor.h"
#include "AutomatonGraph.h"
#include "AutomatonNode.h"

class SuffixLinkCalculator :
    public BfsVisitor<AutomatonNode *, AutomatonGraph::Edge> {
public:
  explicit SuffixLinkCalculator(AutomatonNode *root) :
      root_(root) {}

  void ExamineVertex(AutomatonNode *node) {}
  void DiscoverVertex(AutomatonNode *node) {}

  void ExamineEdge(const AutomatonGraph::Edge &edge);

private:
  AutomatonNode *root_;
};

#endif //AHO_CORASICK_SUFFIXLINKCALCULATOR_H

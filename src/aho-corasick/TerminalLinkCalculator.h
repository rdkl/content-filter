// Sergey Voronov, 2015.

#ifndef AHO_CORASICK_TERMINALLINKCALCULATOR_H
#define AHO_CORASICK_TERMINALLINKCALCULATOR_H

#include "BfsVisitor.h"
#include "AutomatonGraph.h"
#include "AutomatonNode.h"

class TerminalLinkCalculator :
    public BfsVisitor<AutomatonNode *, AutomatonGraph::Edge> {
public:
  explicit TerminalLinkCalculator(AutomatonNode *root) :
      root_(root) {}

  void ExamineVertex(AutomatonNode *node) {}
  void ExamineEdge(const AutomatonGraph::Edge &edge) {}

  void DiscoverVertex(AutomatonNode *node);

private:
  AutomatonNode *root_;
};


#endif //AHO_CORASICK_TERMINALLINKCALCULATOR_H

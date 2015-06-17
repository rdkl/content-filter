// Sergey Voronov, 2015.

#ifndef AHO_CORASICK_AUTOMATONGRAPH_H
#define AHO_CORASICK_AUTOMATONGRAPH_H

#include "AutomatonNode.h"

class AutomatonGraph {
public:
  struct Edge {
    Edge(AutomatonNode *source,
         AutomatonNode *target,
         char character) :
        source(source),
        target(target),
        character(character) {
    }

    AutomatonNode *source;
    AutomatonNode *target;
    char character;
  };

  std::vector<Edge> OutgoingEdges(AutomatonNode *vertex) const;
};

#endif //AHO_CORASICK_AUTOMATONGRAPH_H

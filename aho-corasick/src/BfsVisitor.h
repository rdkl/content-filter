// Sergey Voronov, 2015.

#ifndef AHO_CORASICK_BFSVISITOR_H
#define AHO_CORASICK_BFSVISITOR_H

template<class Vertex, class Edge>
class BfsVisitor {
public:
  virtual void DiscoverVertex(Vertex /*vertex*/) {}
  virtual void ExamineEdge(const Edge & /*edge*/) {}
  virtual void ExamineVertex(Vertex /*vertex*/) {}
  virtual ~BfsVisitor() {}
};

#endif //AHO_CORASICK_BFSVISITOR_H

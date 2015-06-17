cmake_minimum_required(VERSION 3.2)
project(aho_corasick)


set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "aho-corasick")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main_test.cpp)
add_executable(aho_corasick ${SOURCE_FILES}
               AutomatonGraph.cpp AutomatonGraph.h
               AutomatonNode.cpp AutomatonNode.h
               BfsVisitor.h
               TerminalLinkCalculator.cpp TerminalLinkCalculator.h
               SuffixLinkCalculator.cpp SuffixLinkCalculator.h
               BreadWidthSearch.h
               Automaton.cpp Automaton.h
               NodeReference.cpp NodeReference.h
               AutomatonBuilder.cpp AutomatonBuilder.h
               Matcher.cpp Matcher.h)
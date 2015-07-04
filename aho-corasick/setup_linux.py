import shutil
from distutils.core import setup, Extension

aho = Extension("AhoCorasick64",
                sources = ["src/Automaton.cpp",
                           "src/AutomatonBuilder.cpp",
                           "src/AutomatonGraph.cpp",
                           "src/AutomatonNode.cpp",
                           "src/main.cpp",
                           "src/Matcher.cpp",
                           "src/NodeReference.cpp",
                           "src/SuffixLinkCalculator.cpp",
                           "src/TerminalLinkCalculator.cpp"],
                extra_compile_args=["-std=c++11"],)

setup (name = "AhoCorasick64",
       version = "1.0",
       description = "Python wrapper for C++ Aho-Corasick implementation",
       ext_modules = [aho],
       author = "Sergey Voronov")
       
shutil.copyfile("build/lib.linux-x86_64-2.7/AhoCorasick64.so", 
                "../src/libs/AhoCorasick64.so")

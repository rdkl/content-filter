import shutil
from distutils.core import setup, Extension

aho = Extension("AhoCorasick",
                    sources = ["../aho-corasick/Automaton.cpp",
                               "../aho-corasick/AutomatonBuilder.cpp",
                               "../aho-corasick/AutomatonGraph.cpp",
                               "../aho-corasick/AutomatonNode.cpp",
                               "../aho-corasick/main.cpp",
                               "../aho-corasick/Matcher.cpp",
                               "../aho-corasick/NodeReference.cpp",
                               "../aho-corasick/SuffixLinkCalculator.cpp",
                               "../aho-corasick/TerminalLinkCalculator.cpp"],
                    extra_compile_args=["-std=c++11"],)

setup (name = "AhoCorasick",
       version = "1.0",
       description = "Python wrapper for C++ Aho-Corasick implementation",
       ext_modules = [aho],)
       
shutil.copyfile("build/lib.linux-x86_64-2.7/AhoCorasick.so", 
                "../libs/AhoCorasick.so")

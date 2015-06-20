// Sergey Voronov, 2015.

#include <iostream>
#include <vector>
#include <fstream>

#include "Python.h"
#include "Matcher.h"

Matcher matcher;
std::vector<std::string> words;

void Print(const std::vector<size_t> &sequence) {
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

void Init(std::string filename) {
  std::ifstream infile(filename);
  words.reserve(20000);

  std::string word;
  while (std::getline(infile, word)) {
    // First line (should be empty) of file contains 4 bytes of info. Also skip
    // empty lines: size = 2.
    if (word.size() > 4) {
      word.pop_back();
      words.push_back(word);
      // std::cout << word << " " << word.size() << "\n";
    }
  }

  matcher.Init(words);
}

std::vector<size_t> FindMatchesInText(std::string &text) {
  for (size_t offset = 0; offset < text.size(); ++offset) {
    matcher.Scan(text[offset]);
  }

  return matcher.words_occurrences_by_id_;
}

static PyObject *Init(PyObject *self, PyObject *args) {
  const char *command;
  if (!PyArg_ParseTuple(args, "s", &command))
    return NULL;

  std::string filename(command);
  Init(filename);

  return Py_None;
}

static PyObject *FindWordsInText(PyObject *self, PyObject *args) {
  const char *command;
  if (!PyArg_ParseTuple(args, "s", &command))
    return NULL;

  std::string text(command);
  
  std::vector<size_t> matches = FindMatchesInText(text);
  Print(matches);
  
  PyObject *d = PyDict_New();
  for (size_t i = 0; i < matches.size(); ++i) {
    if (matches[i] != 0) {
      PyObject* key = Py_BuildValue("i", i);
      PyObject* val = Py_BuildValue("i", matches[i]);
      PyDict_SetItem(d, key, val);
    }
  }
  
  return d;
}

static PyObject *Reset(PyObject *self, PyObject *args) {
  matcher.Reset();
  return Py_None;
}

static PyMethodDef AhoMethods[] = {
    {"Init",  Init, METH_VARARGS, "Initialize mather with file with words."},
    {"FindWordsInText",  FindWordsInText, METH_VARARGS,
        "Find all words from Init file."},
    {"Reset",  Reset, METH_VARARGS,
        "Reset matcher state to beginning."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initAhoCorasick(void)
{
  (void) Py_InitModule("AhoCorasick", AhoMethods);
}


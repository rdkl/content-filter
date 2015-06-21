// Sergey Voronov, 2015.

#include <iostream>
#include <vector>
#include <fstream>

#include "Python.h"
#include "structmember.h"

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

typedef struct {
    PyObject_HEAD
    PyObject *matcher;
} PyMatcher;


static void
PyMatcher_dealloc(PyMatcher* self) {
    delete self->matcher;
}

static PyObject *
PyMatcher_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyMatcher *self;

    self = (PyMatcher *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->matcher = (PyObject*) new Matcher();
    }

    return (PyObject *)self;
}

static PyMemberDef PyMatcher_members[] = {
    {"matcher", T_OBJECT_EX, offsetof(PyMatcher, matcher), 0,
     "AhoCorasick matcher"},
    {NULL}  /* Sentinel */
};

static PyObject *
PyMatcher_Init(PyMatcher* self, PyObject *args)
{
  const char *command;
  if (!PyArg_ParseTuple(args, "s", &command))
    return NULL;

  std::string filename(command);
  
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
  
  ((Matcher*) self->matcher)->Init(words);

  return Py_None;
}

static PyObject *
PyMatcher_FindWordsInText(PyObject *self, PyObject *args) {
  const char *command;
  if (!PyArg_ParseTuple(args, "s", &command))
    return NULL;

  std::string text(command);
  
  Matcher* local_matcher = (Matcher*) ((PyMatcher*) self)->matcher;
  
  for (size_t offset = 0; offset < text.size(); ++offset) {
    local_matcher->Scan(text[offset]);
  }

  std::vector<size_t> matches = local_matcher->words_occurrences_by_id_;
  
  // std::vector<size_t> matches = local_matcher->FindMatchesInText(text);
  Print(matches);
  
  PyObject *dict = PyDict_New();
  for (size_t i = 0; i < matches.size(); ++i) {
    if (matches[i] != 0) {
      PyObject* key = Py_BuildValue("i", i);
      PyObject* val = Py_BuildValue("i", matches[i]);
      PyDict_SetItem(dict, key, val);
    }
  }
  
  return dict;
}

static PyObject *
PyMatcher_Reset(PyObject *self) {
  ((Matcher*) ((PyMatcher*) self)->matcher)->Reset();
  return Py_None;
}

static PyMethodDef PyMatcher_methods[] = {
    {"Init", (PyCFunction)PyMatcher_Init, METH_VARARGS, "Init"},
    {"FindWordsInText", (PyCFunction)PyMatcher_FindWordsInText, METH_VARARGS, 
    "FWIT"},
    {"Reset", (PyCFunction)PyMatcher_Reset, METH_NOARGS, "Reset"},
    {NULL}  /* Sentinel */
};

static PyTypeObject PyMatcherType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "AhoCorasick.Matcher",             /*tp_name*/
    sizeof(PyMatcher),             /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)PyMatcher_dealloc, /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
    "PyMatcher objects",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    PyMatcher_methods,             /* tp_methods */
    PyMatcher_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    0,      /* tp_init */
    0,                         /* tp_alloc */
    PyMatcher_new,                 /* tp_new */
};

PyMODINIT_FUNC initAhoCorasick(void)
{
  // (void) Py_InitModule("AhoCorasick", AhoMethods);
  PyObject* m;

  if (PyType_Ready(&PyMatcherType) < 0)
      return;

  m = Py_InitModule3("AhoCorasick", AhoMethods,
                     "Example module that creates an extension type.");

  if (m == NULL)
    return;

  Py_INCREF(&PyMatcherType);
  PyModule_AddObject(m, "Matcher", (PyObject *)&PyMatcherType);
}

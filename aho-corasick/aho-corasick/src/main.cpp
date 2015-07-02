// Sergey Voronov, 2015.

// Check MSVC environment.
#if _WIN32 || _WIN64
#if _WIN64
#define ENV64_MSVC
#else
#define ENV32_MSVC
#endif
#endif

// Check GCC environment.
#if __GNUC__
#if __x86_64__ || __ppc64__
#define ENV64_GCC
#else
#define ENV32_GCC
#endif
#endif

#include <iostream>
#include <vector>
#include <fstream>
#include <string>

#include "Python.h"
#include "structmember.h"

#include "Matcher.h"

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

static PyMethodDef 
AhoMethods[] = {
        {NULL, NULL, 0, NULL}
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
PyMatcher_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
        PyMatcher *self;

        self = (PyMatcher *)type->tp_alloc(type, 0);
        if (self != NULL) {
                self->matcher = (PyObject*) new Matcher();
        }

        return (PyObject *)self;
}

static PyMemberDef 
PyMatcher_members[] = {
        {"matcher", T_OBJECT_EX, offsetof(PyMatcher, matcher), 0,
         "AhoCorasick matcher class"},
        {NULL}    /* Sentinel */
};

static PyObject * 
PyMatcher_Init(PyMatcher* self, PyObject *args) {
    const char *command;
    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;

    std::string filename(command);
    
    std::ifstream infile(filename);
    words.reserve(20000);

    std::string word;
    while (std::getline(infile, word)) {
        // First line (should be empty) of file contains 4 bytes of info. Also skips
        // empty lines: size = 2.
        if (word.size() > 4) {
            word.pop_back();
            words.push_back(" " + word + "");
        }
    }
    
    ((Matcher*) self->matcher)->Init(words);

    PyObject *dict = PyDict_New();    
    for (size_t i = 0; i < words.size(); ++i) {
        PyObject* key = Py_BuildValue("i", i);
        PyObject* val = Py_BuildValue("s", words[i].c_str());
        PyDict_SetItem(dict, key, val);
    }

    return dict;
}

// Now it resets matcher after every string. 
static PyObject *
PyMatcher_FindWordsInText(PyObject *self, PyObject *args) {
    // Local assigment of matcher.
    Matcher* matcher = (Matcher*) ((PyMatcher*) self)->matcher;
    
    // Get input text from arguments.
    const char *input_string;
    if (!PyArg_ParseTuple(args, "s", &input_string)) {
        return NULL;
    }
    
    std::string text(input_string);

    std::cout << "|" << text << "|\n";
    std::cout << "|" << words[0] << "|\n";
    
    // Find words. All occurences are stored in words_occurrences_by_id_.
    for (size_t offset = 0; offset < text.size(); ++offset) {
        matcher->Scan(text[offset]);
    }
    std::vector<size_t> matches = matcher->words_occurrences_by_id_;
    
    // Prints results as vector (with all zeros) to console.
    // Print(matches);
    
    // Return dict of matches.
    PyObject *dict = PyDict_New();

    for (size_t i = 0; i < matches.size(); ++i) {
        if (matches[i] != 0) {
            PyObject* key = Py_BuildValue("i", i);
            PyObject* val = Py_BuildValue("i", matches[i]);
            PyDict_SetItem(dict, key, val);
        }
    }

    matcher->Reset();    
    return dict;
}


// Uncomment if there will be function like "FindWordsInCurrentLineOfText". 
// static PyObject *
// PyMatcher_Reset(PyObject *self) {
//     ((Matcher*) ((PyMatcher*) self)->matcher)->Reset();
//     return Py_None;
// }


static PyMethodDef PyMatcher_methods[] = {
        {"Init", (PyCFunction)PyMatcher_Init, METH_VARARGS, "Init"},
        {"FindWordsInText", (PyCFunction)PyMatcher_FindWordsInText, METH_VARARGS, 
        "FWIT"},
        // {"Reset", (PyCFunction)PyMatcher_Reset, METH_NOARGS, "Reset"},
        {NULL}    /* Sentinel */
};

// Class definition.
static PyTypeObject PyMatcherType = {
        PyObject_HEAD_INIT(NULL)
        0,                                                 /* ob_size */
        "AhoCorasick.Matcher",                             /* tp_name */
        sizeof(PyMatcher),                                 /* tp_basicsize */
        0,                                                 /* tp_itemsize */
        (destructor)PyMatcher_dealloc,                     /* tp_dealloc */
        0,                                                 /* tp_print */
        0,                                                 /* tp_getattr */
        0,                                                 /* tp_setattr */
        0,                                                 /* tp_compare */
        0,                                                 /* tp_repr */
        0,                                                 /* tp_as_number */
        0,                                                 /* tp_as_sequence */
        0,                                                 /* tp_as_mapping */
        0,                                                 /* tp_hash */
        0,                                                 /* tp_call */
        0,                                                 /* tp_str */
        0,                                                 /* tp_getattro */
        0,                                                 /* tp_setattro */
        0,                                                 /* tp_as_buffer */
        Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,          /* tp_flags */
        "PyMatcher objects",                               /* tp_doc */
        0,                                                 /* tp_traverse */
        0,                                                 /* tp_clear */
        0,                                                 /* tp_richcompare */
        0,                                                 /* tp_weaklistoffset */
        0,                                                 /* tp_iter */
        0,                                                 /* tp_iternext */
        PyMatcher_methods,                                 /* tp_methods */
        PyMatcher_members,                                 /* tp_members */
        0,                                                 /* tp_getset */
        0,                                                 /* tp_base */
        0,                                                 /* tp_dict */
        0,                                                 /* tp_descr_get */
        0,                                                 /* tp_descr_set */
        0,                                                 /* tp_dictoffset */
        0,                                                 /* tp_init */
        0,                                                 /* tp_alloc */
        PyMatcher_new,                                     /* tp_new */
};

#if defined(ENV64_GCC) || defined(ENV64_MSVC) 
PyMODINIT_FUNC initAhoCorasick64(void) {
  const char module_name[] = "AhoCorasick64";
  const char module_description[] = "Provides an Aho-Corasick matcher (64 bit).";
#elif
PyMODINIT_FUNC initAhoCorasick32(void) {
  const char module_name[] = "AhoCorasick32";
  const char module_description[] = "Provides an Aho-Corasick matcher (32 bit).";
#endif

    PyObject* m;
    if (PyType_Ready(&PyMatcherType) < 0)
            return;

    m = Py_InitModule3(module_name, AhoMethods, module_description);

    if (m == NULL)
        return;

    Py_INCREF(&PyMatcherType);
    PyModule_AddObject(m, "Matcher", (PyObject*) &PyMatcherType);
}

#include <Python.h>

// Function to add two numbers
static PyObject* py_add(PyObject* self, PyObject* args) {
    double a, b;
    if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
        return NULL;
    }
    return Py_BuildValue("d", a + b);
}

// Function to subtract two numbers
static PyObject* py_subtract(PyObject* self, PyObject* args) {
    double a, b;
    if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
        return NULL;
    }
    return Py_BuildValue("d", a - b);
}

// Function to multiply two numbers
static PyObject* py_multiply(PyObject* self, PyObject* args) {
    double a, b;
    if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
        return NULL;
    }
    return Py_BuildValue("d", a * b);
}

// Function to divide two numbers
static PyObject* py_divide(PyObject* self, PyObject* args) {
    double a, b;
    if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
        return NULL;
    }
    if (b == 0) {
        PyErr_SetString(PyExc_ZeroDivisionError, "Division by zero");
        return NULL;
    }
    return Py_BuildValue("d", a / b);
}

// Method definitions
static PyMethodDef CalculatorMethods[] = {
    {"add", py_add, METH_VARARGS, "Add two numbers"},
    {"subtract", py_subtract, METH_VARARGS, "Subtract two numbers"},
    {"multiply", py_multiply, METH_VARARGS, "Multiply two numbers"},
    {"divide", py_divide, METH_VARARGS, "Divide two numbers"},
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef calculatormodule = {
    PyModuleDef_HEAD_INIT,
    "calculator",
    NULL,
    -1,
    CalculatorMethods
};

// Module initialization function
PyMODINIT_FUNC PyInit_calculator(void) {
    return PyModule_Create(&calculatormodule);
}


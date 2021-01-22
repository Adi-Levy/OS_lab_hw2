#include <Python.h>
#include "highscore_api.h"


static PyObject *
posix_error(void)
{
  return PyErr_SetFromErrno(PyExc_OSError);
}


static PyObject *
py_highscore_add(PyObject *self, PyObject *args)
{
  const char *board;
  unsigned int score;
  int status;
  
  if (!PyArg_ParseTuple(args, "zi", &board, &score))
    return NULL;
  
  status = highscore_add(board, score);
  
  if (status < 0)
    return posix_error();
  
  return Py_BuildValue("i", status);
}


static PyObject *
py_highscore_list(PyObject *self, PyObject *args)
{
  const char *board;
  ssize_t size;
  unsigned int *buf;
  ssize_t status;
  PyObject *ret;
  int i;

  if (!PyArg_ParseTuple(args, "zi", &board, &size))
    return NULL;
  
  // Hack to let the syscall catch negative size errors instead of us doing it for it.
  if (size >= 0) {
     buf = malloc(size * sizeof(unsigned int));
     if (!buf)
	 return NULL;
  } else {
     buf = malloc(1 * sizeof(unsigned int));
     if (!buf)
	 return NULL;
  }

  status = highscore_list(board, buf, size);
  
  if (status < 0) {
    free(buf);
    return posix_error();
  }
  
  ret = PyTuple_New(status);
  if (!ret) {
      free(buf);
      return NULL;
  }
  
  for (i=0; i < status; i++) {
      PyTuple_SET_ITEM(ret, i, Py_BuildValue("i", buf[i]));
  }
  free(buf);

  return ret;
}


static PyObject *
py_highscore_list_NULL(PyObject *self, PyObject *args)
{
  const char *board;
  size_t size;
  int status;
  PyObject *ret;
  int i;

  if (!PyArg_ParseTuple(args, "zi", &board, &size))
    return NULL;
  
  status = highscore_list(board, NULL, size);
  
  if (status < 0) {
    return posix_error();
  }
  
  ret = PyTuple_New(status);
  if (!ret) {
      return NULL;
  }
  
  for (i=0; i < status; i++) {
      PyTuple_SET_ITEM(ret, i, Py_BuildValue("i", 0));
  }

  return ret;
}


static PyObject * py_highscore_chleague(PyObject *self, PyObject *args)
{
  int pid;
  int status;
  
  if (!PyArg_ParseTuple(args, "i", &pid))
    return NULL;
  
  status = highscore_chleague(pid);
  if (status < 0) {
    return posix_error();
  }
  
  Py_INCREF(Py_None);
  return Py_None;
}


static PyObject * py_highscore_leagues(PyObject *self, PyObject *args)
{
  int status;
  
  status = highscore_leagues();
  if (status < 0) {
    return posix_error();
  }
  
  return Py_BuildValue("i", status);
}


static PyMethodDef msgMethods[] = {
  {"highscore_add",  py_highscore_add, METH_VARARGS,
   "Add a highscore to the given board's table in the current league.\nExample:\nhighscore_add('/some/board', 12) - will add the high score 12 to the board /some/board. Returns the highscore position of the new entry."},
  {"highscore_list",  py_highscore_list, METH_VARARGS,
   "Return the top requested scores for the given board.\nExample:\nhighscore_list('/some/board', 10) - will return the top 10 scores for the board /some/board, or fewer if there are not enough entries."},
  {"highscore_list_NULL",  py_highscore_list_NULL, METH_VARARGS,
   "Return the top requested scores for the given board.\nExample:\nhighscore_list('/some/board', 10) - will return the top 10 scores for the board /some/board, or fewer if there are not enough entries."},
  {"highscore_chleague",  py_highscore_chleague, METH_VARARGS,
   "Change the current process' league, to the league of another process.\nExample:\nhighscore_chprocess(123) - will change the current process' league to 123's league. Returns None."},
  {"highscore_leagues",  py_highscore_leagues, METH_VARARGS,
   "Return the current number of leagues."},
  {NULL, NULL, 0, NULL} 
};


void
initpyHighscore(void)
{
  (void) Py_InitModule("pyHighscore", msgMethods);
}

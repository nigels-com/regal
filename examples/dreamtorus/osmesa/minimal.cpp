/*

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>

*/

// An example of the minimal Win32 OpenGL (via Regal) program.
// It only works in 16 bit color modes or higher (since it doesn't
// create a palette).

#include <windows.h>

#include <GL/Regal.h>

#ifdef _WIN32
#undef GLAPI
#define GLAPI __declspec(dllimport)
#endif

#ifdef _WIN32
#undef GLAPIENTRY
#define GLAPIENTRY __stdcall
#endif

//extern "C" {
#include <GL/osmesa.h>
//}

#include "render.h"

#include <cstdio>
#include <cstdlib>
using namespace std;

int
main(int argc, char *argv[])
{
  OSMesaContext context;
  const GLsizei width = 800;
  const GLsizei height = 600;
  GLubyte buffer[width*height*4];

  context = OSMesaCreateContext(OSMESA_RGBA, NULL );

  if (OSMesaMakeCurrent(context, buffer, GL_UNSIGNED_BYTE, width, height)==GL_FALSE)
  {
    return EXIT_FAILURE;
  }

  RegalMakeCurrent(context);

  dreamTorusReshape(width, height);
  dreamTorusDisplay(true);

  RegalMakeCurrent(NULL);

  OSMesaDestroyContext(context);

  return EXIT_SUCCESS;
}

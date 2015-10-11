#!/usr/bin/python -B

from string import Template, upper, replace

from ApiUtil import outputCode

regalSys = '''#if REGAL_SYS_OSMESA
# ifndef REGAL_SYS_ES1
#  define REGAL_SYS_ES1 0
# endif
# ifndef REGAL_SYS_ES2
#  define REGAL_SYS_ES2 0
# endif
# ifndef REGAL_SYS_GL
#  define REGAL_SYS_GL 1
# endif
#  ifndef REGAL_SYS_WGL
#   define REGAL_SYS_WGL 0
#  endif
#  ifndef REGAL_SYS_GLX
#   define REGAL_SYS_GLX 0
#  endif
#  ifndef REGAL_SYS_EGL
#   define REGAL_SYS_EGL 0
#  endif
# if defined(_WIN32)
#  ifndef REGAL_SYS_WIN32
#   define REGAL_SYS_WIN32 1
#  endif
# endif
# elif defined(_WIN32)
# if defined(PPAPI)
#  ifndef REGAL_SYS_PPAPI
#   define REGAL_SYS_PPAPI 1
#  endif
# else
#  ifndef REGAL_SYS_WGL
#   define REGAL_SYS_WGL 1
#  endif
# endif
# ifndef REGAL_SYS_WIN32
#  define REGAL_SYS_WIN32 1
# endif
#elif defined(__APPLE__)
# include <TargetConditionals.h>
# if defined(TARGET_OS_IPHONE) && TARGET_OS_IPHONE
#  ifndef REGAL_SYS_IOS
#   define REGAL_SYS_IOS 1
#  endif
# else
#  ifndef REGAL_SYS_OSX
#   define REGAL_SYS_OSX 1
#  endif
#  ifndef REGAL_SYS_GLX
#   define REGAL_SYS_GLX 0
#  endif
# endif
#elif defined(__native_client__)
# ifndef REGAL_SYS_PPAPI
#  define REGAL_SYS_PPAPI 1
# endif
#elif defined(__ANDROID__)
# ifndef REGAL_SYS_ANDROID
#  define REGAL_SYS_ANDROID 1
# endif
# ifndef REGAL_SYS_EGL
#  define REGAL_SYS_EGL 1
# endif
# ifndef REGAL_SYS_GLX
#  define REGAL_SYS_GLX 0
# endif
#elif defined(EMSCRIPTEN)
# ifndef REGAL_SYS_EMSCRIPTEN
#  define REGAL_SYS_EMSCRIPTEN 1
# endif
# ifndef REGAL_SYS_EGL
#  define REGAL_SYS_EGL 1
# endif
# ifndef REGAL_SYS_ES2
#  define REGAL_SYS_ES2 1
# endif
# ifndef REGAL_SYS_EMSCRIPTEN_STATIC
#  define REGAL_SYS_EMSCRIPTEN_STATIC 1
# endif
# if REGAL_SYS_EMSCRIPTEN_STATIC
#  ifndef REGAL_NAMESPACE
#   define REGAL_NAMESPACE 1
#  endif
# endif
#elif !defined(REGAL_SYS_PPAPI) || !REGAL_SYS_PPAPI
# ifndef REGAL_SYS_X11
#  define REGAL_SYS_X11 1
# endif
# ifndef REGAL_SYS_GLX
#  define REGAL_SYS_GLX REGAL_SYS_X11
# endif
#endif

#ifndef REGAL_SYS_WGL
# define REGAL_SYS_WGL 0
#endif

#ifndef REGAL_SYS_IOS
# define REGAL_SYS_IOS 0
#endif

#ifndef REGAL_SYS_OSX
# define REGAL_SYS_OSX 0
#endif

#ifndef REGAL_SYS_PPAPI
# define REGAL_SYS_PPAPI 0
#endif

#ifndef REGAL_SYS_ANDROID
# define REGAL_SYS_ANDROID 0
#endif

#ifndef REGAL_SYS_EGL
# define REGAL_SYS_EGL 0
#endif

#ifndef REGAL_SYS_GLX
# define REGAL_SYS_GLX 0
#endif

#ifndef REGAL_SYS_X11
# define REGAL_SYS_X11 0
#endif

#ifndef REGAL_SYS_WIN32
# define REGAL_SYS_WIN32 0
#endif

#ifndef REGAL_SYS_EMSCRIPTEN
#define REGAL_SYS_EMSCRIPTEN 0
#endif

#ifndef REGAL_SYS_EMSCRIPTEN_STATIC
#define REGAL_SYS_EMSCRIPTEN_STATIC 0
#endif

#ifndef REGAL_SYS_ES1
#define REGAL_SYS_ES1 0
#endif

#ifndef REGAL_SYS_ES2
#define REGAL_SYS_ES2 (REGAL_SYS_PPAPI || REGAL_SYS_IOS || REGAL_SYS_ANDROID || REGAL_SYS_EMSCRIPTEN || REGAL_SYS_EGL)
#endif

#ifndef REGAL_SYS_GL
#define REGAL_SYS_GL (REGAL_SYS_WGL || (!REGAL_SYS_PPAPI && !REGAL_SYS_IOS && !REGAL_SYS_ANDROID && !REGAL_SYS_EMSCRIPTEN))
#endif
'''

systemTemplate = Template( '''${AUTOGENERATED}
${LICENSE}

#ifndef __${HEADER_NAME}_H__
#define __${HEADER_NAME}_H__

${REGAL_SYS}

#endif // __${HEADER_NAME}_H__
''')

def generateSystemHeader(apis, args):

  substitute = {}

  substitute['LICENSE']       = args.license
  substitute['AUTOGENERATED'] = args.generated
  substitute['REGAL_SYS']     = regalSys
  substitute['HEADER_NAME']   = "REGAL_SYSTEM"

  outputCode( '%s/RegalSystem.h' % args.srcdir, systemTemplate.substitute(substitute))

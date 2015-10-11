/*
  Copyright (c) 2011-2013 NVIDIA Corporation
  Copyright (c) 2011-2013 Cass Everitt
  Copyright (c) 2012 Scott Nations
  Copyright (c) 2012 Mathias Schott
  Copyright (c) 2012 Nigel Stewart
  All rights reserved.

  Redistribution and use in source and binary forms, with or without modification,
  are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

    Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
  OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
  OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#ifndef __REGAL_THREAD_H__
#define __REGAL_THREAD_H__

#include "RegalUtil.h"

REGAL_GLOBAL_BEGIN

#include "RegalInit.h"

#if !REGAL_SYS_WIN32
#include <pthread.h>
#endif

// Windows TLS API

#if REGAL_SYS_WIN32 && REGAL_WIN_TLS
extern "C" { DWORD __stdcall TlsAlloc    (void);          }
extern "C" { int   __stdcall TlsFree     (DWORD);         }
extern "C" { void* __stdcall TlsGetValue (DWORD);         }
extern "C" { int   __stdcall TlsSetValue (DWORD, void *); }
#endif

// Windows process and thread ID

#if REGAL_SYS_WIN32
extern "C" { DWORD __stdcall GetCurrentProcessId (void);          }
extern "C" { DWORD __stdcall GetCurrentThreadId  (void);          }
#endif

REGAL_GLOBAL_END

REGAL_NAMESPACE_BEGIN

struct RegalContext;
struct DispatchTableGL;
struct DispatchTableGlobal;

namespace Thread
{

//
// Thread::Thread typedef
//

#if REGAL_NO_TLS
typedef int Thread;
#elif REGAL_SYS_WIN32
typedef DWORD Thread;
#else
typedef pthread_t Thread;
#endif

//
// Thread::Self()
//

inline Thread Self()
{
#if REGAL_NO_TLS
  return 1;
#elif REGAL_SYS_WIN32
  return GetCurrentThreadId();
#else
  return pthread_self();
#endif
}

// Three TLS items - the current RegalContext,
// and the dispatch table pointers for plugins
// calling back into Regal.

struct ThreadLocal
{
  inline ThreadLocal()
  : currentContext(NULL),
    nextDispatchTable(NULL),
    nextDispatchTableGlobal(NULL)
  {
  }

  RegalContext        *currentContext;
  DispatchTableGL     *nextDispatchTable;
  DispatchTableGlobal *nextDispatchTableGlobal;

  // Platform-specifics for thread-local storage

  #if REGAL_NO_TLS
  static ThreadLocal _instance;
  #else
    #if REGAL_SYS_WIN32
      #if REGAL_WIN_TLS
        static DWORD _instanceIndex;
      #else
        static __declspec(thread) ThreadLocal _instance;
      #endif
    #else
      static pthread_key_t _instanceKey;
    #endif
  #endif

  // Cross-platform thread local storage lookup

  static inline ThreadLocal &instance()
  {
    #if REGAL_NO_TLS
      return _instance;
    #elif REGAL_SYS_WIN32
      #if REGAL_WIN_TLS
        ThreadLocal *i = static_cast<ThreadLocal *>(TlsGetValue(_instanceIndex));
        if (!i)
        {
          i = new ThreadLocal();
          TlsSetValue(_instanceIndex,i);
        }
        RegalAssert(i);
        return *i;
      #else
        return _instance;
      #endif
    #else
      ThreadLocal *i = static_cast<ThreadLocal *>(pthread_getspecific(_instanceKey));
      if (!i)
      {
        i = new ThreadLocal();
        pthread_setspecific(_instanceKey,i);
      }
      RegalAssert(i);
      return *i;
    #endif
  }
};


//
// Thread::CurrentContext()
//

inline RegalContext *CurrentContext()
{
  ThreadLocal &instance = ThreadLocal::instance();
  return instance.currentContext;
}

//
// Thread::procID()
// - current process ID
//

inline std::size_t procId()
{
#if REGAL_SYS_WIN32
  return static_cast<std::size_t>(GetCurrentProcessId());
#elif REGAL_SYS_OSX || REGAL_SYS_OSX || REGAL_SYS_IOS || REGAL_SYS_ANDROID || REGAL_SYS_GLX
  return (std::size_t) getpid();
#else
  return 0;
#endif
}

//
// Thread::threadId()
// - current thread ID
//

inline std::size_t threadId()
{
#if REGAL_SYS_WIN32
  return static_cast<std::size_t>(GetCurrentThreadId());
#elif REGAL_SYS_OSX || REGAL_SYS_OSX || REGAL_SYS_IOS || REGAL_SYS_ANDROID || REGAL_SYS_GLX

  // Revisit - pthread_self returns an opaque handle which isn't truely
  // a thread identifier.

  return (std::size_t) pthread_self();
#else
  return 0;
#endif
}

}

#define REGAL_GET_CONTEXT() (::REGAL_NAMESPACE_INTERNAL::Thread::CurrentContext())

REGAL_NAMESPACE_END

#endif // __REGAL_THREAD_H__

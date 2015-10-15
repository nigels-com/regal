/*
 Copyright (c) 2013 NVIDIA Corporation
 Copyright (c) 2013 Cass Everitt
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

#ifndef __REGAL_DISPATCH_HTTP_H__
#define __REGAL_DISPATCH_HTTP_H__

#include "RegalUtil.h"

#if REGAL_HTTP

REGAL_GLOBAL_BEGIN

#include <set>
#include <map>
#include <vector>
#include <deque>
#include <string>

#include "pcre.h"

#include "RegalMutex.h"

REGAL_GLOBAL_END

REGAL_NAMESPACE_BEGIN

struct HttpTextureInfo {
  HttpTextureInfo() : name(0), levelMask(0), target(0) {}
  GLuint name;
  GLuint levelMask;
  GLenum target;
};

struct HttpFboInfo {
  HttpFboInfo( GLuint n = 0 ) : name( n ), width(0), height(0) {}
  GLuint name;
  GLint width;
  GLint height;
};

struct Breakpoint {

  Breakpoint()
  : enabled(true)
  , count(0)
  , stopAfterCount(0)
  , re(NULL)
  {}

  ~Breakpoint() {
    if( re ) {
      pcre_free( re );
    }
  }

  void SetRegularExpression( const std::string & newRe )
  {
    UNUSED_PARAMETER(newRe);
    if( re ) {
      pcre_free( re );
    }
    const char *errStr = NULL;
    int offset;
    re = pcre_compile( reString.c_str(), 0, &errStr, &offset, NULL );
    if( re == NULL ) {
      Error( "Could not compile breakpoint regular expression '", reString, "' - ", offset, " - ", errStr );
    }
  }

  bool enabled;
  int count;
  int stopAfterCount;
  std::string reString;
  pcre *re;
};

enum HttpRunState {
  RS_Invalid,
  RS_Run,
  RS_Pause,
  RS_Next,
  RS_NextDraw,
  RS_NextFbo,
  RS_NextFrame,
  RS_NextGroup,
  RS_StepOverGroup,
  RS_StepOutOfGroup,
};

struct DispatchTableGL;

struct DispatchHttpState
{
public:
  DispatchHttpState();
  ~DispatchHttpState();
  void Init( RegalContext * ctx );

  std::map<GLuint, HttpFboInfo> fbo;
  std::set<GLuint> vao;

  // these are share group things, so should only be tracked in the "resource containing" context of the group
  std::set<GLuint> buffer;
  std::set<GLuint> program;
  std::set<GLuint> shader;
  std::map<GLuint, HttpTextureInfo> texture;
  std::vector< Breakpoint * > breakpoint;
  int currentBreakpoint;                         // -1 while not at breaktpoint

  void YieldToHttpServer( RegalContext * ctx, bool log = true );  // called by rendering thread

  void AcquireAppContext( RegalContext * ctx );      // called by http server
  void ReleaseAppContext( RegalContext * ctx );      // called by http server
  void ContinueFromBreakpoint( RegalContext * ctx, HttpRunState rs ); // called by http server

  Thread::Mutex *contextMutex;
  Thread::Mutex *breakpointMutex;
  bool httpServerWantsContext;
  HttpRunState runState;
  int debugGroupStackDepth;
  int stepOverGroupDepth;
  int inBeginEnd;
  std::string callString;
  std::deque<std::string> callLog;

  struct EventCount {
    EventCount() {
      memset( this, 0, sizeof( *this ));
    }
    GLuint64 call;
    GLuint64 draw;
    GLuint64 group;
    GLuint64 fbo;
    GLuint64 frame;
    GLuint64 lastDraw;  // call number of last draw
    GLuint64 lastGroup; // call number of last group
    GLuint64 lastFbo;   // call number of last fbo
    GLuint64 lastFrame; // call number of last frame
  };

  EventCount count;


  struct GlProcs {
    GlProcs() {
      memset( this, 0, sizeof( *this ) );
    }

    void Initialize( DispatchTableGL * tbl );

    PFNGLFINISHPROC Finish;
    PFNGLGETACTIVEUNIFORMPROC GetActiveUniform;
    PFNGLGETATTACHEDSHADERSPROC GetAttachedShaders;
    PFNGLGETINTEGERVPROC GetIntegerv;
    PFNGLGETPROGRAMINFOLOGPROC GetProgramInfoLog;
    PFNGLGETPROGRAMIVPROC GetProgramiv;
    PFNGLGETSHADERINFOLOGPROC GetShaderInfoLog;
    PFNGLGETSHADERSOURCEPROC GetShaderSource;
    PFNGLGETSHADERIVPROC GetShaderiv;
    PFNGLGETTEXTUREIMAGEEXTPROC GetTextureImage;
    PFNGLGETTEXTURELEVELPARAMETERFVEXTPROC GetTextureLevelParameter;
    PFNGLGETTEXTUREPARAMETERFVEXTPROC GetTextureParameter;
    PFNGLGETUNIFORMLOCATIONPROC GetUniformLocation;
    PFNGLREADPIXELSPROC ReadPixels;
  };

  GlProcs gl;

};

REGAL_NAMESPACE_END

#endif

#endif // __REGAL_DISPATCH_HTTP_H__

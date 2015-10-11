#!/usr/bin/python -B

from string import Template, upper, replace

from ApiCodeGen   import *
from ApiUtil      import outputCode
from ApiUtil      import typeIsVoid
from ApiUtil      import typeIsVoidPointer
from ApiRegal     import logFunction

from Dispatch     import dispatchGenCode

from RegalContextInfo import cond

from RegalDispatchShared import apiDispatchFuncInitCode
from RegalDispatchShared import apiDispatchGlobalFuncInitCode

formulae = {
  'bindtexture' : {
    'entries' : [ 'glBindTexture(EXT|)' ],
    'pre' : [
      'if( ${arg1} != 0 ) {',
      '  HttpTextureInfo & hti = _context->http.texture[ ${arg1} ];',
      '  RegalAssert( hti.name == 0 || hti.name == ${arg1} );',
      '  if( hti.name == 0 ) {',
      '    hti.name = ${arg1};',
      '    hti.target = ${arg0};',
      '  }',
      '}',
    ],
  },
  'bindmultitexture' : {
    'entries' : [ 'glBindMultiTextureEXT' ],
    'pre' : [
      'if( ${arg2} != 0 ) {',
      '  HttpTextureInfo & hti = _context->http.texture[ ${arg2} ];',
      '  RegalAssert( hti.name == 0 || hti.name == ${arg2} );',
      '  if( hti.name == 0 ) {',
      '    hti.name = ${arg2};',
      '    hti.target = ${arg1};',
      '  }',
      '}',
    ],
  },
  'bindtextures' : {
    'entries' : [ 'glBindTextures' ],
    'pre' : [
      'if( ${arg2} != NULL ) {',
      '  for( int i = 0; i < ${arg1}; i++ ) {',
      '    if( ${arg2}[i] != 0 ) {',
      '      HttpTextureInfo & hti = _context->http.texture[ ${arg2}[i] ];',
      '      RegalAssert( hti.name == 0 || hti.name == ${arg2}[i] );',
      '      if( hti.name == 0 ) {',
      '        hti.name = ${arg2}[i];',
      '        hti.target = ${arg0};',
      '      }',
      '    }',
      '  }',
      '}',
    ],
  },

  'deletetextures' : {
    'entries' : [ 'glDeleteTextures(EXT|)' ],
    'pre' : [
      'for( int i = 0; i < ${arg0}; i++ ) {',
      '  _context->http.texture.erase( ${arg1}[i] );',
      '}',
    ],
  },

  'createshader' : {
    'entries' : [ 'glCreateShader(ObjectARB|)' ],
    'post' : [
      '_context->http.shader.insert( ret );',
    ],
  },

  'deleteshader' : {
    'entries' : [ 'glDeleteShader(ObjectARB|)' ],
    'post' : [
      '_context->http.shader.erase( ${arg0} );',
    ],
  },

  'createprogram' : {
    'entries' : [ 'glCreateProgram(ObjectARB|)' ],
    'post' : [
      '_context->http.program.insert( ret );',
    ],
  },

  'deleteprogram' : {
    'entries' : [ 'glDeleteProgram(ObjectARB|)' ],
    'post' : [
      '_context->http.program.erase( ${arg0} );',
    ],
  },


  'bindfbo' : {
    'entries' : [ 'glBindFramebuffer(ARB|)' ],
    'pre' : [
      '_context->http.fbo[ ${arg1} ] = HttpFboInfo( ${arg1} );',
      '_context->http.count.fbo++;',
      'if( _context->http.runState == RS_NextFbo ) {',
      '  _context->http.runState = RS_Pause;',
      '}',
    ],
    'post' : [
      '_context->http.count.lastFbo = _context->http.count.call;',
    ],
  },

  'deletefbos' : {
    'entries' : [ 'glDeleteFramebufferss(EXT|)' ],
    'pre' : [
      'for( int i = 0; i < ${arg0}; i++ ) {',
      '  _context->http.fbo.erase( ${arg1}[i] );',
      '}',
    ],
  },

  'pushdebuggroup' : {
    'entries' : [ 'glPushDebugGroup', 'glPushGroupMarkerEXT' ],
    'pre' : [
      '_context->http.count.group++;',
      'if( _context->http.runState == RS_NextGroup ) {',
      '  _context->http.runState = RS_Pause;',
      '}',
      '_context->http.debugGroupStackDepth++;',
    ],
    'post' : [
      '_context->http.count.lastGroup = _context->http.count.call;',
    ],
  },

  'popdebuggroup' : {
    'entries' : [ 'glPopDebugGroup', 'glPopGroupMarkerEXT' ],
    'post' : [
      'DispatchHttpState &h = _context->http;',
      'if( h.runState == RS_StepOutOfGroup || h.runState == RS_NextGroup ) {',
      '  h.runState = RS_Pause;',
      '}',
      'if( h.runState == RS_StepOverGroup && h.debugGroupStackDepth == h.stepOverGroupDepth ) {',
      '  h.runState = RS_Pause;',
      '}',
      'h.debugGroupStackDepth--;',
    ],
  },

  'draw' : {
    'entries' : [ 'gl(Multi|)Draw(Arrays|Elements).*', ],
    'pre' : [
      '_context->http.count.draw++;',
      'if( _context->http.runState == RS_NextDraw ) {',
      '  _context->http.runState = RS_Pause;',
      '}',
    ],
    'post' : [
      '_context->http.count.lastDraw = _context->http.count.call;',
    ],
  },

  'begin' : {
    'entries' : [ 'glBegin' ],
    'pre' : [
      '_context->http.count.draw++;',
      '_context->http.inBeginEnd++;',
      'if( _context->http.runState == RS_NextDraw ) {',
      '  _context->http.runState = RS_Pause;',
      '}',
    ],
    'post' : [
      '_context->http.count.lastDraw = _context->http.count.call;',
    ],
  },

  'end' : {
    'entries' : [ 'glEnd' ],
    'post' : [
      '_context->http.inBeginEnd--;',
      '_context->http.YieldToHttpServer( _context, false /*second call, don\'t update log */ );',
    ],
  },

  'swap' : {
    'entries' : [ '(glX|wgl|egl)SwapBuffers', 'CGLFlushDrawable' ],
    'pre' : [
      '_context->http.count.frame++;',
      'switch( _context->http.runState ) {',
      '   case RS_Run:',
      '     break;',
      '   default:',
      '    _context->http.runState = RS_Pause;',
      '}',
    ],
    'post' : [
      '_context->http.count.lastFrame = _context->http.count.call;',
    ],
  },

}

# CodeGen for dispatch table init.

dispatchHttpTemplate = Template('''${AUTOGENERATED}
${LICENSE}

#include "pch.h" /* For MS precompiled header support */

#include "RegalUtil.h"

#if REGAL_HTTP

REGAL_GLOBAL_BEGIN

#include "RegalLog.h"
#include "RegalHttp.h"
#include "RegalPush.h"
#include "RegalToken.h"
#include "RegalHelper.h"
#include "RegalContext.h"
#include "RegalDispatch.h"
#include "RegalDispatcherGL.h"
#include "RegalDispatcherGlobal.h"

using namespace ::REGAL_NAMESPACE_INTERNAL::Logging;
using namespace ::REGAL_NAMESPACE_INTERNAL::Token;

REGAL_GLOBAL_END

REGAL_NAMESPACE_BEGIN

${API_FUNC_DEFINE}

void InitDispatchTableHttp(DispatchTableGL &tbl)
{
${API_GL_DISPATCH_INIT}
}

${API_GLOBAL_DISPATCH_INIT}

REGAL_NAMESPACE_END

#endif
''')


def generateDispatchHttp(apis, args):

  # CodeGen for API functions.

  code = ''
  categoryPrev = None

  for api in apis:

    code += '\n'
    if api.name in cond:
      code += '#if %s\n' % cond[api.name]

    for function in api.functions:

      if getattr(function,'regalOnly',False)==True:
        continue

      name   = function.name
      params = paramsDefaultCode(function.parameters, True)
      callParams = paramsNameCode(function.parameters)
      rType  = typeCode(function.ret.type)
      rTypes    = rType.strip()
      category  = getattr(function, 'category', None)
      version   = getattr(function, 'version', None)

      if category:
        category = category.replace('_DEPRECATED', '')
      elif version:
        category = version.replace('.', '_')
        category = 'GL_VERSION_' + category

      # Close prev category block.
      if categoryPrev and not (category == categoryPrev):
        code += '\n'

      # Begin new category block.
      if category and not (category == categoryPrev):
        code += '// %s\n\n' % category

      categoryPrev = category

      code += 'static %sREGAL_CALL %s%s(%s) \n{\n' % (rType, 'http_', name, params)

      generated = dispatchGenCode( function, formulae )

      retInit = ''
      if not typeIsVoid(rType):
        if rTypes in api.defaults:
          retInit += '%s' % ( api.defaults[rTypes] )
        else:
          if rType[-1]=='*' or typeIsVoidPointer(rType):
            retInit += 'NULL'
          else:
            retInit += '(%s) 0' % ( rTypes )

      if not typeIsVoid(rType):
        code += '    %s ret = %s;\n' % (rType, retInit)
      code += '    RegalContext *_context = REGAL_GET_CONTEXT();\n'
      if function.needsContext:
        code += '    RegalAssert( _context );\n'

      code += '    if( _context ) {\n'
      if generated and 'pre' in generated:
        for i in generated['pre']:
          code += '      %s\n' % i

      code += '      if( _context->http.runState == RS_Next ) {\n'
      code += '        _context->http.runState = RS_Pause;\n'
      code += '      }\n'
      code += '      _context->http.YieldToHttpServer( _context );\n'

      code += '    }\n'

      if function.needsContext:
        code += '    DispatchTableGL *_next = _context ? _context->dispatcher.http.next() : NULL;\n'
      else:
        code += '    DispatchTableGlobal *_next = dispatcherGlobal.http.next();\n'

      code += '    RegalAssert(_next);\n'

      code += '    '

      if not typeIsVoid(rType):
        code += 'ret = '
      code += '_next->call(&_next->%s)(%s);\n' % ( name, callParams )

      if generated and 'post' in generated:
        code += '    if( _context ) {\n'
        for i in generated['post']:
          code += '      %s\n' % i
        code += '    }\n'

      if not typeIsVoid(rType):
        code += '    return ret;\n'
      code += '}\n\n'

    if api.name in cond:
      code += '#endif // %s\n' % cond[api.name]
    code += '\n'

  # Close pending if block.
  if categoryPrev:
    code += '\n'

  # Output

  substitute = {}
  substitute['LICENSE']         = args.license
  substitute['AUTOGENERATED']   = args.generated
  substitute['COPYRIGHT']       = args.copyright
  substitute['API_FUNC_DEFINE'] = code
  substitute['API_GL_DISPATCH_INIT']     = apiDispatchFuncInitCode( apis, args, 'http' )
  substitute['API_GLOBAL_DISPATCH_INIT'] = apiDispatchGlobalFuncInitCode( apis, args, 'http' )

  outputCode( '%s/RegalDispatchHttp.cpp' % args.srcdir, dispatchHttpTemplate.substitute(substitute))

#!/usr/bin/python -B

from string import Template, upper, replace

from ApiUtil import outputCode
from ApiUtil import typeIsVoid

from ApiCodeGen import *

from RegalContextInfo import cond

from RegalDispatchShared import apiDispatchFuncInitCode, apiDispatchGlobalFuncInitCode

############################################################################

loaderSourceTemplate = Template('''${AUTOGENERATED}
${LICENSE}

#include "pch.h" /* For MS precompiled header support */

#include "RegalUtil.h"

${IFDEF}REGAL_GLOBAL_BEGIN

#include <string>
using namespace std;

#include "RegalLog.h"
#include "RegalBreak.h"
#include "RegalPush.h"
#include "RegalToken.h"
#include "RegalHelper.h"
#include "RegalPrivate.h"
#include "RegalContext.h"
#include "RegalDispatcherGL.h"
#include "RegalDispatcherGlobal.h"
${LOCAL_INCLUDE}

REGAL_GLOBAL_END

REGAL_NAMESPACE_BEGIN

using namespace ::REGAL_NAMESPACE_INTERNAL::Logging;
using namespace ::REGAL_NAMESPACE_INTERNAL::Token;

namespace Loader
{

${LOCAL_CODE}

  static DispatchTableGL &_getDispatchGL()
  {
    RegalContext * _context = REGAL_GET_CONTEXT();
    RegalAssert(_context);
    return _context->dispatcher.driver;
  }
  
  static void _getProcAddress(void (**func)(), void (*funcRegal)(), const char *name)
  {
    GetProcAddress(*func, name);
    RegalAssert(*func!=funcRegal);
    if (*func==funcRegal)
      *func = NULL;
  }

${API_DISPATCH_FUNC_DEFINE}

  void Init(DispatchTableGL &tbl)
  {
${API_DISPATCH_FUNC_INIT}
  }

${API_DISPATCH_GLOBAL_FUNC_INIT}

} // namespace Loader

REGAL_NAMESPACE_END

${ENDIF}''')

##############################################################################################

# CodeGen for API loader function definition.

def apiLoaderFuncDefineCode(apis, args):
  categoryPrev = None
  code = ''

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

      code += '  static %sREGAL_CALL %s(%s) \n  {\n' % (rType, name, params)

      # Get a reference to the appropriate dispatch table and attempt GetProcAddress

      if function.needsContext:
        code += '    DispatchTableGL &_driver = _getDispatchGL();\n'
      else:
        code += '    DispatchTableGlobal &_driver = dispatcherGlobal.driver;\n'

      code += '    _getProcAddress(reinterpret_cast<void (**)()>(&_driver.%s),reinterpret_cast<void (*)()>(%s),"%s");\n'%(name,name,name)
      code += '    '
      if not typeIsVoid(rType):
        code += 'return '
      code += '_driver.call(&_driver.%s)(%s);\n'%(name, callParams)
      code += '  }\n\n'

    if api.name in cond:
      code += '#endif // %s\n' % cond[api.name]
    code += '\n'

  # Close pending if block.
  if categoryPrev:
    code += '\n'

  return code

def generateLoaderSource(apis, args):

  funcDefine = apiLoaderFuncDefineCode( apis, args )
  funcInit   = apiDispatchFuncInitCode( apis, args, None )
  globalFuncInit   = apiDispatchGlobalFuncInitCode( apis, args, None )

  # Output

  substitute = {}

  substitute['LICENSE']         = args.license
  substitute['AUTOGENERATED']   = args.generated
  substitute['COPYRIGHT']       = args.copyright
  substitute['DISPATCH_NAME']   = 'Loader'
  substitute['LOCAL_CODE']      = ''
  substitute['LOCAL_INCLUDE']   = ''
  substitute['API_DISPATCH_FUNC_DEFINE'] = funcDefine
  substitute['API_DISPATCH_FUNC_INIT'] = funcInit
  substitute['API_DISPATCH_GLOBAL_FUNC_INIT'] = globalFuncInit
  substitute['IFDEF'] = '#if REGAL_DRIVER && REGAL_LOADER\n\n'
  substitute['ENDIF'] = '#endif\n'

  outputCode( '%s/RegalDispatchLoader.cpp' % args.srcdir, loaderSourceTemplate.substitute(substitute))

# apitrace.inc
#
# Generic gnumake .inc for building apitrace support into Regal
#

# apitrace sources

APITRACE.CXX += src/apitrace/common/os_posix.cpp
APITRACE.CXX += src/apitrace/common/trace_callset.cpp
APITRACE.CXX += src/apitrace/common/trace_dump.cpp
APITRACE.CXX += src/apitrace/common/trace_file_read.cpp
APITRACE.CXX += src/apitrace/common/trace_file_snappy.cpp
APITRACE.CXX += src/apitrace/common/trace_file_write.cpp
APITRACE.CXX += src/apitrace/common/trace_file_zlib.cpp
APITRACE.CXX += src/apitrace/common/trace_file.cpp
APITRACE.CXX += src/apitrace/common/trace_loader.cpp
APITRACE.CXX += src/apitrace/common/trace_model.cpp
APITRACE.CXX += src/apitrace/common/trace_option.cpp
APITRACE.CXX += src/apitrace/common/trace_parser_flags.cpp
APITRACE.CXX += src/apitrace/common/trace_parser.cpp
APITRACE.CXX += src/apitrace/common/trace_profiler.cpp
APITRACE.CXX += src/apitrace/common/trace_writer_local.cpp
APITRACE.CXX += src/apitrace/common/trace_writer_model.cpp
APITRACE.CXX += src/apitrace/common/trace_writer.cpp
APITRACE.CXX += src/apitrace/dispatch/glproc_egl.cpp
APITRACE.CXX += src/apitrace/dispatch/glproc_gl.cpp
APITRACE.CXX += src/apitrace/gen/wrappers/regaltrace.cpp
APITRACE.CXX += src/apitrace/helpers/eglsize.cpp
APITRACE.CXX += src/apitrace/wrappers/glcaps.cpp
APITRACE.CXX += src/apitrace/wrappers/gltrace_state.cpp
APITRACE.CXX += src/apitrace/wrappers/trace.cpp

# APITRACE.CXX += src/apitrace/thirdparty/snappy/snappy-c.cc
# APITRACE.CXX += src/apitrace/thirdparty/snappy/snappy-sinksource.cpp
# APITRACE.CXX += src/apitrace/thirdparty/snappy/snappy.cc

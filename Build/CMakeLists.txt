

cmake_minimum_required (VERSION 2.6)
project (LUI)



# Configure this variables to match your system
# No trailing slash
if (WIN32)
  
  # Default settings for windows. Usually you only have to adjust WIN_PANDA_PATH
  set (WIN_PANDA_PATH "F:/P3D/1.9.0-1")

  # These vars are based on the WIN_PANDA_PATH and usually are correct
  set(PANDA_SRC "${WIN_PANDA_PATH}/")
  set(PANDA_BIN "${WIN_PANDA_PATH}/built_x64/bin")
  set(PANDA_LIBS "${WIN_PANDA_PATH}/built_x64/lib")
  set(PANDA_INCLUDE "${WIN_PANDA_PATH}/built_x64/include")
  set(PYTHON_LIBS "${WIN_PANDA_PATH}/built_x64/python/libs")
  set(PYTHON_INCLUDE "${WIN_PANDA_PATH}/built_x64/python/include")
  set(PYTHON_BIN "${WIN_PANDA_PATH}/built_x64/python")
  set(PANDA_THIRDPARTY "${WIN_PANDA_PATH}/thirdparty/win-libs-vc10-x64")

else()

  message( FATAL_ERROR "Linux not supported yet" )

endif()


# Check if all supplied directories exist
set(CHECK_DIRS ${PANDA_SRC} ${PANDA_BIN} ${PANDA_LIBS} ${PANDA_INCLUDE} ${PYTHON_LIBS} ${PYTHON_INCLUDE} ${PYTHON_BIN} ${PANDA_THIRDPARTY})
foreach(DIRECTORY ${CHECK_DIRS})
  # message("Checking directory '${DIRECTORY}'")
  if(NOT (EXISTS "${DIRECTORY}" AND IS_DIRECTORY "${DIRECTORY}"))
      message(FATAL_ERROR "The supplied directory '${DIRECTORY}' does not exist! Correct the path in CMakeLists.txt!")
  endif()
endforeach()

# Link panda includes / libraries
include_directories("${PANDA_INCLUDE}")
link_directories("${PANDA_LIBS}")

# Also link python includes / libraries
include_directories("${PYTHON_INCLUDE}")
link_directories("${PYTHON_LIBS}")

# Run interrogate over the files
message("Running interrogate ..")

execute_process(
    COMMAND "${PYTHON_BIN}/python" "interrogate.py" "${PANDA_BIN}" "${PANDA_LIBS}" "${PANDA_INCLUDE}"
    OUTPUT_VARIABLE output
    ERROR_VARIABLE errors
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})

message("Interrogate output: ${output} ${errors}")

# Collect sources for compiling
file(GLOB SOURCES_H Source/*.h)
file(GLOB SOURCES_I Source/*.I)
file(GLOB SOURCES Source/*.cxx)

set(SOURCES ${SOURCES_H} ${SOURCES_I} ${SOURCES})

# Link python library
IF (WIN32)
    set(LIBRARIES "python27.dll")
ELSE()
    set(LIBRARIES "libpython2.7.so")
ENDIF()

# Link panda libraries
# set(LIBRARIES ${LIBRARIES} "libpandabullet.lib")
set(LIBRARIES ${LIBRARIES} "libp3framework.lib")
set(LIBRARIES ${LIBRARIES} "libpanda.lib")
set(LIBRARIES ${LIBRARIES} "libpandaexpress.lib")
set(LIBRARIES ${LIBRARIES} "libp3dtool.lib")
set(LIBRARIES ${LIBRARIES} "libp3dtoolconfig.lib")
set(LIBRARIES ${LIBRARIES} "libp3direct.lib")


# cl /favor:blend /wd4996 /wd4275 /wd4267 /wd4101 /wd4273 /Fobuilt_x64_buffered/tm
# p/p3lui_composite1.obj /nologo /c /Ipanda/src/lui /Ibuilt_x64_buffered/tmp /Ibui
# lt_x64_buffered/include /Ithirdparty/win-python-x64/include /Ithirdparty/win-lib
# s-vc10-x64/lui/include /Ithirdparty/win-libs-vc10-x64/extras/include /MD /Zi /O2
#  /Ob2 /Oi /Ot /fp:fast /DFORCE_INLINING /Fdbuilt_x64_buffered/tmp/p3lui_composit
# e1.pdb /DBUILDING_PANDASKEL /bigobj /EHa /Zm300 /DWIN32_VC /DWIN32 /DWIN64_VC /D
# WIN64 /W3 panda/src/lui/p3lui_composite1.cxx

# Optimizations
IF(MSVC)
   # ADD_DEFINITIONS("/Ot")
   # ADD_DEFINITIONS("/O2")
   # ADD_DEFINITIONS("/Oi")
   # ADD_DEFINITIONS("/MD")
   # ADD_DEFINITIONS("/Zi")
   # ADD_DEFINITIONS("/Ob2")
   # ADD_DEFINITIONS("/fp:fast")
   # ADD_DEFINITIONS("/DFORCE_INLINING")
   # ADD_DEFINITIONS("/bigobj")
   # ADD_DEFINITIONS("/EHa")
   # ADD_DEFINITIONS("/Zm300")
   # ADD_DEFINITIONS("/DWIN32_VC")
   # ADD_DEFINITIONS("/DWIN64_VC")
   # ADD_DEFINITIONS("/DWIN64")
   # ADD_DEFINITIONS("/MP")

ELSE()
   set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -msse -msse2 -msse3 -mtune=native -march=native")
ENDIF()


# Add defines
add_definitions( -DBUILDING_PANDASKEL )
# add_definitions( -D_CRT_SECURE_NO_WARNINGS )

# Ignore some warnings
IF(MSVC)
  add_definitions( /wd4267 /wd4101 )
ENDIF()

set(CMAKE_BUILD_TYPE RelWithDebInfo)
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "")

# Build library
add_library(LUI MODULE ${SOURCES})

IF(MSVC)
   # SET_TARGET_PROPERTIES(LUI PROPERTIES LINK_FLAGS "/DEBUG /INCREMENTAL /ASSEMBLYDEBUG ")
ENDIF()

# Python wants .pyd on windows
IF (WIN32)
  set_target_properties(LUI 
    PROPERTIES 
    SUFFIX ".pyd")
ENDIF()

target_link_libraries(LUI ${LIBRARIES})

# After building, copy the file to the current directory
add_custom_command(
    TARGET LUI
    POST_BUILD
    COMMAND "${PYTHON_BIN}/python" "finalize.py" "$<TARGET_FILE:LUI>"
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})


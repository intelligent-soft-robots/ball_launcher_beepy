cmake_minimum_required(VERSION 3.5)
project(ball_launcher VERSION 1.0
                      LANGUAGES CXX)

find_package(Protobuf REQUIRED)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# generate C++ files required for protocol buffer
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ball_launcher.proto)
add_library(ball_launcher_proto STATIC ${PROTO_SRCS} ${PROTO_HDRS})
target_include_directories(ball_launcher_proto PUBLIC ${Protobuf_INCLUDE_DIRS})
target_link_libraries(ball_launcher_proto PUBLIC ${PROTOBUF_LIBRARIES})

# library for C++ ball launcher client
add_library(ball_launcher_client STATIC src/ball_launcher_client.cpp include/ball_launcher_client.hpp)
target_include_directories(ball_launcher_client PUBLIC include ${Protobuf_INCLUDE_DIRS} ${CMAKE_CURRENT_BINARY_DIR})
target_link_libraries(ball_launcher_client PUBLIC ball_launcher_proto)

# examples
add_subdirectory(examples)

# generate python code from protocol buffers
find_program(PYTHON "python") 

if (PYTHON)   
  protobuf_generate_python(PROTO_PY ball_launcher.proto)   
  #configure_file(setup.py.in setup.py)   
  add_custom_target(ball_launcher_py_proto ALL SOURCES ${PROTO_PY} ) 
  install(FILES ${PROTO_PY} DESTINATION ${CMAKE_CURRENT_LIST_DIR}/ball_launcher)
endif()


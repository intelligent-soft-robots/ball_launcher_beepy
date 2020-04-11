cmake_minimum_required(VERSION 3.5)
project(ball_launcher_beepy VERSION 1.0
                      LANGUAGES CXX)

find_package(Protobuf REQUIRED)

find_package(catkin REQUIRED)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

catkin_package(
 LIBRARIES ball_launcher_proto ball_launcher_client
 INCLUDE_DIRS include 
)
# generate C++ files required for protocol buffer
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ball_launcher.proto)
add_library(ball_launcher_proto STATIC ${PROTO_SRCS} ${PROTO_HDRS})
target_include_directories(ball_launcher_proto PUBLIC ${Protobuf_INCLUDE_DIRS})
target_link_libraries(ball_launcher_proto PUBLIC ${PROTOBUF_LIBRARIES})

# library for C++ ball launcher client
add_library(ball_launcher_client STATIC src/ball_launcher_client.cpp include/ball_launcher_beepy/ball_launcher_client.hpp)
target_include_directories(ball_launcher_client PUBLIC include ${Protobuf_INCLUDE_DIRS} ${CMAKE_CURRENT_BINARY_DIR})
target_link_libraries(ball_launcher_client PUBLIC ball_launcher_proto)

# tests
add_subdirectory(tests)

# generate python code from protocol buffers
find_program(PYTHON "python") 

if (PYTHON)   
  protobuf_generate_python(PROTO_PY ball_launcher.proto)   
  add_custom_target(ball_launcher_py_proto ALL SOURCES ${PROTO_PY} )
  install(FILES ${PROTO_PY}
    DESTINATION ${CATKIN_PACKAGE_PYTHON_DESTINATION})
  catkin_python_setup()
endif()



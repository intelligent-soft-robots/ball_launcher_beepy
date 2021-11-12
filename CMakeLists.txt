cmake_minimum_required(VERSION 3.5)
project(ball_launcher_beepy)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# dependencies		    
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(mpi_cmake_modules REQUIRED)
find_package(Protobuf REQUIRED)
ament_export_dependencies(
  mpi_cmake_modules
)


# prepare to export all needed targets
set(all_targets)
set(all_target_exports)

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
# add_subdirectory(tests)

# generate python code from protocol buffers
find_program(PYTHON "python") 
if (PYTHON)   
  protobuf_generate_python(PROTO_PY ball_launcher.proto)   
  add_custom_target(ball_launcher_py_proto ALL SOURCES ${PROTO_PY} )
  _ament_cmake_python_get_python_install_dir()
  install(FILES ${PROTO_PY}
    DESTINATION ${PYTHON_INSTALL_DIR})
  ament_python_install_package(${PROJECT_NAME} PACKAGE_DIR python/${PROJECT_NAME})
endif()

# install and export
install(DIRECTORY include/ DESTINATION include)
install(
  TARGETS ${all_targets}
  EXPORT ${all_target_exports}
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin
  INCLUDES
  DESTINATION include)
ament_package()

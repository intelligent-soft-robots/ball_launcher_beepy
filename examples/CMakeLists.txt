add_executable(launch_ball launch_ball.cpp)
target_include_directories(launch_ball PUBLIC "${CMAKE_SOURCE_DIR}/include" ${CMAKE_BINARY_DIR})
target_link_libraries(launch_ball PUBLIC ball_launcher_client zmq)

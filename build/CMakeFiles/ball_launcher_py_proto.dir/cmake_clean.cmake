file(REMOVE_RECURSE
  "ball_launcher_pb2.py"
)

# Per-language clean rules from dependency scanning.
foreach(lang )
  include(CMakeFiles/ball_launcher_py_proto.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()

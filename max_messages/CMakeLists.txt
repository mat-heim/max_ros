cmake_minimum_required(VERSION 2.8.3)
project(max_messages)

find_package(catkin REQUIRED COMPONENTS	message_generation)
	
## Generate services in the 'srv' folder
add_service_files(FILES
   Ears.srv
   EyeBrows.srv
   Eyes.srv
   Neck.srv
   Mouth.srv
   Cmd.srv
 )

generate_messages()

catkin_package(DEPENDS CATKIN DEPENDS message_runtime)

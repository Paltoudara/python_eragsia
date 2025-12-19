import funcs
map_students,map_courses,map_grades=funcs.parse_files()
funcs.validate_data(map_students,map_courses,map_grades)
funcs.menu(map_students,map_courses,map_grades)


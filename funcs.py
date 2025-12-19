import locale
#parse the files and creates the maps students,courses,grades
#sos everything is a str for printing make them ints and float
#done
def parse_files():
    map_students={}
    map_courses={}
    map_grades={}
    try:
        file_students=open("students.txt","r",encoding="utf-8")
        file_courses=open("courses.txt","r",encoding="utf-8")
        file_grades=open("grades.txt","r",encoding="utf-8")
    except FileNotFoundError:
        print("file not found")
        exit(1)
    #requirements for students
    # am->[1000,9999]
    # first_name length>0
    # last_name length>0
    # year in university>0
    for line in file_students:
        line=line.strip()
        if not line:
            continue
        parts=line.split(';')
        if len(parts)!=4:
            continue
        am=parts[0]
        first_name=parts[1]
        last_name=parts[2]
        year_in_university=parts[3]
        try:
            #keep only those that meet the requirements
            if 1000<=int(am)<=9999 and len(first_name)>0 and len(last_name)>0 and int(year_in_university)>0:
                map_students[int(am)]=[first_name,last_name,int(year_in_university)]
        except ValueError:
            print("invalid input check the files")
            exit(1)
    #requirements for courses
    #code of subject length>0
    #title length>0
    #semester >0
    #ects>0
    for line in file_courses:
        line=line.strip()
        if not line:
            continue
        parts=line.split(';')
        if len(parts)!=4:
            continue
        code=parts[0]
        title=parts[1]
        semester=parts[2]
        ects=parts[3]
        try:
            #keep only those that meet the requirements
            if len(code)>0 and len(title)>0 and int(semester)>0 and int(ects)>0:
                map_courses[code]=[title,int(semester),int(ects)]
        except ValueError:
            print("invalid input check the files")
            exit(1)
    #requirements for grades
    #am in [1000,9999]
    #code length>0
    #grade-> [0.0,10.0]
    for line in file_grades:
        line=line.strip()
        if not line:
            continue
        parts=line.split(';')
        if len(parts)!=3:
            continue
        am=parts[0]
        code=parts[1]
        grade=parts[2]
        try:
            #keep only those that meet the requirements
            if 1000<=int(am)<=9999 and len(code)>0 and 0.0<=float(grade)<=10.0:
                map_grades[(int(am),code)]=[float(grade)]
        except ValueError:
            print("invalid input check the files")
            exit(1)
    file_students.close()
    file_courses.close()
    file_grades.close()

    return map_students,map_courses,map_grades
#check if data from the file are valid
#done
def validate_data(map_students,map_courses,map_grades):
    #whatever appears in grades it must also appear at the students and courses maps
    #but whatever appears in students and courses maps is not necessary to be in grades
    for (key1,key2),value in map_grades.items():
        if (key1 not in map_students) or (key2 not in map_courses):
            print("invalid input check the files")
            exit(1)
#menu this is the main part of the system and also where the user gives his choices
#done
def menu(map_students,map_courses,map_grades):
    print("Φόρτωση δεδοµένων...")
    print(f"Φόρτωση students.txt: {len(map_students)}")
    print(f"Φόρτωση courses.txt: {len(map_courses)}")
    print(f"Φόρτωση grades.txt: {len(map_grades)}\n")
    while True:
        print("====================================")
        print("Mini SIS+ - Σύστηµα Φοιτητών")
        print("====================================")
        print("1. Προβολή όλων των φοιτητών")
        print("2. Προβολή όλων των µαθηµάτων")
        print("3. Αναζήτηση φοιτητή (µε AM)")
        print("4. Προβολή αναλυτικής βαθµολογίας φοιτητή")
        print("5. Εισαγωγή νέου φοιτητή")
        print("6. Εισαγωγή νέου µαθήµατος")
        print("7. Εισαγωγή νέας βαθµολογίας")
        print("8. Στατιστικά µαθήµατος")
        print("9. Δηµιουργία συνολικής αναφοράς σε αρχείο")
        print("0. Έξοδος")
        print("------------------------------------")
        try:
            choice = int(input("Επιλογη: "))
        except ValueError:
            print("invalid input")
            continue
        if choice == 1:
            print_all_students(map_students)
        elif choice == 2:
            print_all_subjects(map_courses)
        elif choice == 3:
            find_student_by_am(map_students)
        elif choice == 4:
            grades_of_a_student(map_students, map_courses, map_grades)
        elif choice == 5:
            insert_a_student(map_students)
        elif choice == 6:
            insert_a_subject(map_courses)
        elif choice == 7:
            insert_a_grade(map_students, map_courses, map_grades)
        elif choice == 8:
            stats_of_a_subject(map_courses, map_grades)
        elif choice == 9:
            create_full_report_file(map_students, map_courses, map_grades)
        elif choice == 0:
            print("Έξοδος από το σύστηµα Mini SIS+... Καλή συνέχεια!")
            return
#print all students function
#done
def print_all_students(map_students):
    # "Greek_Greece.1253" this works in windows
    locale.setlocale(locale.LC_COLLATE, "Greek_Greece.1253")
    print("--- Λίστα φοιτητών (αλφαβητικά) ---\n")
    list_students=list(map_students.items())
    # sort the students based on the last name,if two students have same last_name it sorts by
    # the first name the sorting is in alphabetical order,use locale library in order to sort
    # properly in greek letters
    list_students.sort(key=lambda  item:(locale.strxfrm(item[1][1]),locale.strxfrm(item[1][0])))
    # print everything about every student
    # list_students: am->[first_name,last_name,year_in_university]
    # list students will be something like this
    # [(1234, ['Γιώργος', 'Αλεξίου', 1]),
    # (3456, ['Ελένη', 'Κωνσταντίνου', 3]),
    # (2345, ['Μαρία', 'Πέτρου', 2])]
    # so parse it like this
    for key in list_students:
        print(f"{key[0]:<10}", end='')
        print(f"{key[1][0]:<30}", end='')
        print(f"{key[1][1]:<30}", end='')
        print(f"(Ετος: {key[1][2]})", end='')
        print()

    print()
    input("Πατήστε Enter για συνέχεια...")
    print()

#print all subjects function
#done
def print_all_subjects(map_courses):
    print("--- Λίστα µαθηµάτων (ανά εξάµηνο) ---")
    max_semester=-1
    # find max semester in order to know where to stop
    # map_courses: subject_code->[title,semester,ects]
    for key, value in map_courses.items():
        if value[1] > max_semester:
            max_semester = value[1]
    semester=1
    #find max_semester
    while semester <= max_semester:
        # for every semester print all subjects
        print(f"Εξαμηνο {semester}")
        for key, value in map_courses.items():
            if value[1] == semester:
                print(f"  {key:<10}", end='')
                print(f"{value[0]:<30}", end='')
                print(f"(ECTS: {value[2]})")
        semester += 1
    print()
    input("Πατήστε Enter για συνέχεια...")
    print()
#find student by am
#done
def find_student_by_am(map_students):
    # we expect an int between [1000,9999]
    while True:
        # wait until user gives the proper input that we want
        try:
            am = int(input("Δώσε Αριθµό Μητρώου (AM): "))
        except ValueError:
            print("invalid input")
            continue
        if 1000 <= am <= 9999:
            break
        else:
            print("ο αριθμός μητρώου πρέπει να είναι τετραψήφιος θετικός αριθμός")
    #we know now that am is in [1000,9999]
    # if am in students map
    # map_students am->[first_name,last_name,year_in_university]
    if am in map_students:
        print("Βρέθηκε φοιτητής:")
        print(f"AM: {am}")
        print(f"Όνοµα: {map_students[am][0]}")
        print(f"Επώνυµο: {map_students[am][1]}")
        print(f"Έτος σπουδών: {map_students[am][2]}")
    else:
        # student not found
        print(f"Δεν βρέθηκε φοιτητής με ΑΜ: {am}")
    print()
    input("Πατήστε Enter για συνέχεια...")
    print()
#grades of a student function
#done
def grades_of_a_student(map_students,map_courses,map_grades):
    # we expect an int between [1000,9999]
    while True:
        try:
            am = int(input("Δώσε Αριθµό Μητρώου (AM): "))
        except ValueError:
            print("invalid input")
            continue
        if 1000 <= am <= 9999:
            break
        else:
            print("Ο αριθμός μητρώου πρέπει να είναι ένας θετικός τετραψήγιος")
    # whatever am exists in map_grades exists also in students check validate_data function
    #whatever code of subject exists in grades it also exists in the courses map check validate_data function
    if am in map_students:
        print()
        print("--- Αναλυτική βαθµολογία φοιτητή ---")
        print()
        #the student might not have any grades
        print(f"Φοιτητής: {am} - {map_students[am][0]} {map_students[am][1]} (Έτος: {map_students[am][2]})")
        print("Μάθημα               Εξάμηνο     Βαθμός")
        print("---------------------------------------")
        # map_grades: (am,subject_code)->[grade]
        # map_courses: subject_code->[title,semester,ects]
        # we search all his grades in every subject
        for (key1, key2), value in map_grades.items():
            if am == key1:  # find that subject and print about it
                print(
                    f"{map_courses[key2][0]:<30} {key2:<10} {map_courses[key2][1]:<10} {map_grades[(key1, key2)][0]:<10}")
        #
        print()
        subject_counter = 0
        how_many_passed = 0
        average = 0.0
        # for every subject in map_grades
        for (key1, key2), value in map_grades.items():
            if am == key1:
                average += value[0]
                subject_counter += 1
                if value[0] >= 5.0:
                    how_many_passed += 1
        print(f"Σύνολο µαθηµάτων µε βαθµό: {subject_counter}")
        print(f"Περασµένα µαθήµατα (βαθµός ≥ 5): {how_many_passed}")
        if subject_counter > 0:
            print(f"Μέσος όρος: {average / subject_counter}")
        else:
            print(f"Μέσος όρος: 0.0")
    else:
        print("Δεν υπάρχει φοιτητής με αυτόν τον αριθμό μητρώου")

    print()
    input("Πατήστε Enter για συνέχεια...")
    print()

#insert a student function
#done
def insert_a_student(map_students):
    print("--- Εισαγωγή νέου φοιτητή ---")
    # give am
    while True:
        try:
            am = int(input("Δωσε ΑΜ: "))
        except ValueError:
            print("invalid input")
            continue
        if 1000 <= am <= 9999:
            break
        else:
            print("ο αριθμός μητρώου πρέπει να είναι τετραψήφιος θετικός αριθμός")
    while True:
        first_name = input("Δώσε Όνοµα: ")
        last_name = input("Δώσε Επώνυµο: ")
        if len(first_name) != 0 and len(last_name) != 0:
            break
        else:
            print("Το όνομα και το επίθετο δεν πρέπει να είναι άδεια")
    # year in university
    while True:
        try:
            year_in_university = int(input("Δώσε Έτος σπουδών: "))
        except ValueError:
            print("invalid input")
            continue
        if year_in_university > 0:
            break
        else:
            print("Έτος σπουδών πρέπει να είναι θετικό")
    # if we don't already have this student insert him in the map and in the file
    if am not in map_students:
        print("Επιβεβαίωση:")
        print(f"AM: {am}, Όνοµα: {first_name}, Επώνυµο: {last_name}, Έτος: {year_in_university}")
        answer = input("Καταχώρηση; (Ν/Ο): ")
        if answer == 'Ν':
            map_students[am] = [first_name, last_name, year_in_university]
            # change students.txt here
            try:
                file_students = open("students.txt", "a", encoding="utf-8")
            except FileNotFoundError:
                print("file not found")
                exit(1)
            file_students.write(f"\n{am};{first_name};{last_name};{year_in_university}")
            file_students.close()
            print("Ο φοιτητής καταχωρήθηκε µε επιτυχία.")
            print("(Ενηµερώθηκε και το αρχείο students.txt)")
    else:
        print("Αυτός ο μαθήτης υπάρχει ήδη")
    print()
    input("Πατήστε Enter για συνέχεια...")
    print()
#insert a subject function
#done
def insert_a_subject(map_courses):
    print("--- Εισαγωγή νέου μαθήματος ---")
    while True:
        code=input("Δώσε τον κωδικό του μαθήματος: ")
        if len(code)>0:
            break
        else:
            print("Ο κωδικός του μαθήματος δεν πρέπει να είναι άδειος")
    # title must not be empty
    while True:
        title = input("Δώσε τίτλο μαθήματος ")
        if len(title) > 0:
            break
        else:
            print("O τίτλος του μαθήματος δεν πρέπει να είναι άδειος")
    #semester>0
    while True:
        try:
            semester=int(input("Δώσε το εξάμηνο που διδάσκεται το μάθημα: "))
        except ValueError:
            print("invalid input")
            continue
        if semester>0:
            break
        else:
            print("Το εξάμηνο που διδάσκεται το μάθημα πρέπει να ειναι >0")
    # ects>0
    while True:
        try:
            ects = int(input("Δώσε ects: "))
        except ValueError:
            print("invalid input")
            continue
        if ects>0:
            break
        else:
            print("ects πρέπει να είναι >0")
    # map_courses: subject_code->[title,semester,ects]
    # if the subject is not in our map insert it
    if code in map_courses:
        print(f"Το μάθημα με κωδικό {code} υπάρχει ήδη")
    else:
        print("Επιβεβαίωση:")
        print(f"Κωδικός μαθήματος: {code}, τίτλος: {title}, εξάμηνο: {semester}, ects: {ects} ")
        answer = input("Καταχώρηση; (Ν/Ο): ")
        if answer == 'Ν':
            # change the map and the courses.txt
            map_courses[code] = [title,semester,ects]
            try:
                file_courses = open("courses.txt", "a", encoding="utf-8")
            except FileNotFoundError:
                print("file not found")
                exit(1)
            file_courses.write(f"\n{code};{title};{semester};{ects}")
            file_courses.close()
            print("Το μάθημα καταχωρήθηκε με επιτυχία")
            print("(Ενηµερώθηκε και το αρχείο courses.txt)")
        else:
            print("Το μάθημα δεν καταχωρήθηκε")
    print()
    input("Πατήστε Enter για συνέχεια...")
    print()
#insert a grade function
#done
def insert_a_grade(map_students,map_courses,map_grades):
    print("--- Εισαγωγή νέας βαθµολογίας ---")
    while True:
        try:
            am = int(input("Δωσε ΑΜ:"))
        except ValueError:
            print("invalid input")
            continue
        if 1000 <= am <= 9999:
            break
        else:
            print("ο αριθμός μητρώου πρέπει να είναι τετραψήφιος θετικός αριθμός")
    while True:
        code = input("Δώσε τον κωδικό του μαθήματος: ")
        if len(code) > 0:
            break
        else:
            print("Ο κωδικός του μαθήματος δεν πρέπει να είναι άδειος")
    # if we already know the student and the subject we just put a mark
    # map_courses: subject_code->[title,semester,ects]
    # map_students: am->[first_name,last_name,year_in_university]
    if (am in map_students) and (code in map_courses):
        print(f"Βρέθηκε φοιτητής: {map_students[am][0]} {map_students[am][1]}")
        print(f"Μάθηµα: {code} - {map_courses[code][0]}")
        while True:
            try:
                grade =float( input("Δώσε βαθµό (0-10): "))
            except ValueError:
                print("invalid input")
                continue
            if 0.0<=grade<=10.0:
                break
            else:
                print("Ο βαθμός πρέπει να ειναι απο (0-10)")


        print("Καταχώρηση:")
        print(f"{am};{code};{grade}")
        # EXTRA EGGRAFH ARXEIO
        map_grades[(am,code)] = [grade]
        try:
            file_grades = open("grades.txt", "w", encoding="utf-8")
        except FileNotFoundError:
            print("file not found")
            exit(1)
        # map_grades: (am,subject_code)->[grade]
        for (key1, key2), value in map_grades.items():
            file_grades.write(f"{key1};{key2};{value[0]}\n")
        file_grades.close()
        print("Η βαθµολογία καταχωρήθηκε επιτυχώς.")
        print("(Ενηµερώθηκε και το αρχείο grades.txt)")
    print()
    input("Πατήστε Enter για συνέχεια...")
    print()
#stats_of_a_subject function
#done
def stats_of_a_subject(map_courses,map_grades):
    #map_courses code->[title,semester,ects]
    #map_grades (am,code)->[grade]
    print("--- Στατιστικά µαθήµατος ---")
    while True:
        code=input("Δώσε τον κωδικό του μαθήματος: ")
        if len(code)>0:
            break
        else:
            print("Δεν είναι σωστός κωδικός μαθήματος αυτός")
    if code in map_courses:
        print(f"Μάθηµα: {code} - {map_courses[code][0]}")
        print()
    else:
        print("Αυτό το μάθημα δεν υπάρχει")
        return
    grades=[]
    for (key1, key2), value in map_grades.items():
        if key2==code:
            grades.append(value[0])
    print(f"Βαθμοί: {grades}")
    print(f"Αριθµός φοιτητών: {len(grades)}")
    if len(grades) != 0:
        print(f"Μέσος όρος: {sum(grades) / len(grades)}")
        print(f"Ελάχιστος βαθµός: {min(grades)}")
        print(f"Μέγιστος βαθµός: {max(grades)}")
    else:
        print("Μέσος όρος: 0.0")
        print("Ελάχιστος βαθµός: 0.0")
        print("Μέγιστος βαθµός: 0.0")
    print(f"Περασμένοι φοιτητές (βαθμός >=5): {len([x for x in grades if x >= 5.0])}")

    print()
    input("Πατήστε Enter για συνέχεια...")
    print()
#create_full_report_file
#done
def create_full_report_file(map_students,map_courses,map_grades):
    file_report=open("full_report.txt","w",encoding="utf-8")
    print("--- Δηµιουργία πλήρους αναφοράς ---")
    print("Δηµιουργία αρχείου: full_report.txt ...")
    print("Η αναφορά δηµιουργήθηκε µε επιτυχία.")
    print("Περίληψη:")
    file_report.write(f"- Σύνολο φοιτητών: {len(map_students)}\n")
    file_report.write(f"- Σύνολο µαθηµάτων: {len(map_courses)}\n")
    file_report.write(f"- Σύνολο βαθµολογιών: {len(map_grades)}\n")
    print(f"- Σύνολο φοιτητών: {len(map_students)}")
    print(f"- Σύνολο µαθηµάτων: {len(map_courses)}")
    print(f"- Σύνολο βαθµολογιών: {len(map_grades)}")
    #map_grades: (am,subject_code)->[grade]
    _sum=0.0
    for (key1,key2),value in map_grades.items():
        _sum+=value[0]
    if len(map_grades)!=0:
        print(f"- Γενικός µέσος όρος: {_sum/len(map_grades)}")
        file_report.write(f"- Γενικός µέσος όρος: {_sum/len(map_grades)}\n")
    else:
        print("- Γενικός µέσος όρος: 0.0")
        file_report.write("- Γενικός µέσος όρος: 0.0\n")
    #for every am make average and take max
    #_map will contain am->[sum,how_many_grades]
    _map={}
    for (key1,key2),value in  map_grades.items():
        #initialise
        _map[key1]=[0.0,0]
    for (key1,key2),value in map_grades.items():
       _map[key1][0]+=value[0]
       _map[key1][1]+=1
    if len(_map)==0:
        #there is no best student because there are no students with grades
        file_report.close()
        return
    max_average=-5
    max_am=-5
    #_map will contain am->[sum,how_many_grades]
    for key,value in _map.items():
        if (value[0]/value[1])>max_average:
            max_average=value[0]/value[1]
            max_am=key
    #we know that whatever am in map_grades will also be in map_students
    print(f"Καλύτερος φοιτητής: {max_am} ({map_students[max_am][0]} {map_students[max_am][1]}) με Μ.Ο {max_average}")
    file_report.write(f"Καλύτερος φοιτητής: {max_am} ({map_students[max_am][0]} {map_students[max_am][1]}) με Μ.Ο {max_average}\n")
    file_report.close()

    print()
    input("Πατήστε Enter για συνέχεια...")
    print()

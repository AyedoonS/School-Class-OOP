# An OOP project i've been working on, it 
# is a WIP, updates will eventually be made

class School:

    def __init__(self, name: str):
        self.school_name = name
        self.list_students = {}
        self.num_students = 0
        self.list_faculty = {}
        self.num_faculty = 0

    def update_count_people(self):
        self.num_faculty = len(self.list_faculty)
        self.num_students = len(self.list_students)

    def add_student(self, student):
        """
        Adds student to the schools list of students, a dict
        <list_students>, with keys being the user_id of <student>
        """
        self.list_students.setdefault(student.get_id(),
                                      [student])
        self.update_count_people()

    def remove_student(self, student):
        """
        Removes a student from the school list of students
        """
        # TODO: Finish this
        pass

    def add_faculty(self, faculty):
        # TODO: Finish this
        self.list_faculty.setdefault([], [])
        self.update_count_people()

    def remove_faculty(self, faculty):
        """
        Removes a member of faculty from this school
        """
        # TODO: Finish this
        pass

    def get_name(self):
        """
        Returns name of the school
        """
        return self.school_name

    def check_student(self, student):
        """
        Checks if a student <student> is in the list of students
        for the school
        """
        for stu in self.list_students:
            if student.get_id() == stu:
                return True
        return False

    def check_faculty(self, faculty):
        """
        Checks if a faculty member is in the list of faculty
        members for this specific school
        """
        # TODO: Finish this

    def get_students(self):
        """
        Returns a list of students that attend the school
        """
        list_stu = []
        for i in self.list_students:
            list_stu.append(self.list_students[i][0])
        return list_stu

    def get_passing_students(self, min_gr: float):
        """
        Returns a list of students whose cGPA is greater-than or
        equal-to the minimum grade point <min_gr>
        """
        list_stu = []
        for i in self.list_students:
            if self.list_students[i][0].get_cgpa() >= min_gr:
                list_stu.append(self.list_students[i])
        return list_stu

    def get_faculty(self):
        """
        Returns a list of faculty at the school
        """
        list_fac = []
        for i in self.list_faculty:
            list_fac.append(self.list_faculty[i][0])
        return list_fac

    def get_failing_faculty(self, min_rt: float):
        """
        Returns a list of faculty whose rating is less-than
        the minimum rating <min_rt>
        """
        # TODO: Finish this
        list_fac = []
        for i in self.list_faculty:
            pass
        return list_fac

    def __eq__(self, other):
        """
        Returns True if <num_students> of self equals num_students of other
        """
        return (self.num_students + self.num_faculty
                == other.num_students + other.num_faculty)

    def __str__(self):
        """
        Returns a string representation of the school
        """
        return (f'School: {self.school_name}, '
                f'Number of students: {self.num_students}')


class Student:

    # TODO: randomly generate user id for each student
    # + (maybe explicitly check to ensure it is not already taken)
    def __init__(self, name: str, user_id: int, school: School):
        """
        Initialize student, assign it variables <name>, <user_id>,
        and <school>, if it is a valid school
        """
        self.name = name
        self.ID = user_id
        self.cgpa = 0
        self.course_sel = {1: {}, 2: {}, 3: {}, 4: {}}
        self.credits = 0

        try:
            school.add_student(self)
            self.school_attending = school.get_name()
        except TypeError:
            self.school_attending = None

    @staticmethod
    def get_year(code: str) -> int:
        """
        Returns the level of a course given its code, <code>
        """
        return int(code[3])

    def update_cgpa(self):
        """
        Updates student cGPA - The average of their GPA across all their
        courses
        """
        sum_gpa, num_courses = 0, 0
        for year in self.course_sel:
            for lec in self.course_sel[year]:
                if isinstance(self.course_sel[year][lec], float):
                    sum_gpa += self.course_sel[year][lec]
                    num_courses += 1
        self.cgpa = round(sum_gpa / num_courses, 2)

    def add_courses(self, courses: list[str]):
        """
        Adds courses from list: <courses> to Student's transcript
        """
        for course in courses:
            year = self.get_year(course)
            self.course_sel[year].setdefault(course, 'In-Progress')

    def add_marks(self, mark_list: list[list[str, int]]):
        """
        Adds marks, <mark_list[1]> to the courses given a list of marks, with
        their corresponding course <mark_list[0]>, and updates Student's cGPA
        """
        for course in mark_list:
            year = self.get_year(course[0])
            if (course[0] in self.course_sel[year]
                    and self.course_sel[year][course[0]] == 'In-Progress'):
                self.course_sel[year][course[0]] = course[1]
                self.credits += 1
        self.update_cgpa()

    def update_mark(self, course: str, mark: float):
        """
        Updates the GPA mark for a course, <course> of a Student from
        its original value -- if there was anything -- to <mark>
        """
        year = self.get_year(course)
        if course in self.course_sel[year]:
            self.course_sel[year][course] = mark
            self.update_cgpa()

    def remove_courses(self, courses: list[str]):
        """
        Removes courses in list <courses> from Student's transcript, if
        it was a course taken by the student
        """
        for lec in courses:
            for year in self.course_sel:
                if lec in self.course_sel[year]:
                    self.course_sel[year].pop(lec)
                    self.credits -= 1
        self.update_cgpa()

    def get_courses(self):
        """
        Returns the course codes of courses a student had taken
        throughout their time at the school, along with the GPA of
        those courses if anything was recorded. Returns NoData for the
        years there are no course data available
        """
        courses = f"Name: {self.name}\n"
        for year in self.course_sel:
            courses += f"--------Year {year}--------\n"
            if len(self.course_sel[year]) == 0:
                courses += '       NoData\n'
            else:
                for course in self.course_sel[year]:
                    courses += (f"|c| Course: {course} "
                                f"|g| GPA: {self.course_sel[year][course]}\n")
        return courses

    def change_school(self, school: School):
        """
        Changes the School the Student attends to <school>.
        """
        school.list_students.pop(self.get_id())
        self.school_attending = school.get_name()

    def get_school(self):
        """
        Returns the school that the student attends
        """
        return self.school_attending

    def get_id(self):
        """
        Returns student's ID
        """
        return self.ID

    def get_name(self):
        """
        Returns student's name
        """
        return self.name

    def get_cgpa(self):
        """
        Returns student's cGPA
        """
        return self.cgpa

    def get_status(self):
        """
        Returns students year of study
        (given by their credit count)
        """
        if self.credits >= 24:
            return 4
        elif self.credits >= 16:
            return 3
        elif self.credits >= 8:
            return 2
        else:
            return 1

    def __eq__(self, other):
        """
        Returns cGPA Student <self> == cGPA Student <other>
        """
        return self.cgpa == other.cgpa

    def __str__(self):
        """
        Returns a string representation of Student <self>, including their
        Name, School, ID, and cGPA.
        """
        return (f'Name: {self.name}, School: {self.get_school()}, '
                f'ID: {self.ID}, Credits achieved: {self.credits}, '
                f'Year of Study: {self.get_status()}, cGPA: {self.cgpa}')


class Faculty:

    def __init__(self, name: str, user_id: int, school: School,
                 position: str, salary: float):
        self.name = name
        self.ID = user_id
        self.ann_salary = salary
        self.position = position
        try:
            school.add_faculty(self)
            self.school_working = school.get_name()
        except TypeError:
            self.school_working = None

    def update_salary(self, updated_salary):
        self.ann_salary = updated_salary

    def update_school(self):
        """
        Updates the school at which this member of faculty works in
        """
        # TODO: Finish this
        pass

    def get_id(self):
        """
        Returns the ID of the member of faculty
        """
        return self.ID

    def get_position(self):
        """
        Returns the role/position/level the member of faculty is working at
        """
        return self.position

    def update_position(self, new_pos: str):
        """
        Updates/changes the position of this member of faculty to
        <new_pos>
        """
        self.position = new_pos

    def __eq__(self, other):
        return self.ann_salary == other.ann_salary

    def __str__(self):
        return (f'Name: {self.name}, ID: {self.ID}, '
                f'Role: {self.get_position()}, School: {self.school_working}, '
                f'Salary: {self.ann_salary}')

# An OOP project i've been working on, it 
# is a WIP, updates will eventually be made

class SchoolBoard:
    def __init__(self, board: str, region: str) -> None:
        self.name_board = board
        self.region = region
        self.list_schools = []
        self.num_schools = 0

    def get_name_board(self) -> str:
        return self.name_board

    def add_school(self, school) -> None:
        """
        Adds a school to a list comprised of schools associated
        with the school board <self>
        """
        if school in self.list_schools:
            return None
        else:
            self.list_schools.append(school)

    def remove_school(self, school) -> None:
        if school in self.list_schools:
            self.list_schools.pop(school)
        return None

    def get_schools(self) -> list:
        """
        Returns a list of all the schools affiliated with the school board
        self
        """
        return self.list_schools

    def find_school(self, school) -> bool:
        """
        Returns True if school <school> is affiliated with the school board
        self
        """
        return school in self.list_schools

    def get_region(self) -> str:
        """
        Returns the region of the school
        """
        return self.region

    def __eq__(self, other) -> bool:
        """
        Returns true if the number of schools in the school board
        <self> equals those in <other>
        """
        return self.num_schools == other.num_schools

    def __str__(self) -> str:
        """
        Returns a basic string representation of self
        """
        return f'Name of board: {self.name_board}, Region: {self.region}'

    def __repr__(self) -> str:
        """
        Returns a more detailed string representation of self
        """
        return (f'Name of board: {self.name_board}, Region: {self.region}, '
                f'Number of schools: {self.num_schools}')


class School:

    def __init__(self, name: str) -> None:
        self.school_name = name
        self.list_students = {}
        self.num_students = 0
        self.list_faculty = {}
        self.num_faculty = 0

    def update_count_people(self) -> None:
        """
        Updates the count of students and faculty in the school
        """
        self.num_faculty = len(self.list_faculty)
        self.num_students = len(self.list_students)

    def add_student(self, student) -> None:
        """
        Adds student to the schools list of students, a dict
        <list_students>, with keys being the user_id of <student>

        TODO (maybe): Split dict of students by their year of study
        (i.e., a key for years 1-4).
        """
        student.change_school(self)
        student.school_attending = self.school_name
        self.list_students.setdefault(student.get_id(), student)
        self.update_count_people()

    def remove_student(self, student) -> None:
        """
        Removes a student from the school list of students
        """
        if student.get_id() in self.list_students:
            self.list_students.pop(student.get_id())
            student.change_school(None)

    def add_faculty(self, faculty) -> None:
        """
        Adds faculty to the schools list of faculty, a dict
        <list_faculty>, with keys being the user_id of faculty
        member
        """
        self.list_faculty.setdefault(faculty.get_id(), faculty)
        self.update_count_people()

    def remove_faculty(self, faculty) -> None:
        """
        Removes a member of faculty from this school
        """
        if faculty in self.list_faculty:
            self.list_faculty.pop(faculty.get_id())
            faculty.update_school(None)
            faculty.update_salary(0)

    def check_student(self, student) -> bool:
        """
        Checks if a student <student> is in the list of students
        for the school
        """
        return student.get_id() in self.list_students

    def check_faculty(self, faculty) -> bool:
        """
        Checks if a faculty member is in the list of faculty
        members for this specific school
        """
        return faculty.get_id() in self.list_students

    def get_students(self) -> list:
        """
        Returns a list of students that attend the school
        """
        list_stu = []
        for i in self.list_students:
            list_stu.append(str(self.list_students[i]))
        return list_stu

    def get_passing_students(self, min_gr: float) -> list:
        """
        Returns a list of students whose cGPA is greater-than or
        equal-to the minimum grade point <min_gr>
        """
        list_stu = []
        for i in self.list_students:
            if self.list_students[i].get_cgpa() >= min_gr:
                list_stu.append(str(self.list_students[i]))
        return list_stu

    def get_faculty(self) -> list:
        """
        Returns a list of faculty at the school
        """
        list_fac = []
        for i in self.list_faculty:
            list_fac.append(str(self.list_faculty[i]))
        return list_fac

    def get_failing_faculty(self, min_rt: float) -> list:
        """
        Returns a list of faculty whose rating is less-than
        the minimum rating <min_rt>
        """
        list_fac = []
        for i in self.list_faculty:
            if self.list_faculty[i].get_rating() < min_rt:
                list_fac.append(str(self.list_faculty[i]))
        return list_fac

    def get_name(self) -> str:
        """
        Returns name of the school
        """
        return self.school_name

    def __eq__(self, other) -> bool:
        """
        Returns True if <num_students> of self equals num_students of other
        """
        return (self.num_students + self.num_faculty
                == other.num_students + other.num_faculty)

    def __str__(self) -> str:
        """
        Returns a string representation of School <self>
        """
        return self.school_name

    def __repr__(self) -> str:
        return (f'{self.school_name}, Students: {self.num_students}, '
                f'Faculty: {self.num_faculty}')


class Student:

    # TODO: randomly generate user id for each student
    # + (maybe explicitly check to ensure it is not already taken)
    def __init__(self, name: str, user_id: int, school: School) -> None:
        """
        Initialize student, assign it variables <name>, <user_id>,
        and <school>, if it is a valid school
        """
        self.name = name
        self.ID = user_id
        self.cgpa = 0
        self.course_sel = {1: {}, 2: {}, 3: {}, 4: {}}
        self.credits = 0
        self.school = school
        self.school_attending = school.get_name()
        school.add_student(self)

        self.num_courses = 0

    @staticmethod
    def get_year(code: str) -> int:
        """
        Returns the level of a course given its code, <code>.

        This is represented by the third character of a course code.
        (ex. MA1[3]099 = third-year course, PH2[4]001 = fourth-year)
        """
        return int(code[3])

    def update_cgpa(self) -> None:
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
        self.num_courses = num_courses
        if num_courses == 0:
            return None
        else:
            self.cgpa = round(float(sum_gpa / num_courses), 2)

    def add_courses(self, courses: list[str]) -> None:
        """
        Adds courses from list: <courses> to Student's transcript
        """
        for course in courses:
            year = self.get_year(course)
            self.course_sel[year].setdefault(course, 'In-Progress')

    def add_marks(self, mark_list: list[list[str, int]]) -> None:
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

    def update_mark(self, course: str, mark: float) -> None:
        """
        Updates the GPA mark for a course, <course> of a Student from
        its original value -- if there was anything -- to <mark>
        """
        year = self.get_year(course)
        if course in self.course_sel[year]:
            self.course_sel[year][course] = mark
            self.update_cgpa()

    def remove_courses(self, courses: list[str]) -> None:
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

    def get_courses(self) -> str:
        """
        Returns the course codes of courses a student had taken
        throughout their time at the school, along with the GPA of
        those courses if anything was recorded. Returns NoData for the
        years there are no course data available
        """
        courses = f"Name: {self.name}, at {self.get_school()}\n"
        for year in self.course_sel:
            courses += f"--------Year {year}--------\n"
            if len(self.course_sel[year]) == 0:
                courses += '        NoData\n'
            else:
                for course in self.course_sel[year]:
                    courses += (f"|c| Course: {course} "
                                f"|g| GPA: {self.course_sel[year][course]}\n")
        return courses

    def change_school(self, school: School) -> None:
        """
        Changes the School the Student attends to <school>.
        """
        if isinstance(school, School) and school is not self.school:
            self.school.list_students.pop(self.get_id())
            self.school = school
            self.school_attending = school.get_name()
        elif school is not self.school:
            self.school_attending = '--None--'
        else:
            return None

    def get_school(self) -> str:
        """
        Returns the school that the student attends
        """
        return self.school_attending

    def get_id(self) -> int:
        """
        Returns student's ID
        """
        return self.ID

    def get_name(self) -> str:
        """
        Returns student's name
        """
        return self.name

    def get_cgpa(self) -> float:
        """
        Returns student's cGPA
        """
        return self.cgpa

    def get_status(self) -> int:
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

    def __eq__(self, other) -> bool:
        """
        Returns cGPA Student <self> == cGPA Student <other>
        """
        return self.cgpa == other.cgpa

    def __str__(self) -> str:
        """
        Returns a string representation of Student <self>, including their
        Name, School, ID, and cGPA.
        """
        return (f'Name: {self.name}, Student ID: {self.ID}, '
                f'Credits achieved: {self.credits}, cGPA: {self.cgpa}')

    def __repr__(self) -> str:
        """
        Returns a more detailed string representation of Student
        """
        return (f'Name: {self.name}, School: {self.get_school()}, '
                f'Student ID: {self.ID}, Credits achieved: {self.credits}, '
                f'Year of Study: {self.get_status()}, cGPA: {self.cgpa}')


class Faculty:

    def __init__(self, name: str, user_id: int, school: School,
                 position: str, salary: float) -> None:
        self.name = name
        self.ID = user_id
        self.ann_salary = salary
        self.position = position
        self.rating = 5.0
        self.school = school
        self.work_school = school.get_name()
        school.add_faculty(self)

    def update_salary(self, updated_salary: float) -> None:
        """
        Updates the salary for the faculty member
        """
        self.ann_salary = updated_salary

    def update_school(self, school: School) -> None:
        """
        Updates the school at which this member of faculty works in
        """
        if isinstance(school, School) and school is not self.school:
            self.school.list_faculty.pop(self.get_id())
            self.school = school
            self.work_school = school.get_name()
        else:
            self.work_school = '--None--'

    def get_rating(self) -> float:
        """
        Returns the rating of faculty member. The rating is based on a
        10-point scale where 0 = bad and 10 = good
        """
        return float(self.rating)

    def update_rating(self, updated_rating: float) -> None:
        """
        Updates faculty member rating
        """
        if updated_rating > 10:
            self.rating = 10
        elif updated_rating < 0:
            self.rating = 0
        else:
            self.rating = updated_rating

    def get_id(self) -> int:
        """
        Returns the ID of the member of faculty
        """
        return self.ID

    def get_position(self) -> str:
        """
        Returns the role/position/level the member of faculty is working at
        """
        return self.position

    def update_position(self, new_pos: str) -> None:
        """
        Updates/changes the position of this member of faculty to
        <new_pos>
        """
        self.position = new_pos

    def get_school(self) -> str:
        return self.work_school

    def __eq__(self, other) -> bool:
        return self.rating == other.rating

    def __str__(self) -> str:
        """
        Returns a string representation of Faculty member
        """
        return (f'Name: {self.name}, ID: {self.ID}, '
                f'Role/Position: {self.get_position()}')

    def __repr__(self) -> str:
        """
        Returns a more detailed string representation of Faculty
        member
        """
        return (f'Name: {self.name}, ID: {self.ID}, '
                f'Role/Position: {self.get_position()}, '
                f'School employed: {self.get_school()}, '
                f'Annual Salary: ${self.ann_salary}, '
                f'Member Rating: {self.get_rating()}')

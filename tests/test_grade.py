import random
from faker import Faker
import requests

from services.university.helpers.grade_helper import GradeHelper
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.models.base_grade import MIN_GRADE, MAX_GRADE
from services.university.models.grade_request import GradeRequest
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService
from utils.soft_assert import SoftAssert


faker = Faker()

NON_EXIST_ID_VALUE = 0

class TestGrade:
    def test_grade_status_code(self, university_api_utils_admin):
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)
        grade_response = grade_helper.post_grade(
            {"teacher_id": NON_EXIST_ID_VALUE,
             "student_id": NON_EXIST_ID_VALUE,
             "grade": random.randint(MIN_GRADE, MAX_GRADE)})

        assert grade_response.status_code == requests.codes.not_found,\
            f"Wrong teacher_id or student_id.\n"\
            f"Actual: {grade_response.status_code}\n"\
            f"Expected: {requests.codes.not_found}"

    def test_grade_post(self, university_api_utils_admin):
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group)

        student = StudentRequest(first_name=faker.first_name(),
                                 last_name=faker.last_name(),
                                 email=faker.email(),
                                 degree=random.choice([option for option in DegreeEnum]),
                                 phone=faker.numerify("+7##########"),
                                 group_id=group_response.id)
        student_response = university_service.create_student(student)

        teacher = TeacherRequest(first_name=faker.first_name(),
                                 last_name=faker.last_name(),
                                 subject=random.choice([option for option in SubjectEnum]))
        teacher_response = university_service.create_teacher(teacher)

        random_grade = random.randint(MIN_GRADE, MAX_GRADE)
        grade = GradeRequest(teacher_id=teacher_response.id,
                             student_id=student_response.id,
                             grade=random_grade)
        grade_response = university_service.give_grade(grade)

        with SoftAssert() as soft:
            soft.check(grade_response.teacher_id == teacher_response.id,
            f"Wrong teacher id.\n"
            f"Actual: {grade_response.teacher_id}\n"
            f"Expected: {teacher_response.id}")

            soft.check(grade_response.student_id == student_response.id,
            f"Wrong student id.\n"
            f"Actual: {grade_response.student_id}\n"
            f"Expected: {student_response.id}")

            soft.check(grade_response.grade == random_grade,
            f"Wrong grade.\n"
            f"Actual: {grade_response.grade}\n"
            f"Expected: {random_grade}")
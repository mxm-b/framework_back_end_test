import random
from faker import Faker
import requests

from services.university.helpers.grade_helper import GradeHelper
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.helpers.teacher_helper import TeacherHelper
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum

faker = Faker()


class TestGrade:
    def test_grade_status_code(self, university_api_utils_admin):
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)
        grade_response = grade_helper.post_grade({"teacher_id": random.randint(1, 100),
                                                 "student_id": random.randint(1, 100),
                                                 "grade": random.randint(1, 5)})

        assert grade_response.status_code == requests.codes.not_found,\
            f"Wrong teacher_id or student_id.\n"\
            f"Actual: {grade_response.status_code}\n"\
            f"Expected: {requests.codes.not_found}"

    def test_grade_post(self, university_api_utils_admin):
        group_helper = GroupHelper(api_utils=university_api_utils_admin)
        group_response = group_helper.post_group({"name": faker.name()})

        student_helper = StudentHelper(api_utils=university_api_utils_admin)
        student_response = student_helper.post_student({"first_name": faker.first_name(),
                                                        "last_name": faker.last_name(),
                                                        "email": faker.email(),
                                                        "degree": random.choice([option for option in DegreeEnum]),
                                                        "phone": faker.numerify("+7##########"),
                                                        "group_id": group_response.json()["id"]})

        teacher_helper = TeacherHelper(api_utils=university_api_utils_admin)
        teacher_response = teacher_helper.post_teacher({"first_name": faker.first_name(),
                                                        "last_name": faker.last_name(),
                                                        "subject": random.choice([option for option in SubjectEnum])})

        random_grade = random.randint(1, 5)
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)
        grade_response = grade_helper.post_grade({"teacher_id": teacher_response.json()["id"],
                                                 "student_id": student_response.json()["id"],
                                                 "grade": random_grade})

        assert grade_response.json()["teacher_id"] == teacher_response.json()["id"],\
            f"Wrong teacher id.\n"\
            f"Actual: {grade_response.json()["teacher_id"]}\n"\
            f"Expected: {teacher_response.json()["id"]}"

        assert grade_response.json()["student_id"] == student_response.json()["id"],\
            f"Wrong student id.\n"\
            f"Actual: {grade_response.json()["student_id"]}\n"\
            f"Expected: {student_response.json()["id"]}"

        assert grade_response.json()["grade"] == random_grade,\
            f"Wrong grade.\n"\
            f"Actual: {grade_response.json()['grade']}\n"\
            f"Expected: {random_grade}"
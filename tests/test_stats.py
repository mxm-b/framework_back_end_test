import random
from faker import Faker
from logger.logger import Logger
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService
from utils.assert_utils import AssertUtils


faker = Faker()

list_of_grades = [2, 5, 3]

class TestStats:
    def test_get_stats(self, university_api_utils_admin):
        Logger.info("Step #1. Create group")
        university_service = UniversityService(university_api_utils_admin)
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group)

        Logger.info("Step #2. Create student")
        student = StudentRequest(first_name=faker.first_name(),
                                 last_name=faker.last_name(),
                                 email=faker.email(),
                                 degree=random.choice([option for option in DegreeEnum]),
                                 phone=faker.numerify("+7##########"),
                                 group_id=group_response.id)
        student_response = university_service.create_student(student)

        Logger.info("Step #3. Create teacher")
        teacher = TeacherRequest(first_name=faker.first_name(),
                                 last_name=faker.last_name(),
                                 subject=random.choice([option for option in SubjectEnum]))
        teacher_response = university_service.create_teacher(teacher)

        Logger.info("Step #4. Give grades")
        for grade in list_of_grades:
            grade_request = GradeRequest(teacher_id=teacher_response.id,
                             student_id=student_response.id,
                             grade=grade)
            university_service.give_grade(grade_request)

        Logger.info("Step #5. Get stats")
        stats_response = university_service.get_stats(
            student_id=student_response.id,
            teacher_id=teacher_response.id,
            group_id=group_response.id
        )

        assert_utils = AssertUtils()
        assert_utils.assert_stats(stats_response, list_of_grades)
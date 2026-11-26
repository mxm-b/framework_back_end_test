from random import randint
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
from services.university.models.base_grade import MIN_GRADE, MAX_GRADE
from utils.soft_assert import SoftAssert

faker = Faker()

FIRST_GRADE = 2
SECOND_GRADE = 5
THIRD_GRADE = 3
LIST_OF_GRADES = [FIRST_GRADE, SECOND_GRADE, THIRD_GRADE]

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
        grade = GradeRequest(teacher_id=teacher_response.id,
                             student_id=student_response.id,
                             grade=FIRST_GRADE)
        grade_response = university_service.give_grade(grade)

        grade_2 = GradeRequest(teacher_id=teacher_response.id,
                             student_id=student_response.id,
                             grade=SECOND_GRADE)
        grade_response_2 = university_service.give_grade(grade_2)

        grade_3 = GradeRequest(teacher_id=teacher_response.id,
                             student_id=student_response.id,
                             grade=THIRD_GRADE)
        grade_response_3 = university_service.give_grade(grade_3)

        Logger.info("Step #5. Get stats")
        stats_response = university_service.get_stats(
            student_id=student_response.id,
            teacher_id=teacher_response.id,
            group_id=group_response.id
        )

        with SoftAssert() as soft:
            soft.check(stats_response.count == len(LIST_OF_GRADES),
            f"Wrong quantity.\n"
            f"Actual: {stats_response.count}\n"
            f"Expected: {len(LIST_OF_GRADES)}")

            soft.check(stats_response.avg == sum(LIST_OF_GRADES) / len(LIST_OF_GRADES),
            f"Wrong average value.\n"
            f"Actual: {stats_response.avg}\n"
            f"Expected: {sum(LIST_OF_GRADES) / len(LIST_OF_GRADES)}")

            soft.check(stats_response.min == min(LIST_OF_GRADES),
            f"Wrong min value.\n"
            f"Actual: {stats_response.min}\n"
            f"Expected: {min(LIST_OF_GRADES)}")

            soft.check(stats_response.max == max(LIST_OF_GRADES),
            f"Wrong max value.\n"
            f"Actual: {stats_response.max}\n"
            f"Expected: {max(LIST_OF_GRADES)}")
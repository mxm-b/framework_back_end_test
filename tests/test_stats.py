from random import randint
import random

from faker import Faker
from logger.logger import Logger
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.group_request import GroupRequest
from services.university.models.stats_request import StatsRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService

faker = Faker()


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
                             grade=randint(1, 5))
        grade_response = university_service.give_grade(grade)

        grade_2 = GradeRequest(teacher_id=teacher_response.id,
                             student_id=student_response.id,
                             grade=randint(1, 5))
        grade_response_2 = university_service.give_grade(grade_2)

        grade_3 = GradeRequest(teacher_id=teacher_response.id,
                             student_id=student_response.id,
                             grade=randint(1, 5))
        grade_response_3 = university_service.give_grade(grade_3)

        grades = [grade_response.grade, grade_response_2.grade, grade_response_3.grade]

        Logger.info("Step #5. Get stats")
        stats = StatsRequest(student_id=student_response.id,
                             teacher_id=teacher_response.id,
                             group_id=group_response.id)
        stats_response = university_service.get_stats(stats)

        assert stats_response.count == len(grades),\
            f"Wrong quantity.\n"\
            f"Actual: {stats_response.count}\n"\
            f"Expected: {len(grades)}"

        assert stats_response.avg == sum(grades) / len(grades),\
            f"Wrong average value.\n"\
            f"Actual: {stats_response.avg}\n"\
            f"Expected: {sum(grades) / len(grades)}"

        assert stats_response.min == min(grades),\
            f"Wrong min value.\n"\
            f"Actual: {stats_response.min}\n"\
            f"Expected: {min(grades)}"

        assert stats_response.max == max(grades),\
            f"Wrong max value.\n"\
            f"Actual: {stats_response.max}\n"\
            f"Expected: {max(grades)}"
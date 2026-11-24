from faker import Faker
import random
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

class TestStatsOfTwoStudents:
    def test_stats_of_two_students(self, university_api_utils_admin):
        Logger.info("Step 1. Create a group")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group)

        Logger.info("Step 2. Create teacher")
        teacher = TeacherRequest(first_name=faker.first_name(),
                                 last_name=faker.last_name(),
                                 subject=random.choice([choice for choice in SubjectEnum]))
        teacher_response = university_service.create_teacher(teacher)

        Logger.info("Step 3. Create student #1")
        student_1 = StudentRequest(first_name=faker.first_name(),
                                   last_name=faker.last_name(),
                                   email=faker.email(),
                                   degree=random.choice([choice for choice in DegreeEnum]),
                                   phone=faker.numerify("+7##########"),
                                   group_id=group_response.id)
        student_response_1 = university_service.create_student(student_1)

        Logger.info("Step 4. Give grade for student #1")
        grade_student_1 = GradeRequest(teacher_id=teacher_response.id,
                                       student_id=student_response_1.id,
                                       grade=random.randint(1,5))
        grade_response_student_1 = university_service.give_grade(grade_student_1)

        Logger.info("Step 5. Create student #2")
        student_2 = StudentRequest(first_name=faker.first_name(),
                                   last_name=faker.last_name(),
                                   email=faker.email(),
                                   degree=random.choice([choice for choice in DegreeEnum]),
                                   phone=faker.numerify("+7##########"),
                                   group_id=group_response.id)
        student_response_2 = university_service.create_student(student_2)

        Logger.info("Step 6. Give grade for student #2")
        grade_student_2 = GradeRequest(teacher_id=teacher_response.id,
                                       student_id=student_response_2.id,
                                       grade=random.randint(1, 5))
        grade_response_student_2 = university_service.give_grade(grade_student_2)

        Logger.info("Step 7. Get stats for student #1")
        stats_student_1 = StatsRequest(student_id=student_response_1.id,
                                       teacher_id=teacher_response.id,
                                       group_id=group_response.id)
        stats_response_student_1 = university_service.get_stats(stats_student_1)



        Logger.info("Step 8. Get stats for student #2")
        stats_student_2 = StatsRequest(student_id=student_response_2.id,
                                       teacher_id=teacher_response.id,
                                       group_id=group_response.id)
        stats_response_student_2 = university_service.get_stats(stats_student_2)

        assert stats_response_student_1.count == 1,\
            f"Wrong quantity of grades.\n"\
            f"Actual: {stats_response_student_1.count}\n"\
            f"Expected: {1}"

        assert stats_response_student_1.max == grade_response_student_1.grade,\
            f"Wrong max value.\n"\
            f"Actual: {stats_response_student_1.max}\n"\
            f"Expected: {grade_response_student_1.grade}"

        assert stats_response_student_1.min == grade_response_student_1.grade,\
            f"Wrong min value.\n"\
            f"Actual: {stats_response_student_1.min}\n"\
            f"Expected: {grade_response_student_1.grade}"

        assert stats_response_student_1.avg == grade_response_student_1.grade,\
            f"Wrong average value.\n"\
            f"Actual: {stats_response_student_1.avg}\n"\
            f"Expected: {grade_response_student_1.grade}"




        assert stats_response_student_2.count == 1, \
            f"Wrong quantity of grades.\n" \
            f"Actual: {stats_response_student_2.count}\n" \
            f"Expected: {1}"

        assert stats_response_student_2.max == grade_response_student_2.grade, \
            f"Wrong max value.\n" \
            f"Actual: {stats_response_student_2.max}\n" \
            f"Expected: {grade_response_student_2.grade}"

        assert stats_response_student_2.min == grade_response_student_2.grade, \
            f"Wrong min value.\n" \
            f"Actual: {stats_response_student_2.min}\n" \
            f"Expected: {grade_response_student_2.grade}"

        assert stats_response_student_2.avg == grade_response_student_2.grade, \
            f"Wrong average value.\n" \
            f"Actual: {stats_response_student_2.avg}\n" \
            f"Expected: {grade_response_student_2.grade}"


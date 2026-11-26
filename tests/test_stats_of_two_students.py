from faker import Faker
import random
from logger.logger import Logger
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService
from utils.soft_assert import SoftAssert

FIRST_GRADE_FOR_STUDENT_1 = 2
SECOND_GRADE_FOR_STUDENT_1 = 5
LIST_OF_GRADES_FOR_STUDENT_1 = [FIRST_GRADE_FOR_STUDENT_1, SECOND_GRADE_FOR_STUDENT_1]
FIRST_GRADE_FOR_STUDENT_2 = 1
SECOND_GRADE_FOR_STUDENT_2 = 4
LIST_OF_GRADES_FOR_STUDENT_2 = [FIRST_GRADE_FOR_STUDENT_2, SECOND_GRADE_FOR_STUDENT_2]

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

        Logger.info("Step 4. Give grade #1 for student #1")
        grade_student_1 = GradeRequest(teacher_id=teacher_response.id,
                                       student_id=student_response_1.id,
                                       grade=FIRST_GRADE_FOR_STUDENT_1)
        grade_response_student_1 = university_service.give_grade(grade_student_1)

        Logger.info("Step 5. Give grade #2 for student #1")
        grade_2_student_1 = GradeRequest(teacher_id=teacher_response.id,
                                       student_id=student_response_1.id,
                                       grade=SECOND_GRADE_FOR_STUDENT_1)
        grade_2_response_student_1 = university_service.give_grade(grade_2_student_1)

        Logger.info("Step 6. Create student #2")
        student_2 = StudentRequest(first_name=faker.first_name(),
                                   last_name=faker.last_name(),
                                   email=faker.email(),
                                   degree=random.choice([choice for choice in DegreeEnum]),
                                   phone=faker.numerify("+7##########"),
                                   group_id=group_response.id)
        student_response_2 = university_service.create_student(student_2)

        Logger.info("Step 7. Give grade #1 for student #2")
        grade_student_2 = GradeRequest(teacher_id=teacher_response.id,
                                       student_id=student_response_2.id,
                                       grade=FIRST_GRADE_FOR_STUDENT_2)
        grade_response_student_2 = university_service.give_grade(grade_student_2)

        Logger.info("Step 8. Give grade #2 for student #2")
        grade_2_student_2 = GradeRequest(teacher_id=teacher_response.id,
                                       student_id=student_response_2.id,
                                       grade=SECOND_GRADE_FOR_STUDENT_2)
        grade_response_student_2 = university_service.give_grade(grade_2_student_2)

        Logger.info("Step 9. Get stats for student #1")
        stats_response_student_1 = university_service.get_stats(
            student_id=student_response_1.id,
            teacher_id=teacher_response.id,
            group_id=group_response.id
        )

        with SoftAssert() as soft:
            soft.check(stats_response_student_1.count == len(LIST_OF_GRADES_FOR_STUDENT_1),
                f"Wrong quantity of grades.\n"
                f"Actual: {stats_response_student_1.count}\n"
                f"Expected: {len(LIST_OF_GRADES_FOR_STUDENT_1)}")

            soft.check(stats_response_student_1.max == max(LIST_OF_GRADES_FOR_STUDENT_1),
                f"Wrong max value.\n"
                f"Actual: {stats_response_student_1.max}\n"
                f"Expected: {max(LIST_OF_GRADES_FOR_STUDENT_1)}")

            soft.check(stats_response_student_1.min == min(LIST_OF_GRADES_FOR_STUDENT_1),
                f"Wrong min value.\n"
                f"Actual: {stats_response_student_1.min}\n"
                f"Expected: {min(LIST_OF_GRADES_FOR_STUDENT_1)}")

            soft.check(stats_response_student_1.avg == sum(LIST_OF_GRADES_FOR_STUDENT_1)
                / len(LIST_OF_GRADES_FOR_STUDENT_1),
                f"Wrong average value.\n"
                f"Actual: {stats_response_student_1.avg}\n"
                f"Expected: {sum(LIST_OF_GRADES_FOR_STUDENT_1) / len(LIST_OF_GRADES_FOR_STUDENT_1)}")
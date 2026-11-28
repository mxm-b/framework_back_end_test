import random

import requests
from faker import Faker

from services.university.helpers.teacher_helper import TeacherHelper
from services.university.models.base_teacher import SubjectEnum

faker = Faker()

class TestTeacherCreate:
    def test_teacher_create(self, university_api_utils_anonym):
        teacher_helper = TeacherHelper(api_utils=university_api_utils_anonym)
        teacher_response = teacher_helper.post_teacher(
            {"first_name": faker.first_name(),
             "last_name": faker.last_name(),
             "subject": random.choice([option for option in SubjectEnum])})

        assert teacher_response.status_code == requests.status_codes.codes.forbidden,\
            f"Wrong status code.\n"\
            f"Actual: {teacher_response.status_code}\n"\
            f"Expected: {requests.status_codes.codes.forbidden}"
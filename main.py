import random
from faker import Faker

from services.auth.helpers.authorization_helper import AuthorizationHelper
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.helpers.teacher_helper import TeacherHelper
from services.auth.helpers.user_helper import UserHelper
from utils.api_utils import ApiUtils
from services.university.helpers.grade_helper import GradeHelper


faker = Faker()

AUTH_URL = "http://localhost:8000"
UNIVERSITY_URL = "http://localhost:8001"

REGISTER_ENDPOINT = "/auth/register/"
LOGIN_ENDPOINT = "/auth/login/"


GROUPS_ENDPOINT = "/groups/"
STUDENTS_ENDPOINT = "/students/"
TEACHERS_ENDPOINT = "/teachers/"
GRADE_ENDPOINT = "/grades/"

username = faker.user_name()
password = faker.word() + "1Fsafds$"
email = faker.email()

authorization_helper = AuthorizationHelper(api_utils=ApiUtils(AUTH_URL))

register_response = authorization_helper.post_register(
            data = {"username": username,
            "password": password,
            "password_repeat": password,
            "email": email}
)

login_response = authorization_helper.post_login(
    data={"username": username,
          "password": password}
)


access_token = login_response.json()["access_token"]

authorization_admin_helper = AuthorizationHelper(
    api_utils=ApiUtils(AUTH_URL, headers={"Authorization": f"Bearer {access_token}"}))

group_admin_helper = GroupHelper(
    api_utils=ApiUtils(UNIVERSITY_URL, headers={"Authorization": f"Bearer {access_token}"}))
student_admin_helper = StudentHelper(
    api_utils=ApiUtils(UNIVERSITY_URL, headers={"Authorization": f"Bearer {access_token}"}))
teacher_admin_helper = TeacherHelper(
    api_utils=ApiUtils(UNIVERSITY_URL, headers={"Authorization": f"Bearer {access_token}"}))
grade_admin_helper = GradeHelper(
    api_utils=ApiUtils(UNIVERSITY_URL, headers={"Authorization": f"Bearer {access_token}"})
)

user_admin_helper = UserHelper(
    api_utils=ApiUtils(AUTH_URL, headers={"Authorization": f"Bearer {access_token}"}))

admin_university_api_utils = ApiUtils(UNIVERSITY_URL, headers={"Authorization": f"Bearer {access_token}"})

user_response = user_admin_helper.get_me()

group_response = group_admin_helper.post_group(json={"name": faker.name()})

students_response = student_admin_helper.post_student(
    json={"first_name": faker.first_name(),
          "last_name": faker.last_name(),
          "email": faker.email(),
          "degree": random.choice(["Associate",
                                   "Bachelor",
                                   "Master",
                                   "Doctorate"]),
          "phone": faker.numerify("+7##########"),
          "group_id": group_response.json()["id"]})

teachers_response = teacher_admin_helper.post_teacher(
    json={"first_name": faker.first_name(),
          "last_name": faker.last_name(),
          "subject": random.choice(["History",
                                   "Mathematics",
                                   "Physics",
                                   "Biology",
                                   "Geography"])})

grades_response = grade_admin_helper.post_grade(
    json={"teacher_id": teachers_response.json()["id"],
          "student_id": students_response.json()["id"],
          "grade": random.randint(1, 5)})
from services.general.helpers.base_helper import BaseHelper


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"
    ROOT_ENDPOINT =f"{ENDPOINT_PREFIX}/"
    STATS_ENDPOINT = f"{ROOT_ENDPOINT}stats/"


    def post_grade(self, json: dict):
        response = self.api_utils.post(self.ROOT_ENDPOINT, data=json)
        return response

    def get_grade(self, json: dict):
        response = self.api_utils.get(self.ROOT_ENDPOINT, data=json)
        return response

    def get_grade_stats(self, params: dict):
        response = self.api_utils.get(self.STATS_ENDPOINT, params=params)
        return response

    def delete_grade(self, grade_id: int):
        self.ENDPOINT = f"{self.ROOT_ENDPOINT}{grade_id}/"
        response = self.api_utils.delete(self.ENDPOINT)
        return response

    def put_grade(self, params: dict, grade_id: int):
        self.ENDPOINT = f"{self.ROOT_ENDPOINT}{grade_id}/"
        response = self.api_utils.put(self.ENDPOINT, params=params)
        return response
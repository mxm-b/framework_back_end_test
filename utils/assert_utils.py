from services.university.models.stats_response import StatsResponse
from utils.soft_assert import SoftAssert


class AssertUtils:
    def assert_stats(self, stats_response: StatsResponse, expected_grades: list[int]):
        with SoftAssert() as soft:
            soft.check(stats_response.count == len(expected_grades),
                f"Wrong quantity of grades.\n"
                f"Actual: {stats_response.count}\n"
                f"Expected: {len(expected_grades)}")

            soft.check(stats_response.max == max(expected_grades),
                f"Wrong max value.\n"
                f"Actual: {stats_response.max}\n"
                f"Expected: {max(expected_grades)}")

            soft.check(stats_response.min == min(expected_grades),
                f"Wrong min value.\n"
                f"Actual: {stats_response.min}\n"
                f"Expected: {min(expected_grades)}")

            soft.check(stats_response.avg == sum(expected_grades)
                / len(expected_grades),
                f"Wrong average value.\n"
                f"Actual: {stats_response.avg}\n"
                f"Expected: {sum(expected_grades) / len(expected_grades)}")
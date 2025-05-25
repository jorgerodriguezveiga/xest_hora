from xest_hora.optimization.aggregation import Aggregation


class FixedTeacherCalendarTaskDayTimes(Aggregation):

    _columns = ["teacher", "calendar", "task", "day", "time"]
    _indices = ["teacher", "calendar", "task", "day", "time"]
    _required_columns = ["teacher", "calendar", "task", "day", "time"]
    _default_column_values = {}
    _columns_type = {"teacher": str, "calendar": str, "task": str, "day": str, "time": str}

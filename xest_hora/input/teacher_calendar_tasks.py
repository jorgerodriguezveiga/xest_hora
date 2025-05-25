from xest_hora.aggregation import Aggregation


class TeacherCalendarTasks(Aggregation):

    _columns = ["teacher", "calendar", "task"]
    _indices = ["teacher", "calendar", "task"]
    _required_columns = ["teacher", "calendar", "task"]
    _default_column_values = {}
    _columns_type = {"teacher": str, "calendar": str, "task": str}

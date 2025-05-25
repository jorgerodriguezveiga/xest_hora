from xest_hora.optimization.aggregation import Aggregation


class Playtime(Aggregation):

    _columns = ["calendar", "day", "time"]
    _indices = ["calendar", "day", "time"]
    _required_columns = ["calendar", "day", "time"]
    _default_column_values = {}
    _columns_type = {"calendar": str, "day": str, "time": str}

    def __init__(self, name="playtime", **kwargs):
        super().__init__(**kwargs)
        self.name = name

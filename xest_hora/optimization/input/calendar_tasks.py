from xest_hora.aggregation import Aggregation
import pandas as pd


class CalendarTasks(Aggregation):

    _columns = ["calendar", "task", "min_time_periods", "max_time_periods", "max_time_period_per_day", "num_teachers"]
    _indices = ["calendar", "task"]
    _required_columns = ["calendar", "task"]
    _default_column_values = {
        "min_time_periods": 0,
        "max_time_periods": float("inf"),
        "max_time_period_per_day": float("inf"),
        "num_teachers": 1,
    }
    _columns_type = {
        "calendar": str,
        "task": str,
        "min_time_periods": int,
        "max_time_periods": float,
        "max_time_period_per_day": float,
        "num_teachers": int,
    }


default_calendar_tasks = CalendarTasks(
    pd.DataFrame(
        [
            {"calendar": "1A EP", "task": "titoría", "min_time_periods": 16, "max_time_periods": 16},
            {
                "calendar": "1A EP",
                "task": "inglés",
                "min_time_periods": 5,
                "max_time_periods": 5,
                "max_time_period_per_day": 1,
            },
            {
                "calendar": "1A EP",
                "task": "educación física",
                "min_time_periods": 4,
                "max_time_periods": 4,
                "max_time_period_per_day": 1,
            },
            {
                "calendar": "1A EP",
                "task": "plástica",
                "min_time_periods": 2,
                "max_time_periods": 2,
                "max_time_period_per_day": 1,
            },
            {
                "calendar": "1A EP",
                "task": "música",
                "min_time_periods": 2,
                "max_time_periods": 2,
                "max_time_period_per_day": 1,
            },
            {
                "calendar": "1A EP",
                "task": "relixión/valores",
                "min_time_periods": 1,
                "max_time_periods": 1,
                "max_time_period_per_day": 1,
                "num_teachers": 2,
            },
            {"calendar": "1A EP", "task": "recreo", "num_teachers": 0},
            {"calendar": "2A EP", "task": "titoría", "min_time_periods": 16, "max_time_periods": 16},
            {
                "calendar": "2A EP",
                "task": "inglés",
                "min_time_periods": 5,
                "max_time_periods": 5,
                "max_time_period_per_day": 1,
            },
            {
                "calendar": "2A EP",
                "task": "educación física",
                "min_time_periods": 4,
                "max_time_periods": 4,
                "max_time_period_per_day": 1,
            },
            {
                "calendar": "2A EP",
                "task": "plástica",
                "min_time_periods": 2,
                "max_time_periods": 2,
                "max_time_period_per_day": 1,
            },
            {
                "calendar": "2A EP",
                "task": "música",
                "min_time_periods": 2,
                "max_time_periods": 2,
                "max_time_period_per_day": 1,
            },
            {
                "calendar": "2A EP",
                "task": "relixión/valores",
                "min_time_periods": 1,
                "max_time_periods": 1,
                "max_time_period_per_day": 1,
                "num_teachers": 2,
            },
            {"calendar": "2A EP", "task": "recreo", "num_teachers": 0},
            {"calendar": "Noa Fuertes", "task": "libre disposición", "min_time_periods": 2, "max_time_periods": 2},
            {"calendar": "Noa Fuertes", "task": "garda", "min_time_periods": 2},
            {"calendar": "Noa Fuertes", "task": "coordinación", "min_time_periods": 2, "max_time_periods": 2},
            {"calendar": "Pilar Campos", "task": "libre disposición", "min_time_periods": 2, "max_time_periods": 2},
            {"calendar": "Pilar Campos", "task": "garda", "min_time_periods": 2},
            {
                "calendar": "Laura Álvarez",
                "task": "libre disposición",
                "min_time_periods": 2,
                "max_time_periods": 2,
            },
            {"calendar": "Laura Álvarez", "task": "garda", "min_time_periods": 2},
            {"calendar": "Rocío", "task": "libre disposición", "min_time_periods": 2, "max_time_periods": 2},
            {"calendar": "Rocío", "task": "garda", "min_time_periods": 2},
        ]
    )
)

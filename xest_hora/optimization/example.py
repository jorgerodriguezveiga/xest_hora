import pandas as pd
from xest_hora.input.calendar_tasks import CalendarTasks
from xest_hora.input.input_data import InputData
from xest_hora.input.playtime import Playtime
from xest_hora.input.teacher_calendar_tasks import TeacherCalendarTasks
from xest_hora.input.fixed_teacher_calendar_task_day_times import FixedTeacherCalendarTaskDayTimes


def example() -> InputData:
    classes = ["1A EP", "2A EP"]
    days = ["Luns", "Martes", "Mércores", "Xoves", "Venres"]
    times = [
        "08:55 - 09:45",
        "09:45 - 10:35",
        "10:35 - 11:25",
        "11:25 - 11:55",
        "11:55 - 12:15",
        "12:15 - 13:05",
        "13:05 - 13:55",
    ]
    playtime = Playtime(
        name="recreo",
        data=pd.DataFrame([{"calendar": c, "day": d, "time": "11:25 - 11:55"} for c in classes for d in days]),
    )
    teacher_calendar_tasks = TeacherCalendarTasks(
        pd.DataFrame(
            [
                {"teacher": "Noa Fuertes", "calendar": "1A EP", "task": "titoría"},
                {"teacher": "Noa Fuertes", "calendar": "1A EP", "task": "relixión/valores"},
                {"teacher": "Noa Fuertes", "calendar": "1A EP", "task": "educación física"},
                {"teacher": "Noa Fuertes", "calendar": "2A EP", "task": "educación física"},
                {"teacher": "Noa Fuertes", "calendar": "Noa Fuertes", "task": "garda"},
                {"teacher": "Noa Fuertes", "calendar": "Noa Fuertes", "task": "libre disposición"},
                {"teacher": "Noa Fuertes", "calendar": "Noa Fuertes", "task": "coordinación"},
                {"teacher": "Pilar Campos", "calendar": "1A EP", "task": "plástica"},
                {"teacher": "Pilar Campos", "calendar": "1A EP", "task": "música"},
                {"teacher": "Pilar Campos", "calendar": "2A EP", "task": "titoría"},
                {"teacher": "Pilar Campos", "calendar": "2A EP", "task": "plástica"},
                {"teacher": "Pilar Campos", "calendar": "2A EP", "task": "música"},
                {"teacher": "Pilar Campos", "calendar": "2A EP", "task": "relixión/valores"},
                {"teacher": "Pilar Campos", "calendar": "Pilar Campos", "task": "garda"},
                {"teacher": "Pilar Campos", "calendar": "Pilar Campos", "task": "libre disposición"},
                {"teacher": "Laura Álvarez", "calendar": "1A EP", "task": "inglés"},
                {"teacher": "Laura Álvarez", "calendar": "2A EP", "task": "inglés"},
                {"teacher": "Laura Álvarez", "calendar": "Laura Álvarez", "task": "garda"},
                {"teacher": "Laura Álvarez", "calendar": "Laura Álvarez", "task": "libre disposición"},
                {"teacher": "Rocío", "calendar": "1A EP", "task": "titoría"},
                {"teacher": "Rocío", "calendar": "2A EP", "task": "titoría"},
                {"teacher": "Rocío", "calendar": "1A EP", "task": "relixión/valores"},
                {"teacher": "Rocío", "calendar": "2A EP", "task": "relixión/valores"},
                {"teacher": "Rocío", "calendar": "Rocío", "task": "garda"},
                {"teacher": "Rocío", "calendar": "Rocío", "task": "libre disposición"},
            ]
        )
    )

    calendar_tasks = CalendarTasks(
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

    fixed_teacher_calendar_task_day_times = FixedTeacherCalendarTaskDayTimes(
        pd.DataFrame(
            [
                {
                    "teacher": "Noa Fuertes",
                    "calendar": "Noa Fuertes",
                    "task": "libre disposición",
                    "day": "Luns",
                    "time": "08:55 - 09:45",
                },
                {
                    "teacher": "Noa Fuertes",
                    "calendar": "Noa Fuertes",
                    "task": "libre disposición",
                    "day": "Venres",
                    "time": "08:55 - 09:45",
                },
                {
                    "teacher": "Noa Fuertes",
                    "calendar": "Noa Fuertes",
                    "task": "coordinación",
                    "day": "Luns",
                    "time": "13:05 - 13:55",
                },
                {
                    "teacher": "Pilar Campos",
                    "calendar": "Pilar Campos",
                    "task": "libre disposición",
                    "day": "Luns",
                    "time": "09:45 - 10:35",
                },
                {
                    "teacher": "Laura Álvarez",
                    "calendar": "Laura Álvarez",
                    "task": "libre disposición",
                    "day": "Martes",
                    "time": "08:55 - 09:45",
                },
            ]
        )
    )
    return InputData(
        classes=classes,
        days=days,
        times=times,
        playtime=playtime,
        teacher_calendar_tasks=teacher_calendar_tasks,
        calendar_tasks=calendar_tasks,
        fixed_teacher_calendar_task_day_times=fixed_teacher_calendar_task_day_times,
    )

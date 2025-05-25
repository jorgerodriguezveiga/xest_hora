from dataclasses import dataclass
import pandas as pd

from xest_hora.input.calendar_tasks import CalendarTasks
from xest_hora.input.fixed_teacher_calendar_task_day_times import FixedTeacherCalendarTaskDayTimes
from xest_hora.input.playtime import Playtime
from xest_hora.input.teacher_calendar_tasks import TeacherCalendarTasks


@dataclass
class InputData:
    classes: list[str]
    days: list[str]
    times: list[str]
    playtime: Playtime
    teacher_calendar_tasks: TeacherCalendarTasks
    calendar_tasks: CalendarTasks
    fixed_teacher_calendar_task_day_times: FixedTeacherCalendarTaskDayTimes

    @property
    def teachers(self) -> list[str]:
        return list(set(self.teacher_calendar_tasks._data["teacher"].to_list()))

    @property
    def calendars(self) -> list[str]:
        return list(set(self.calendar_tasks._data["calendar"].to_list()))

    @property
    def tasks(self) -> list[str]:
        return list(set(self.calendar_tasks._data["task"].to_list() + [self.playtime.name]))

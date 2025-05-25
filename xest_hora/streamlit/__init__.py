# Inicializar datos en session_state se é necesario
import pandas as pd
from xest_hora.streamlit.streamlit_calendar_tasks import StreamlitCalendarTasks
from xest_hora.streamlit.streamlit_calendars import StreamlitCalendars
from xest_hora.streamlit.streamlit_list import StreamlitList
from xest_hora.streamlit.streamlit_teacher_tasks import StreamlitTeacherTasks

# Classes
class_tasks = StreamlitCalendarTasks(
    "class_tasks",
    default=pd.DataFrame(
        [
            {
                "Tarefa": "titoría",
                "Nº mínimo de sesións semanais": 16,
                "Nº máximo de sesións semanais": 16,
                "Nº máximo de sesións diarias": 10,
                "Nº Profesores/as": 1,
            },
            {
                "Tarefa": "inglés",
                "Nº mínimo de sesións semanais": 5,
                "Nº máximo de sesións semanais": 5,
                "Nº máximo de sesións diarias": 1,
                "Nº Profesores/as": 1,
            },
            {
                "Tarefa": "educación física",
                "Nº mínimo de sesións semanais": 4,
                "Nº máximo de sesións semanais": 4,
                "Nº máximo de sesións diarias": 1,
                "Nº Profesores/as": 1,
            },
            {
                "Tarefa": "plástica",
                "Nº mínimo de sesións semanais": 2,
                "Nº máximo de sesións semanais": 2,
                "Nº máximo de sesións diarias": 1,
                "Nº Profesores/as": 1,
            },
            {
                "Tarefa": "música",
                "Nº mínimo de sesións semanais": 2,
                "Nº máximo de sesións semanais": 2,
                "Nº máximo de sesións diarias": 1,
                "Nº Profesores/as": 1,
            },
            {
                "Tarefa": "relixión/valores",
                "Nº mínimo de sesións semanais": 1,
                "Nº máximo de sesións semanais": 1,
                "Nº máximo de sesións diarias": 1,
                "Nº Profesores/as": 2,
            },
            {
                "Tarefa": "recreo",
                "Nº mínimo de sesións semanais": 5,
                "Nº máximo de sesións semanais": 5,
                "Nº máximo de sesións diarias": 1,
                "Nº Profesores/as": 0,
            },
            {
                "Tarefa": "hora de lectura",
                "Nº mínimo de sesións semanais": 5,
                "Nº máximo de sesións semanais": 5,
                "Nº máximo de sesións diarias": 1,
                "Nº Profesores/as": 1,
            },
        ]
    ),
)
initial_class_calendar = StreamlitCalendars(state_name="initial_class_calendar")
days = StreamlitList(state_name="days", name_to_display="Días")
times = StreamlitList(state_name="times", name_to_display="Horas")

# Teachers
teacher_tasks = StreamlitCalendarTasks(
    "teacher_tasks",
    default=pd.DataFrame(
        [
            {
                "Tarefa": "libre disposición",
                "Nº mínimo de sesións semanais": "2",
                "Nº máximo de sesións semanais": "2",
                "Nº máximo de sesións diarias": "1",
                "Nº Profesores/as": "1",
            },
            {
                "Tarefa": "recreo",
                "Nº mínimo de sesións semanais": "5",
                "Nº máximo de sesións semanais": "5",
                "Nº máximo de sesións diarias": "1",
                "Nº Profesores/as": "1",
            },
        ]
    ),
)
teacher_class_tasks = StreamlitTeacherTasks(
    "teacher_class_tasks",
    default=pd.DataFrame([{"Calendario": "", "Tarefa": ""}]),
)
initial_teacher_calendar = StreamlitCalendars(state_name="initial_teacher_calendar")

from typing import Optional
import pandas as pd
from xest_hora.streamlit.streamlit_multi_object import StreamlitMultiObject


def create_empty_calendar(dias, horas, fixed_tasks: Optional[dict[(str, str), str]] = None):
    if fixed_tasks is None:
        fixed_tasks = {}

    df = pd.DataFrame("", index=horas, columns=dias)  # Contenido vacío
    df.index.name = "Horas"
    for (hour, day), task in fixed_tasks.items():
        df.loc[hour, day] = task
    return df


class StreamlitCalendars(StreamlitMultiObject):
    pass

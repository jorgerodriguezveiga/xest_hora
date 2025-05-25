from xest_hora.streamlit.streamlit_multi_object import StreamlitMultiObject


class StreamlitCalendarTasks(StreamlitMultiObject):

    def get_calendar_tasks(self, name) -> list[str]:
        return self.elements[name]["Tarefa"].to_list()

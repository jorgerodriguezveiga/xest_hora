from xest_hora.streamlit.streamlit_multi_object import StreamlitMultiObject


class StreamlitTeacherTasks(StreamlitMultiObject):

    def get_teacher_tasks(self, name) -> list[str]:
        return self.elements[name]["Tarefa"].to_list()

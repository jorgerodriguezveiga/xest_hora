from pandas import unique
from xest_hora.aggregation import Aggregation
import plotly.graph_objects as go


class Calendar(Aggregation):

    _columns = ["day", "time", "task"]
    _indices = ["day", "time"]
    _required_columns = ["day", "time"]
    _default_column_values = {"task": ""}
    _columns_type = {"day": str, "time": str, "task": str}

    def __init__(self, days, times, name="", **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.days = days
        self.times = times

    def plot(self, width=900, height=900):
        matrix = [["" for _ in self.days] for _ in self.times]

        # Llenar las celdas con las tareas
        for _, row in self.data.iterrows():
            i = self.times.index(row["time"])
            j = self.days.index(row["day"])
            matrix[i][j] = row["task"]

        # Crear tabla con Plotly
        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(values=[""] + self.days, fill_color="lightgrey", align="center"),
                    cells=dict(
                        values=[[h for h in self.times]] + list(map(list, zip(*matrix))),
                        fill_color="white",
                        align="center",
                    ),
                )
            ]
        )

        fig.update_layout(width=width, height=height, title=self.name)
        fig.write_html(f"{self.name}.html")

import os
from typing import Literal
import streamlit as st
import pandas as pd


class StreamlitMultiObject:
    def __init__(self, state_name, default=None):
        if default is None:
            default = pd.DataFrame()

        self.state_name = state_name
        self._default = default

        self.folder = f"xest_hora/streamlit/data/{self.state_name}"
        self.load()

    def create_folder(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    @property
    def default(self) -> pd.DataFrame:
        return self._default.copy()

    @default.setter
    def default(self, value: pd.DataFrame):
        if not isinstance(value, pd.DataFrame):
            raise ValueError("Default must be a pandas DataFrame.")
        self._default = value.copy()

    @property
    def elements(self) -> dict[str, pd.DataFrame]:
        return getattr(st.session_state, self.state_name)

    @property
    def names(self) -> list[str]:
        return list(self.elements.keys())

    def create(self, name):
        self.elements[name] = self.default
        self.save_table(name)

    def delete(self, name):
        del self.elements[name]
        os.remove(f"{self.folder}/{name}.parquet")

    def edit(self, name, num_rows: Literal["dynamic", "fixed"] = "dynamic", column_config=None):
        df_editado = st.data_editor(
            self.elements[name], column_config=column_config, num_rows=num_rows, key=f"{self.state_name}_{name}"
        )
        if not df_editado.equals(self.elements[name]):
            self.elements[name] = df_editado
            self.save_table(name)
            st.rerun()

    def save_table(self, name):
        self.create_folder()
        df = self.elements[name]
        df.to_parquet(f"{self.folder}/{name}.parquet")

    def save(self):
        for name in self.names:
            self.save_table(name)

    def _create_streamlit_object(self):
        if not hasattr(st.session_state, self.state_name):
            setattr(st.session_state, self.state_name, {})

    def load_table(self, name):
        self._create_streamlit_object()
        file_path = f"{self.folder}/{name}.parquet"
        if os.path.exists(file_path):
            df = pd.read_parquet(file_path)
            self.elements[name] = df
        else:
            st.error(f"Table '{name}' not found.")

    def load(self):
        self._create_streamlit_object()
        self.create_folder()
        files = os.listdir(self.folder)
        for name in files:
            name = name.replace(".parquet", "")
            self.load_table(name)

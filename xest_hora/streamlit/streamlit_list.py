import os
import pandas as pd
import streamlit as st
from typing import Optional
import yaml


class StreamlitList:
    def __init__(self, state_name, name_to_display):
        self.state_name = state_name
        self.name_to_display = name_to_display

        self.folder = f"xest_hora/streamlit/data"
        self.load()

    def create_folder(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    @property
    def element(self) -> list:
        return getattr(st.session_state, self.state_name)

    @element.setter
    def element(self, value: list):
        return setattr(st.session_state, self.state_name, value)

    def edit(self):
        edited_df = st.data_editor(
            pd.DataFrame({self.name_to_display: self.element}), num_rows="dynamic", key=f"{self.state_name}_editor"
        )
        edited_list = edited_df[self.name_to_display].dropna().tolist()
        if set(self.element) != set(edited_list):
            self.element = edited_list
            self.save()
            st.rerun()

    def save(self):
        self.create_folder()
        yaml_path = f"{self.folder}/{self.state_name}.yaml"
        with open(yaml_path, "w") as f:
            yaml.dump(self.element, f)

    def load(self):
        file_path = f"{self.folder}/{self.state_name}.yaml"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                self.element = yaml.safe_load(f)
        else:
            st.warning(f"File {file_path} not found. You need to create it.")

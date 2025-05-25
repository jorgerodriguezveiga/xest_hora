import streamlit as st
import pandas as pd
from xest_hora.streamlit import class_tasks, initial_class_calendar, days, times
from xest_hora.streamlit.streamlit_calendars import create_empty_calendar

times.load()
days.load()
class_tasks.load()
initial_class_calendar.load()

st.set_page_config(layout="wide")

st.title("Información das Clases")
st.subheader("Horario das clases")


# --- Edición de días ---
with st.expander("📅 Editar días da semana"):
    days.edit()

# --- Edición de tramos horarios ---
with st.expander("⏰ Editar tramos horarios"):
    times.edit()

# -------------------- Crear novo calendario --------------------
st.subheader("Cursos")
with st.expander("➕ Engadir novo calendario"):
    name = st.text_input("Nome do novo calendario:")
    if st.button("Crear calendario"):
        if name:
            if name not in class_tasks.names or name not in initial_class_calendar.names:
                class_tasks.create(name)
                fixed_tasks = {}
                for day in days.element:
                    fixed_tasks[times.element[3], day] = "recreo"
                    fixed_tasks[times.element[4], day] = "hora de lectura"
                initial_class_calendar.default = create_empty_calendar(
                    days.element, times.element, fixed_tasks=fixed_tasks
                )
                initial_class_calendar.create(name)
                st.success(f"Calendario '{name}' engadido correctamente.")
            else:
                st.warning("Ese nome de calendario xa existe.")
        else:
            st.warning("Por favor, introduce un nome válido.")

# -------------------- Seleccionar calendario --------------------
calendarios = list(class_tasks.names)
if calendarios:
    calendario_seleccionado = st.selectbox("Selecciona un calendario:", sorted(calendarios))

    # Botón para borrar calendario
    with st.expander("⚠️ Xestión do calendario seleccionado"):
        if st.button("🗑️ Borrar este calendario"):
            class_tasks.delete(calendario_seleccionado)
            initial_class_calendar.delete(calendario_seleccionado)
            st.success(f"Calendario '{calendario_seleccionado}' eliminado.")
            st.rerun()  # Recargar a páxina tras borrar

    # Editor da táboa asociada ao calendario seleccionado
    st.markdown(f"### Clase {calendario_seleccionado}")
    st.markdown(f"#### Tareas")
    class_tasks.edit(name=calendario_seleccionado)

    st.markdown(f"#### Horario")
    column_config = {
        col: st.column_config.SelectboxColumn(
            label=col,
            options=class_tasks.get_calendar_tasks(calendario_seleccionado),
            help="Escolla unha tarefa ou escribe unha nova.",
        )
        for col in initial_class_calendar.elements[calendario_seleccionado].columns
    }
    initial_class_calendar.edit(name=calendario_seleccionado, num_rows="fixed", column_config=column_config)
else:
    st.info("Aínda non hai calendarios creados. Engade un para comezar.")

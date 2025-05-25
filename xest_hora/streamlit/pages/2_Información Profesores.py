import streamlit as st
from xest_hora.streamlit import teacher_class_tasks, teacher_tasks, class_tasks, initial_teacher_calendar, days, times
from xest_hora.streamlit.streamlit_calendars import create_empty_calendar

class_tasks.load()
teacher_class_tasks.load()
teacher_tasks.load()
initial_teacher_calendar.load()
days.load()
times.load()

st.title("Información das Clases")

# -------------------- Crear novo profesor --------------------
with st.expander("➕ Engadir novo profesor/a"):
    name = st.text_input("Nome do novo profesor/a:")
    if st.button("Crear profesor/a"):
        if name:
            if name not in teacher_tasks.names:
                # Crear táboa baleira para o novo profesor
                teacher_class_tasks.create(name)
                teacher_tasks.create(name)
                fixed_tasks = {}
                for day in days.element:
                    fixed_tasks[times.element[3], day] = "recreo"
                initial_teacher_calendar.default = create_empty_calendar(
                    days.element, times.element, fixed_tasks=fixed_tasks
                )
                initial_teacher_calendar.create(name)
                st.success(f"Profesor/a '{name}' engadido correctamente.")
            else:
                st.warning("Ese nome de profesor xa existe.")
        else:
            st.warning("Por favor, introduce un nome válido.")

# -------------------- Seleccionar calendario --------------------
teachers = list(teacher_tasks.names)
if teachers:
    selected_teacher = st.selectbox("Selecciona un profesor/a:", teachers)

    # Botón para borrar profesor/a
    with st.expander("⚠️ Xestión do profesor/a seleccionado"):
        if st.button("🗑️ Borrar este profesor/a"):
            teacher_tasks.delete(selected_teacher)
            teacher_class_tasks.delete(selected_teacher)
            initial_teacher_calendar.delete(selected_teacher)
            st.success(f"Profesor/a '{selected_teacher}' eliminado.")
            st.rerun()  # Recargar a páxina tras borrar

    # Editor da táboa asociada ao calendario seleccionado
    st.subheader(f"Tarefas nas clases")
    classes = list(class_tasks.names)
    tasks = sorted(set(t for df in class_tasks.elements.values() for t in df["Tarefa"].dropna()).difference("recreo"))
    column_config = {
        "Calendario": st.column_config.SelectboxColumn(label="Calendario", options=classes),
        "Tarefa": st.column_config.SelectboxColumn(label="Tarefa", options=tasks),
    }
    teacher_class_tasks.edit(selected_teacher, column_config=column_config)

    st.subheader(f"Tarefas Persoais")
    teacher_tasks.edit(selected_teacher)

    st.subheader(f"Horario")
    all_teacher_tasks = sorted(
        teacher_class_tasks.get_teacher_tasks(selected_teacher) + teacher_tasks.get_calendar_tasks(selected_teacher)
    )
    column_config = {
        col: st.column_config.SelectboxColumn(
            label=col,
            options=all_teacher_tasks,
            help="Escolla unha tarefa",
        )
        for col in initial_teacher_calendar.elements[selected_teacher].columns
    }
    initial_teacher_calendar.edit(name=selected_teacher, num_rows="fixed", column_config=column_config)
else:
    st.info("Aínda non hai profesores/as creados. Engade un para comezar.")

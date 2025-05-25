import streamlit as st
import pandas as pd

# Inicialización
if "days" not in st.session_state:
    st.session_state.days = ["Luns", "Martes", "Mércores", "Xoves", "Venres"]

if "times" not in st.session_state:
    st.session_state.times = [
        "08:55 - 09:45",
        "09:45 - 10:35",
        "10:35 - 11:25",
        "11:25 - 11:55",
        "11:55 - 12:15",
        "12:15 - 13:05",
        "13:05 - 13:55",
    ]


def crear_horario_vacio():
    return pd.DataFrame("", index=st.session_state.times, columns=st.session_state.days)


if "horarios_clases" not in st.session_state:
    st.session_state.horarios_clases = {}

# Crear nueva clase
with st.sidebar:
    st.subheader("📚 Clases")
    nova_clase = st.text_input("➕ Engadir clase")
    if st.button("Crear clase"):
        if nova_clase and nova_clase not in st.session_state.horarios_clases:
            st.session_state.horarios_clases[nova_clase] = crear_horario_vacio()
            st.success(f"Clase '{nova_clase}' creada.")
            st.rerun()

clases = list(st.session_state.horarios_clases.keys())
clase_seleccionada = st.sidebar.selectbox("Selecciona unha clase:", clases) if clases else None

# Mostrar editor si hay clase seleccionada
if clase_seleccionada:
    st.subheader(f"✏️ Horario da clase: {clase_seleccionada}")
    horario_original = st.session_state.horarios_clases[clase_seleccionada]

    # Cargar tabla editable al estado si no existe
    if f"horario_editado_{clase_seleccionada}" not in st.session_state:
        st.session_state[f"horario_editado_{clase_seleccionada}"] = horario_original.copy()

    horario_editado = st.session_state[f"horario_editado_{clase_seleccionada}"]

    materias = ["", "Matemáticas", "Física", "Lingua", "Historia", "Recreo"]
    column_config = {
        col: st.column_config.SelectboxColumn(label=col, options=materias) for col in horario_editado.columns
    }

    tabla = st.data_editor(
        horario_editado, column_config=column_config, use_container_width=True, key=f"editor_{clase_seleccionada}"
    )

    # Guardar con botón
    if st.button("💾 Gardar cambios"):
        st.session_state.horarios_clases[clase_seleccionada] = tabla.copy()
        st.session_state[f"horario_editado_{clase_seleccionada}"] = tabla.copy()
        st.success("Cambios gardados.")
        st.rerun()

import streamlit as st

st.set_page_config(page_title="Xestor de Datos", page_icon="📊", layout="wide")

# -------------------- Cabeceira --------------------
st.title("📊 Xestor de Horarios Escolares")
st.markdown("### Benvido/a á túa plataforma para a creación de horarios escolares")

# -------------------- Introdución --------------------
st.markdown(
    """
Esta aplicación está deseñada para axudar a creación dos horarios escolares tendo en conta a **normativa do centro** e as **prioridades do profesorado**.

---

### 🔧 Cómo funciona?

#### 📚 Información Clases
- Introduce a información das clases.

#### 🧑‍🏫 Información Profesores
- Introduce a información dos profesores.

---

### 🗓️ Calendarios
- Obtén os calendarios e modifícaos ata chegar a unha solución que che convenza.
"""
)

st.markdown("---")
st.caption("Desenvolvido con ❤️ por Noa Fuertes Opazo e Jorge Rodríguez Veiga · Versión 0.1")

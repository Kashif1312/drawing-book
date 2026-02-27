import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="Drawing Book", layout="wide")

st.title("🎨 My Drawing Book")

# ===============================
# Sidebar - Dashboard 1
# ===============================
st.sidebar.header("🛠 Dashboard")

clear = st.sidebar.button("Clear Canvas")

uploaded_image = st.sidebar.file_uploader(
    "Insert Image", type=["png", "jpg", "jpeg"]
)

uploaded_sticker = st.sidebar.file_uploader(
    "Insert Sticker (PNG with transparency)", type=["png"]
)

# ===============================
# Sidebar - Drawing Tools
# ===============================
st.sidebar.header("✏️ Drawing Tools")

drawing_mode = st.sidebar.selectbox(
    "Select Tool",
    ("freedraw", "line", "rect", "circle")
)

pencil_size = st.sidebar.radio(
    "Pencil Size",
    ("Simple", "Bold", "Extra Bold")
)

stroke_width = {
    "Simple": 3,
    "Bold": 7,
    "Extra Bold": 12
}[pencil_size]

stroke_color = st.sidebar.color_picker("Pick Color", "#000000")

# ===============================
# Canvas Background Setup
# ===============================
if "background" not in st.session_state or clear:
    st.session_state.background = Image.new("RGB", (800, 500), "white")

# Insert Image
if uploaded_image is not None:
    img = Image.open(uploaded_image).convert("RGB")
    img = img.resize((200, 200))
    st.session_state.background.paste(img, (50, 50))
    uploaded_image = None

# Insert Sticker
if uploaded_sticker is not None:
    sticker = Image.open(uploaded_sticker).convert("RGBA")
    sticker = sticker.resize((120, 120))
    st.session_state.background.paste(sticker, (300, 200), sticker)
    uploaded_sticker = None

# ===============================
# Drawing Canvas
# ===============================
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_image=st.session_state.background,
    update_streamlit=True,
    height=500,
    width=800,
    drawing_mode=drawing_mode,
    key="canvas",
)

# ===============================
# Save Drawing
# ===============================
st.sidebar.header("💾 Save Drawing")

if canvas_result.image_data is not None:
    final_image = Image.fromarray(
        canvas_result.image_data.astype("uint8")
    )

    buffer = io.BytesIO()
    final_image.save(buffer, format="PNG")

    st.sidebar.download_button(
        label="Download as PNG",
        data=buffer.getvalue(),
        file_name="drawing.png",
        mime="image/png"
    )

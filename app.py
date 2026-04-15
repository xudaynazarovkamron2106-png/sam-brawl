import streamlit as st
import random

st.set_page_config(page_title="GeminGPT-Pro Image", page_icon="🎨")

st.markdown("<h1 style='text-align: center; color: #00d4ff;'>GeminGPT PRO IMAGE</h1>", unsafe_allow_html=True)

query = st.text_input("Nima chizamiz?", placeholder="Masalan: Futuristic city...")

if st.button("YARATISH ✨", use_container_width=True):
    if query:
        with st.spinner("KGO Engine rasm yaratmoqda..."):
            seed = random.randint(1, 999999)
            # Eng tezkor va iPad-da ishlaydigan link
            img_url = f"https://image.pollinations.ai/prompt/{query.replace(' ', '%20')}?seed={seed}&width=1024&height=1024&nologo=true"
            st.image(img_url, caption="KGO Group Natijasi", use_container_width=True)
            st.success("Tayyor!")
    else:
        st.warning("Tavsif yozing!")

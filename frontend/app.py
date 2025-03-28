import streamlit as st
import requests
import re
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/brightest_color")

st.title("Hex Color to Brightness")

color_input = st.text_area("Enter a list of colors (comma-separated)", "#AABBCC, #154331, #A0B1C2, #000000, #FFFFFF")

if st.button("Find Brightest Color"):
    color_list = []
    for hex_color in color_input.split(","):
        hex_color = hex_color.strip()
        if not hex_color.startswith("#"):
            st.error(f'Invalid hex color "{hex_color}"! Must start with "#".')
        if len(hex_color) != 7:
            st.error(f'Invalid hex color "{hex_color}"! Must be 7 characters long including "#".')
        if not re.match(r"^#[A-Fa-f0-9]{6}$", hex_color):
            st.error(f'Invalid hex color "{hex_color}"! Allowed characters after "#": 0-9, A-F, a-f.')

        if re.fullmatch(r"^#([A-Fa-f0-9]{6})$", hex_color):
            color_list.append(hex_color)

    response = requests.post(API_URL, json={"colors": color_list})

    if response.status_code == 200:
        result = response.json()["brightest_color"]
        st.success(f"The brightest color is: {result}")
        st.markdown(f'<div style="background-color:{result}; width:100px; height:100px;"></div>', unsafe_allow_html=True)
    else:
        st.error("Error in API request")



import streamlit as st
from pipeline import pipeline


def main():
    "Initialize the frontend with streamlit."
    st.title("Parquet File Validation")

    def on_button_click():
        pipeline()

    if st.button("Run Transformation"):
        on_button_click()


if __name__ == "__main__":
    main()

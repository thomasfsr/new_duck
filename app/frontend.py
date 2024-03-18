import streamlit as st
from transform import validation

def main():
    st.title("Parquet File Validation")

    def on_button_click():
        result = validation('data')
        st.write("Files passed on the validation:", result)

    if st.button("Run Transformation"):
        on_button_click()

if __name__ == "__main__":
    main()

import streamlit as st

      
st.markdown("# Customer Review Analyzier Page  ⭐")
st.sidebar.markdown("# Customer Review Analyzier Page  ⭐")

st.header("📝 Customer Review Analyzer")

# Pilihan input dengan selectbox
option = st.selectbox(
        "Pilih sumber review:",
        ["Pilih...", "Link", "Foto"]
)

if option == "Link":
    st.subheader("Input Review dari Link")
    url = st.text_input("Masukkan URL review:")
    if url:
        st.success(f"URL dimasukkan: {url}")

elif option == "Foto":
    st.subheader("Input Review dari Foto")
    uploaded_file = st.file_uploader("Upload screenshot review", type=["jpg", "png"])
    if uploaded_file:
        st.success("Foto berhasil diupload ✅")

else:
    st.info("Silakan pilih sumber review di atas")


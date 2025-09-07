import streamlit as st
from PIL import Image
from compress_image import compress_image
import io


st.set_page_config(page_title="K-Means Image Compressor",  page_icon="🗜️" )
st.write("## K-Means Image Compressor  🎨🗜️")
st.write("Upload an image and choose the number of colors for the compressed version. "
         "The K-Means algorithm will reduce the color palette of your image.")
st.sidebar.write("## Upload Images")

uploaded_file = st.sidebar.file_uploader("Choose an image to continue", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    original_image = Image.open(uploaded_file).convert("RGB")

    num_colors = st.sidebar.slider("Number of Colors", min_value=2, max_value=50, value=12, step=1)

    if st.sidebar.button("Compress Image"):
        with st.spinner("Compressing..."):
            compressed_image = compress_image(original_image, num_colors)

        # Display original and compressed images side by side
        col1, col2 = st.columns(2)
        with col1:
            st.image(original_image, caption="Original Image",use_container_width=True)
        with col2:
            st.image(compressed_image, caption=f"Compressed Image ({num_colors} colors)",use_container_width=True)

        # Download compressed Image
        buf = io.BytesIO()
        compressed_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="Download Compressed Image",
            data=byte_im,
            file_name=f"compressed_{uploaded_file.name}",
            mime="image/png",
        )

        # Get and display original and compressed file sizes
        file_size = uploaded_file.size  
        st.write(f"Uploaded file size: {file_size / 1024:.2f} KB")
        compressed_size = buf.getbuffer().nbytes 
        st.write(f"Compressed image size: {compressed_size / 1024:.2f} KB")


else:
    st.info("Please upload an image file to get started.")


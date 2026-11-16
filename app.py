import io
import streamlit as st
from google import genai
from google.genai import types


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="PixelForge AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main page */
    .stApp {
        background:
            radial-gradient(circle at top left, #17172b 0%, #0b0b12 40%, #07070b 100%);
        color: white;
    }

    /* Remove default top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1200px;
    }

    /* Header */
    .hero {
        text-align: center;
        padding: 30px 10px 20px 10px;
    }

    .hero-title {
        font-size: 48px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 8px;
        background: linear-gradient(
            90deg,
            #ffffff,
            #b9a7ff,
            #8fdcff
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #a9a9b8;
        font-size: 18px;
        margin-bottom: 10px;
    }

    /* Cards */
    .card {
        background: rgba(20, 20, 31, 0.88);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25);
    }

    .card-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .small-text {
        color: #9999aa;
        font-size: 14px;
    }

    /* Text area */
    textarea {
        background-color: #11111a !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #303040 !important;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        height: 52px;
        border-radius: 12px;
        border: none;
        font-size: 16px;
        font-weight: 700;
        background: linear-gradient(
            90deg,
            #7c5cff,
            #4ca9ff
        );
        color: white;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(100, 120, 255, 0.30);
    }

    /* Download button */
    .stDownloadButton > button {
        width: 100%;
        height: 48px;
        border-radius: 10px;
        font-weight: 600;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0d0d14;
        border-right: 1px solid #252532;
    }

    /* Image */
    [data-testid="stImage"] img {
        border-radius: 16px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #777785;
        font-size: 13px;
        padding-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "generated_image" not in st.session_state:
    st.session_state.generated_image = None

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🎨 PixelForge AI")

    st.markdown(
        """
        <div class="small-text">
        Transform your ideas into AI-generated images.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### ⚙️ Generation Settings")

    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        options=[
            "1:1",
            "16:9",
            "9:16",
            "4:3",
            "3:4"
        ],
        index=0
    )

    image_size = st.selectbox(
        "Image Resolution",
        options=[
            "1K",
            "2K"
        ],
        index=0
    )

    st.divider()

    st.markdown("### 💡 Prompt Tips")

    st.markdown(
        """
        **Describe:**
        
        • Subject  
        • Environment  
        • Lighting  
        • Camera angle  
        • Art style  
        • Mood  
        • Colors
        
        **Example:**
        
        `A futuristic city at sunset, cinematic lighting, 
        flying cars, ultra detailed, realistic photography`
        """
    )

    st.divider()

    st.caption("Powered by Google Gemini")


# =========================================================
# HERO SECTION
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">PixelForge AI</div>
        <div class="hero-subtitle">
            Turn your imagination into stunning AI-generated images.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MAIN LAYOUT
# =========================================================

left_column, right_column = st.columns(
    [1, 1],
    gap="large"
)


# =========================================================
# PROMPT SECTION
# =========================================================

with left_column:

    st.markdown(
        """
        <div class="card">
            <div class="card-title">✨ Create Your Image</div>
        """,
        unsafe_allow_html=True
    )

    prompt = st.text_area(
        "Image Prompt",
        height=190,
        placeholder=(
            "Describe the image you want...\n\n"
            "Example: A beautiful futuristic city at sunset, "
            "cinematic lighting, glowing skyscrapers, flying cars, "
            "ultra detailed, photorealistic."
        ),
        label_visibility="collapsed"
    )

    st.markdown(
        """
        <div class="small-text">
        Be specific for better results. Describe the subject,
        environment, lighting, style and mood.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    generate_button = st.button(
        "🚀 Generate Image",
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# RESULT SECTION
# =========================================================

with right_column:

    st.markdown(
        """
        <div class="card">
            <div class="card-title">🖼️ Generated Image</div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.generated_image is not None:

        st.image(
            st.session_state.generated_image,
            use_container_width=True
        )

        # Prepare image for download
        image_bytes = io.BytesIO()

        st.session_state.generated_image.save(
            image_bytes,
            format="PNG"
        )

        image_bytes.seek(0)

        st.download_button(
            label="⬇️ Download Image",
            data=image_bytes,
            file_name="pixelforge_ai_image.png",
            mime="image/png",
            use_container_width=True
        )

    else:

        st.markdown(
            """
            <div style="
                height: 380px;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                color: #777785;
                border: 1px dashed #303040;
                border-radius: 15px;
                background: rgba(10,10,16,0.5);
            ">
                <div>
                    <div style="font-size: 55px;">🎨</div>
                    <div style="font-size: 18px; font-weight: 600;">
                        Your generated image will appear here
                    </div>
                    <div style="font-size: 14px; margin-top: 8px;">
                        Enter a prompt and click Generate Image
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# IMAGE GENERATION
# =========================================================

if generate_button:

    if not prompt.strip():

        st.warning("⚠️ Please enter a prompt first.")

    else:

        try:

            # Get API key from Streamlit Secrets
            api_key = st.secrets["GEMINI_API_KEY"]

            # Create Gemini client
            client = genai.Client(
                api_key=api_key
            )

            st.session_state.last_prompt = prompt

            with st.spinner("🎨 Creating your image..."):

                response = client.models.generate_content(
                    model="gemini-3.1-flash-image",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                        image_config=types.ImageConfig(
                            aspect_ratio=aspect_ratio,
                            image_size=image_size
                        )
                    )
                )

                generated_image = None

                # Find image returned by Gemini
                for part in response.parts:

                    if part.inline_data is not None:

                        generated_image = part.as_image()
                        break

                if generated_image is None:

                    st.error(
                        "❌ Gemini did not return an image. "
                        "Please try another prompt."
                    )

                else:

                    st.session_state.generated_image = generated_image

                    st.success(
                        "✅ Your image has been generated!"
                    )

                    # Rerun so the generated image appears
                    # in the result section
                    st.rerun()

        except KeyError:

            st.error(
                "❌ GEMINI_API_KEY is missing from Streamlit Secrets."
            )

            st.info(
                "Add GEMINI_API_KEY to your Streamlit Secrets."
            )

        except Exception as e:

            st.error(
                "❌ Image generation failed."
            )

            st.code(str(e))


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        PixelForge AI • Text-to-Image Generator • Powered by Gemini
    </div>
    """,
    unsafe_allow_html=True
)

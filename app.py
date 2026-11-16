
import streamlit as st
import requests
import base64
import io
from PIL import Image

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="PixelForge AI | Image Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PROFESSIONAL UI
# =====================================================

st.markdown("""
<style>
.stApp {
    background: #0b0b14;
    color: #ffffff;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    text-align: center;
    padding: 25px 10px 35px;
}

.hero h1 {
    font-size: 48px;
    font-weight: 850;
    background: linear-gradient(90deg,#ffffff,#a78bfa,#60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #a1a1b5;
    font-size: 17px;
}

section[data-testid="stSidebar"] {
    background: #11111d;
    border-right: 1px solid #28283a;
}

.panel {
    background: #151522;
    border: 1px solid #29293b;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 15px;
}

.panel-title {
    font-size: 21px;
    font-weight: 750;
    margin-bottom: 15px;
    color: #ffffff;
}

.stTextArea textarea {
    background: #10101b !important;
    color: white !important;
    border: 1px solid #343449 !important;
    border-radius: 12px !important;
}

.stButton > button {
    width: 100%;
    height: 52px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(90deg,#7c3aed,#2563eb);
    color: white;
    font-weight: 750;
    font-size: 16px;
}

.stButton > button:hover {
    border: 1px solid #a78bfa;
    color: white;
}

.stDownloadButton > button {
    width: 100%;
    height: 48px;
    border-radius: 11px;
    font-weight: 700;
}

[data-testid="stImage"] img {
    border-radius: 15px;
}

.hint {
    color: #9999ad;
    font-size: 13px;
}

.footer {
    text-align: center;
    color: #77778d;
    padding-top: 35px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# SESSION STATE
# =====================================================

if "generated_image" not in st.session_state:
    st.session_state.generated_image = None

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## 🎨 PixelForge AI")

    st.caption("AI-powered Text to Image Generator")

    st.divider()

    st.markdown("### ⚙️ Generation Settings")

    steps = st.slider(
        "Generation Steps",
        min_value=1,
        max_value=8,
        value=4,
        help="Higher steps may improve quality but can use more resources."
    )

    st.divider()

    st.markdown("### 💡 Prompt Guide")

    st.markdown("""
    Include these details in your prompt:

    - **Subject:** What should appear?
    - **Environment:** Where is it?
    - **Lighting:** Bright, soft or cinematic?
    - **Style:** Realistic, 3D or illustration?
    - **Colors:** Which colors should dominate?
    - **Mood:** What feeling should the image have?
    """)

    st.divider()

    st.caption("Model: FLUX.1 Schnell")
    st.caption("Provider: Cloudflare Workers AI")


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="hero">
    <h1>PixelForge AI</h1>
    <p>
        Transform your imagination into stunning AI-generated images.
        <br>
        Write a prompt, generate your image and download it.
    </p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# MAIN COLUMNS
# =====================================================

left, right = st.columns([1, 1], gap="large")


# =====================================================
# PROMPT INPUT
# =====================================================

with left:

    st.markdown("""
    <div class="panel">
        <div class="panel-title">✨ Create Your Image</div>
    """, unsafe_allow_html=True)

    prompt = st.text_area(
        "Describe your image",
        placeholder=(
            "Example: A beautiful futuristic city at sunset, "
            "glowing skyscrapers, cinematic lighting, "
            "realistic photography, ultra detailed..."
        ),
        height=210,
        max_chars=2048
    )

    st.markdown("""
    <p class="hint">
    Write a detailed description to get better image results.
    Maximum prompt length: 2048 characters.
    </p>
    """, unsafe_allow_html=True)

    generate = st.button(
        "🚀 Generate Image",
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# IMAGE GENERATION FUNCTION
# =====================================================

def generate_image(prompt_text, generation_steps):

    account_id = st.secrets["CLOUDFLARE_ACCOUNT_ID"]
    api_token = st.secrets["CLOUDFLARE_API_TOKEN"]

    model = "@cf/black-forest-labs/flux-1-schnell"

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/ai/run/{model}"
    )

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt_text,
        "steps": generation_steps
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=180
    )

    if not response.ok:
        try:
            error_data = response.json()
            raise RuntimeError(str(error_data))
        except ValueError:
            response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")

    if "image/" in content_type:
        image_bytes = response.content
    else:
        result = response.json()

        if not result.get("success", True):
            raise RuntimeError(str(result.get("errors", result)))

        image_base64 = result.get("result", {}).get("image")

        if not image_base64:
            raise RuntimeError(
                "The API did not return an image. Please try again."
            )

        image_bytes = base64.b64decode(image_base64)

    image = Image.open(io.BytesIO(image_bytes))
    image.load()

    return image.convert("RGB")


# =====================================================
# GENERATE IMAGE
# =====================================================

if generate:

    if not prompt.strip():
        st.warning("Please enter an image description first.")

    elif len(prompt.strip()) > 2048:
        st.warning("Your prompt must be 2048 characters or less.")

    else:

        try:
            with st.spinner(
                "🎨 FLUX AI is creating your image... Please wait."
            ):

                image = generate_image(
                    prompt.strip(),
                    steps
                )

                st.session_state.generated_image = image
                st.session_state.last_prompt = prompt.strip()

            st.success("Your image was generated successfully!")

        except KeyError as e:
            st.error("API credentials are missing from Streamlit Secrets.")
            st.code(str(e))

        except requests.exceptions.Timeout:
            st.error("The generation request timed out. Please try again.")

        except requests.exceptions.RequestException as e:
            st.error("Cloudflare API connection failed.")
            st.code(str(e))

        except Exception as e:
            st.error("Image generation failed.")
            st.code(str(e))


# =====================================================
# GENERATED IMAGE PREVIEW
# =====================================================

with right:

    st.markdown("""
    <div class="panel">
        <div class="panel-title">🖼️ Your Generated Image</div>
    """, unsafe_allow_html=True)

    if st.session_state.generated_image is not None:

        image = st.session_state.generated_image

        st.image(
            image,
            use_container_width=True
        )

        image_buffer = io.BytesIO()
        image.save(image_buffer, format="PNG")
        image_buffer.seek(0)

        st.download_button(
            label="⬇️ Download Image",
            data=image_buffer,
            file_name="pixelforge_generated_image.png",
            mime="image/png",
            use_container_width=True
        )

        st.caption(
            "Prompt: " + st.session_state.last_prompt
        )

    else:

        st.markdown("""
        <div style="
            height: 380px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            border: 1px dashed #41415a;
            border-radius: 14px;
            background: #10101a;
            color: #9999ad;
        ">
            <div>
                <div style="font-size: 65px;">🎨</div>
                <h3 style="color:white;">
                    Your image will appear here
                </h3>
                <p>Enter a prompt and click Generate Image.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">
    PixelForge AI | Powered by FLUX.1 Schnell
    <br>
    Built with Python and Streamlit
</div>
""", unsafe_allow_html=True)

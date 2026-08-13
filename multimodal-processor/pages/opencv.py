import streamlit as st
import cv2
import numpy as np
from PIL import Image
import spacy
from nltk.tokenize import word_tokenize
import json
import datetime
import db

# Lazy-loaded SpaCy model to improve dashboard startup speeds
_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback if model download was interrupted
            spacy.cli.download("en_core_web_sm")
            _nlp = spacy.load("en_core_web_sm")
    return _nlp

def add_to_history(mode, action, input_data, output_data):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    inp_short = str(input_data)[:60] + "..." if len(str(input_data)) > 60 else str(input_data)
    out_short = str(output_data)[:80] + "..." if len(str(output_data)) > 80 else str(output_data)
    
    # Get logged-in user email if available
    user_email = None
    if "user" in st.session_state and st.session_state.user:
        user_email = st.session_state.user.get("email")
        
    # Avoid duplicate writes for identical actions on re-runs
    if st.session_state.history:
        last = st.session_state.history[-1]
        if last["action"] == action and last["input"] == inp_short:
            return
            
    st.session_state.history.append({
        "timestamp": now,
        "mode": mode,
        "action": action,
        "input": inp_short,
        "output": out_short,
        "email": user_email
    })
    db.add_to_history_db(mode, action, inp_short, out_short, user_email)

def set_action(action_name):
    st.session_state.action = action_name

def render_opencv_page():
    st.markdown('<div class="main-title">✨ Multimodal Processor UI ✨</div>', unsafe_allow_html=True)

    # Input modes selector
    tabs = st.tabs(["📄 Input Text Mode", "🖼️ Image (OpenCV)"])
    
    # 1. Text Mode tab
    with tabs[0]:
        st.markdown('<div class="action-grid-title" style="text-align: left; margin-bottom: 0.5rem;">Mode Mode</div>', unsafe_allow_html=True)
        user_text = st.text_area(
            "Enter text here",
            value="SpaCy is an amazing library for NLP.",
            height=180,
            placeholder="Type or paste text to analyze...",
            label_visibility="collapsed",
            key="opencv_text_input"
        )
        
    # 2. Image Mode tab
    with tabs[1]:
        def on_image_upload_change():
            uploaded_file = st.session_state.opencv_image_upload
            if uploaded_file is not None:
                try:
                    st.session_state.uploaded_image = Image.open(uploaded_file).convert("RGB")
                except Exception as e:
                    st.session_state.uploaded_image = None
            else:
                st.session_state.uploaded_image = None

        st.file_uploader(
            "Upload an image",
            type=["png", "jpg", "jpeg"],
            key="opencv_image_upload",
            label_visibility="collapsed",
            on_change=on_image_upload_change
        )
        
        # Load sample image or uploaded image from session state
        if st.session_state.get("uploaded_image") is not None:
            input_image = st.session_state.uploaded_image
            st.markdown('<div class="preview-card">', unsafe_allow_html=True)
            st.image(input_image, caption="Uploaded Image Preview", use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            import os
            try:
                current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                camera_img_path = os.path.join(current_dir, "default_camera.png")
                input_image = Image.open(camera_img_path).convert("RGB")
                st.markdown('<div class="preview-card">', unsafe_allow_html=True)
                st.image(input_image, caption="Default Image Preview (Nikon Camera)", use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.warning("⚠️ No image uploaded and default_camera.png not found. Please upload an image.")
                input_image = None

    # Actions Section
    st.markdown('<div class="action-grid-title">Select an Action</div>', unsafe_allow_html=True)
    
    # Row 1 and Row 2 Columns
    row1_cols = st.columns(4)
    row2_cols = st.columns(4)
    
    selected_action = st.session_state.action
    
    # Button 1: Extract Entities (Blue gradient)
    with row1_cols[0]:
        is_active = (selected_action == "entities")
        active_class = "btn-active-glow" if is_active else ""
        st.markdown(f'<div class="action-marker btn-grad-blue {active_class}"></div>', unsafe_allow_html=True)
        st.button("Extract Entities", key="act_entities", use_container_width=True, on_click=set_action, args=("entities",))
        
    # Button 2: POS Tagging (Purple/Pink gradient)
    with row1_cols[1]:
        is_active = (selected_action == "pos")
        active_class = "btn-active-glow" if is_active else ""
        st.markdown(f'<div class="action-marker btn-grad-pink {active_class}"></div>', unsafe_allow_html=True)
        st.button("POS Tagging", key="act_pos", use_container_width=True, on_click=set_action, args=("pos",))

    # Button 3: Extract Noun Chunks (Green gradient)
    with row1_cols[2]:
        is_active = (selected_action == "noun_chunks")
        active_class = "btn-active-glow" if is_active else ""
        st.markdown(f'<div class="action-marker btn-grad-green {active_class}"></div>', unsafe_allow_html=True)
        st.button("Extract Noun Chunks", key="act_noun_chunks", use_container_width=True, on_click=set_action, args=("noun_chunks",))

    # Button 4: Tokenize Words (Indigo/Purple gradient)
    with row1_cols[3]:
        is_active = (selected_action == "tokenize")
        active_class = "btn-active-glow" if is_active else ""
        st.markdown(f'<div class="action-marker btn-grad-indigo {active_class}"></div>', unsafe_allow_html=True)
        st.button("Tokenize Words", key="act_tokenize", use_container_width=True, on_click=set_action, args=("tokenize",))

    # Button 5: Convert Grayscale (Teal gradient)
    with row2_cols[0]:
        is_active = (selected_action == "grayscale")
        active_class = "btn-active-glow" if is_active else ""
        st.markdown(f'<div class="action-marker btn-grad-teal {active_class}"></div>', unsafe_allow_html=True)
        st.button("Convert Grayscale", key="act_grayscale", use_container_width=True, on_click=set_action, args=("grayscale",))

    # Button 6: Edge Detection (Orange/Red gradient)
    with row2_cols[1]:
        is_active = (selected_action == "edges")
        active_class = "btn-active-glow" if is_active else ""
        st.markdown(f'<div class="action-marker btn-grad-orange {active_class}"></div>', unsafe_allow_html=True)
        st.button("Edge Detection", key="act_edges", use_container_width=True, on_click=set_action, args=("edges",))

    # Button 7: Gaussian Blur (Purple/Violet gradient)
    with row2_cols[2]:
        is_active = (selected_action == "blur")
        active_class = "btn-active-glow" if is_active else ""
        st.markdown(f'<div class="action-marker btn-grad-purple {active_class}"></div>', unsafe_allow_html=True)
        st.button("Gaussian Blur", key="act_blur", use_container_width=True, on_click=set_action, args=("blur",))

    # Button 8: Invert Colors (Red/Orange gradient)
    with row2_cols[3]:
        is_active = (selected_action == "invert")
        active_class = "btn-active-glow" if is_active else ""
        st.markdown(f'<div class="action-marker btn-grad-red {active_class}"></div>', unsafe_allow_html=True)
        st.button("Invert Colors", key="act_invert", use_container_width=True, on_click=set_action, args=("invert",))

    # Output Section
    st.markdown('<div class="output-title">Output Result</div>', unsafe_allow_html=True)
    
    selected_action = st.session_state.action
    text_actions = {"entities", "pos", "noun_chunks", "tokenize"}
    image_actions = {"grayscale", "edges", "blur", "invert"}
    
    if selected_action in text_actions:
        user_text = st.session_state.get("opencv_text_input", "SpaCy is an amazing library for NLP.")
        if not user_text or user_text.strip() == "":
            st.warning("⚠️ Text input is empty! Please write some text inside 'Input Text Mode' to run the operation.")
        else:
            try:
                nlp_obj = get_nlp()
                if selected_action == "entities":
                    doc = nlp_obj(user_text)
                    orgs = {}
                    others = {}
                    for ent in doc.ents:
                        if ent.label_ in ["ORG", "PRODUCT", "WORK_OF_ART", "GPE"]:
                            orgs[ent.text] = ent.label_
                        else:
                            others[ent.text] = ent.label_
                    
                    res = {
                        "SpaCy": {
                            "result": {
                                "organizations": orgs
                            }
                        }
                    }
                    if others:
                        res["SpaCy"]["result"]["other_entities"] = others
                    
                    formatted_json = json.dumps(res, indent=4)
                    html_content = f"""
                    <div class="output-card">
                        <div style="font-weight: 600; margin-bottom: 0.75rem; color: #cbd5e1;">Extract Entities Result</div>
                        <pre class="output-code">{formatted_json}</pre>
                    </div>
                    """
                    st.markdown(html_content, unsafe_allow_html=True)
                    add_to_history("Text", "Extract Entities", user_text, formatted_json)
                    
                elif selected_action == "pos":
                    doc = nlp_obj(user_text)
                    res = {
                        "SpaCy": {
                            "result": {
                                "pos_tags": {token.text: token.pos_ for token in doc}
                            }
                        }
                    }
                    formatted_json = json.dumps(res, indent=4)
                    html_content = f"""
                    <div class="output-card">
                        <div style="font-weight: 600; margin-bottom: 0.75rem; color: #cbd5e1;">POS Tagging Result</div>
                        <pre class="output-code">{formatted_json}</pre>
                    </div>
                    """
                    st.markdown(html_content, unsafe_allow_html=True)
                    add_to_history("Text", "POS Tagging", user_text, formatted_json)
                    
                elif selected_action == "noun_chunks":
                    doc = nlp_obj(user_text)
                    chunks = [chunk.text for chunk in doc.noun_chunks]
                    res = {
                        "SpaCy": {
                            "result": {
                                "noun_chunks": chunks
                            }
                        }
                    }
                    formatted_json = json.dumps(res, indent=4)
                    html_content = f"""
                    <div class="output-card">
                        <div style="font-weight: 600; margin-bottom: 0.75rem; color: #cbd5e1;">Extract Noun Chunks Result</div>
                        <pre class="output-code">{formatted_json}</pre>
                    </div>
                    """
                    st.markdown(html_content, unsafe_allow_html=True)
                    add_to_history("Text", "Extract Noun Chunks", user_text, formatted_json)
                    
                elif selected_action == "tokenize":
                    tokens = word_tokenize(user_text)
                    res = {
                        "NLTK": {
                            "result": {
                                "tokens": tokens,
                                "count": len(tokens)
                            }
                        }
                    }
                    formatted_json = json.dumps(res, indent=4)
                    html_content = f"""
                    <div class="output-card">
                        <div style="font-weight: 600; margin-bottom: 0.75rem; color: #cbd5e1;">Tokenize Words Result</div>
                        <pre class="output-code">{formatted_json}</pre>
                    </div>
                    """
                    st.markdown(html_content, unsafe_allow_html=True)
                    add_to_history("Text", "Tokenize Words", user_text, formatted_json)
            except Exception as e:
                st.error(f"❌ Error during text analysis: {e}")
            
    elif selected_action in image_actions:
        if input_image is None:
            st.warning("⚠️ No image available! Please upload an image in 'Image (OpenCV)' tab to run the operation.")
        else:
            try:
                img_array = np.array(input_image)
                
                if selected_action == "grayscale":
                    output = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                    st.markdown("##### Grayscale Result")
                    st.markdown('<div class="output-image-marker"></div>', unsafe_allow_html=True)
                    st.image(output, use_column_width=True, channels="GRAY")
                    add_to_history("Image", "Convert Grayscale", "[Image]", "Grayscale channel conversion complete.")
                    
                elif selected_action == "edges":
                    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                    output = cv2.Canny(gray, st.session_state.canny_t1, st.session_state.canny_t2)
                    st.markdown("##### Edge Detection Result")
                    st.markdown('<div class="output-image-marker"></div>', unsafe_allow_html=True)
                    st.image(output, use_column_width=True, channels="GRAY")
                    add_to_history("Image", "Edge Detection", "[Image]", f"Canny edge extraction ({st.session_state.canny_t1}, {st.session_state.canny_t2})")
                    
                elif selected_action == "blur":
                    k = st.session_state.blur_k
                    if k % 2 == 0:
                        k += 1
                    output = cv2.GaussianBlur(img_array, (k, k), 0)
                    st.markdown("##### Gaussian Blur Result")
                    st.markdown('<div class="output-image-marker"></div>', unsafe_allow_html=True)
                    st.image(output, use_column_width=True)
                    add_to_history("Image", "Gaussian Blur", "[Image]", f"Gaussian blur smoothing applied (Kernel size {k})")
                    
                elif selected_action == "invert":
                    output = cv2.bitwise_not(img_array)
                    st.markdown("##### Inverted Colors Result")
                    st.markdown('<div class="output-image-marker"></div>', unsafe_allow_html=True)
                    st.image(output, use_column_width=True)
                    add_to_history("Image", "Invert Colors", "[Image]", "RGB pixel value bits inverted.")
            except Exception as e:
                st.error(f"❌ Error during image processing: {e}")
                
    else:
        st.info("💡 Select one of the actions above to run text analysis or OpenCV image transformation!")

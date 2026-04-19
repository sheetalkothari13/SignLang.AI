import streamlit as st
import sys
import os

st.set_page_config(
    page_title="Sign Language Translator",
    page_icon="🤟",
    layout="wide",
)

st.title("🤟 Sign Language Translator")
st.caption("Powered by the `sign-language-translator` Python library (v0.8.1)")

# --- Try importing the library ---
try:
    import sign_language_translator as slt
    SLT_AVAILABLE = True
except Exception as e:
    SLT_AVAILABLE = False
    st.error(f"Failed to import sign_language_translator: {e}")
    st.stop()

# --- Sidebar ---
with st.sidebar:
    st.header("About")
    st.write(
        "This library bridges the communication gap between the hearing and "
        "hearing-impaired community using AI.\n\n"
        "It supports **text ↔ sign language** translation with rule-based and "
        "deep learning models."
    )
    st.markdown("---")
    st.markdown("[GitHub](https://github.com/sign-language-translator/sign-language-translator)")
    st.markdown("[Documentation](https://sign-language-translator.readthedocs.io)")
    st.markdown("[Web Demo](https://huggingface.co/sltAI)")

# --- Tabs ---
tab_overview, tab_languages, tab_models, tab_text, tab_translate, tab_assets = st.tabs([
    "Overview", "Languages", "Models", "Text Processing", "Translation", "Assets"
])

# ─── OVERVIEW ───
with tab_overview:
    st.subheader("What this library does")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Text → Sign Language")
        st.markdown(
            "- Rule-based **concatenative synthesis**: maps each word to a pre-recorded sign video clip\n"
            "- Deep learning seq2seq (coming soon)\n"
            "- Outputs: video, landmarks (CSV/GIF), or pose vectors"
        )
    with col2:
        st.markdown("#### Sign Language → Text")
        st.markdown(
            "- Extract Mediapipe pose landmarks from video\n"
            "- Feed to a classification model (neural network)\n"
            "- Supports Pakistan Sign Language (PSL)"
        )
    st.markdown("---")
    st.markdown("#### Architecture")
    st.code(
        """import sign_language_translator as slt

# Text → Sign (rule-based)
model = slt.models.ConcatenativeSynthesis(
    text_language="urdu",
    sign_language="pk-sl",
    sign_format="video"
)
sign = model.translate("یہ بہت اچھا ہے۔")
sign.show()   # plays sign video

# Check available models
print(list(slt.ModelCodes))
print(list(slt.TextLanguageCodes))
print(list(slt.SignLanguageCodes))
""",
        language="python"
    )

# ─── LANGUAGES ───
with tab_languages:
    st.subheader("Supported Languages")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Text Languages")
        try:
            langs = list(slt.TextLanguageCodes)
            for lang in langs:
                st.write(f"• `{lang.value}` — {lang.name.title()}")
        except Exception as e:
            st.error(str(e))

    with col2:
        st.markdown("#### Sign Languages")
        try:
            langs = list(slt.SignLanguageCodes)
            for lang in langs:
                st.write(f"• `{lang.value}` — {lang.name.replace('_', ' ').title()}")
        except Exception as e:
            st.error(str(e))

    with col3:
        st.markdown("#### Sign Formats")
        try:
            fmts = list(slt.SignFormatCodes)
            for fmt in fmts:
                st.write(f"• `{fmt.value}` — {fmt.name.replace('_', ' ').title()}")
        except Exception as e:
            st.error(str(e))

    st.markdown("---")
    st.info(
        "Currently Pakistan Sign Language (PSL) is the primary supported sign language. "
        "The framework is extensible — you can add any regional sign language by subclassing "
        "`TextLanguage` and `SignLanguage`."
    )

# ─── MODELS ───
with tab_models:
    st.subheader("Available Models")

    try:
        from sign_language_translator.config.enums import ModelCodeGroups, ModelCodes
        groups = list(ModelCodeGroups)
        all_codes = list(ModelCodes)

        st.write(f"Total model codes: **{len(all_codes)}**")
        st.markdown("---")

        cols = st.columns(2)
        for i, group in enumerate(groups):
            with cols[i % 2]:
                st.markdown(f"**{group.name.replace('_', ' ').title()}**")
                try:
                    members = list(group.value)
                    for m in members:
                        st.write(f"  • `{m.value}`")
                except Exception:
                    st.write(f"  `{group.value}`")
                st.write("")

    except Exception as e:
        st.write("Listing all model codes:")
        try:
            for code in list(slt.ModelCodes):
                st.write(f"• `{code.value}`")
        except Exception as e2:
            st.error(str(e2))

# ─── TEXT PROCESSING ───
with tab_text:
    st.subheader("Text Processing")
    st.write("Explore tokenization and tagging for supported text languages.")

    text_lang = st.selectbox(
        "Select text language",
        options=["english", "urdu", "hindi"],
        key="text_lang_select"
    )

    sample_texts = {
        "english": "Hello, how are you doing today?",
        "urdu": "آپ کیسے ہیں؟",
        "hindi": "आप कैसे हैं?",
    }

    user_text = st.text_area(
        "Enter text to process",
        value=sample_texts.get(text_lang, "Hello"),
        height=100
    )

    if st.button("Process Text"):
        if not user_text.strip():
            st.warning("Please enter some text.")
        else:
            with st.spinner("Processing..."):
                try:
                    lang_obj = slt.get_text_language(text_lang)
                    st.success(f"Language loaded: `{type(lang_obj).__name__}`")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**Tokens**")
                        try:
                            tokens = lang_obj.tokenize(user_text)
                            for i, tok in enumerate(tokens):
                                st.write(f"{i+1}. `{tok}`")
                        except Exception as e:
                            st.error(f"Tokenization error: {e}")

                    with col2:
                        st.markdown("**Tags**")
                        try:
                            tokens = lang_obj.tokenize(user_text)
                            tags = lang_obj.get_tags(tokens)
                            for tok, tag in zip(tokens, tags):
                                st.write(f"`{tok}` → `{tag}`")
                        except Exception as e:
                            st.error(f"Tagging error: {e}")

                except Exception as e:
                    st.error(f"Error loading language: {e}")

# ─── TRANSLATION ───
with tab_translate:
    st.subheader("Text → Sign Language Translation")
    st.info(
        "Translation requires downloading sign video assets (~few MB per word). "
        "On first run this may take a moment. Assets are cached locally."
    )

    col1, col2 = st.columns(2)
    with col1:
        tl = st.selectbox("Text language", ["urdu", "english", "hindi"], key="tl_sel")
    with col2:
        sl = st.selectbox("Sign language", ["pk-sl"], key="sl_sel")

    sign_fmt = st.radio("Output format", ["video", "landmarks"], horizontal=True)

    embedding_model = None
    if sign_fmt == "landmarks":
        embedding_model = st.selectbox(
            "Embedding model (required for landmarks)",
            ["mediapipe-world", "mediapipe-image"],
            help="mediapipe-world uses 3D coordinates; mediapipe-image uses 2D image coordinates."
        )
        st.caption("Note: MediaPipe landmarks require the `mediapipe` package. Install it if you see an import error.")

    sample_phrases = {
        "urdu": "آپ کا نام کیا ہے؟",
        "english": "hello",
        "hindi": "नमस्ते",
    }

    phrase = st.text_input("Enter phrase to translate", value=sample_phrases.get(tl, "hello"))

    if st.button("Translate"):
        if not phrase.strip():
            st.warning("Please enter a phrase.")
        else:
            with st.spinner("Loading model and translating (may download assets)..."):
                try:
                    init_kwargs = dict(
                        text_language=tl,
                        sign_language=sl,
                        sign_format=sign_fmt,
                    )
                    if sign_fmt == "landmarks" and embedding_model:
                        init_kwargs["sign_embedding_model"] = embedding_model

                    model = slt.models.ConcatenativeSynthesis(**init_kwargs)
                    sign = model.translate(phrase)
                    st.success("Translation successful!")

                    st.markdown("**Tokenization details**")
                    try:
                        tokens = model.text_language.tokenize(phrase)
                        tags = model.text_language.get_tags(tokens)
                        st.table({"Token": tokens, "Tag": tags})
                    except Exception:
                        pass

                    if sign_fmt == "landmarks":
                        st.markdown("**Landmarks output**")
                        try:
                            import numpy as np
                            arr = sign.numpy() if hasattr(sign, "numpy") else np.array(sign)
                            st.write(f"Array shape: `{arr.shape}`")
                            st.write("Each row = one frame, columns = landmark coordinates (x, y, z, visibility, presence).")
                            st.dataframe(arr[:5])
                        except Exception as e:
                            st.write(f"Sign object type: `{type(sign).__name__}`")
                            st.write(str(sign)[:500])
                    else:
                        out_path = "/tmp/sign_output.mp4"
                        try:
                            sign.save(out_path, overwrite=True)
                            with open(out_path, "rb") as f:
                                st.video(f.read())
                        except Exception as e:
                            st.warning(f"Could not render video: {e}")
                            st.write(f"Sign type: `{type(sign).__name__}`")

                except Exception as e:
                    st.error(f"Translation error: {e}")
                    st.caption("This may happen if required dataset assets haven't been downloaded yet, "
                               "or if an optional dependency like `mediapipe` is missing.")
                    with st.expander("Error detail"):
                        st.code(str(e))

# ─── ASSETS ───
with tab_assets:
    st.subheader("Dataset & Model Assets")
    st.write(
        "The library downloads datasets and model weights on demand. "
        "Below you can inspect what assets are available or already downloaded."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Assets root directory**")
        try:
            st.code(slt.Assets.ROOT_DIR)
        except Exception as e:
            st.error(str(e))

        if st.button("Show downloaded files"):
            try:
                import os
                root = slt.Assets.ROOT_DIR
                if os.path.exists(root):
                    files = []
                    for dirpath, _, filenames in os.walk(root):
                        for fn in filenames:
                            rel = os.path.relpath(os.path.join(dirpath, fn), root)
                            files.append(rel)
                    if files:
                        for f in sorted(files)[:50]:
                            st.write(f"• `{f}`")
                        if len(files) > 50:
                            st.write(f"... and {len(files)-50} more")
                    else:
                        st.info("No assets downloaded yet.")
                else:
                    st.info("Assets directory does not exist yet.")
            except Exception as e:
                st.error(str(e))

    with col2:
        st.markdown("**Downloadable assets (first 40)**")
        try:
            keys = list(slt.Assets.FILE_TO_URL.keys())
            for k in keys[:40]:
                st.write(f"• `{k}`")
            if len(keys) > 40:
                st.info(f"... and {len(keys)-40} more assets available")
        except Exception as e:
            st.error(str(e))

    st.markdown("---")
    st.markdown("**Trigger a manual download**")
    pattern = st.text_input("Regex pattern (e.g., `.*.json` for all JSON files)", value="")
    if st.button("Download matching assets"):
        if not pattern.strip():
            st.warning("Please enter a pattern.")
        else:
            with st.spinner(f"Downloading assets matching `{pattern}` ..."):
                try:
                    slt.Assets.download(pattern)
                    st.success("Download complete!")
                except Exception as e:
                    st.error(f"Download error: {e}")

# AI Sign Bridge 🤟

A Streamlit web app powered by the [`sign-language-translator`](https://github.com/sign-language-translator/sign-language-translator) Python library (v0.8.1).

This project bridges the communication gap between the hearing and hearing-impaired community using AI, enabling translation between text and Pakistan Sign Language (PSL).

## Features

- **Text → Sign Language** translation using rule-based concatenative synthesis
- **Text processing**: tokenization and tagging for Urdu, English, and Hindi
- **Sign formats**: video clips or landmark pose vectors (Mediapipe)
- **Asset browser**: explore and download datasets/models
- **Model explorer**: view all available models and language codes

## Tech Stack

- Python 3.11
- [Streamlit](https://streamlit.io/)
- [sign-language-translator](https://pypi.org/project/sign-language-translator/) — core ML library
- PyTorch, OpenCV, NumPy, Matplotlib

## Setup & Run

```bash
pip install streamlit sign-language-translator torch opencv-contrib-python matplotlib
streamlit run app.py --server.port 5000
```

## Upstream Library

The original `sign-language-translator` library is at:
https://github.com/sign-language-translator/sign-language-translator

## License

Apache-2.0

# Multimodal Processor UI

A Streamlit app combining NLP (spaCy + NLTK) and Computer Vision (OpenCV),
built to match the attached requirements/screenshot.

## Setup

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt punkt_tab
```

## Run

```bash
streamlit run app.py
```

## Features
- **Text Input Mode**: type/paste text, then run
  - Extract Entities (spaCy NER)
  - POS Tagging (spaCy)
  - Extract Noun Chunks (spaCy)
  - Tokenize Words (NLTK)
- **Image (OpenCV) Mode**: upload an image, then run
  - Convert Grayscale
  - Edge Detection (Canny)
  - Gaussian Blur
  - Invert Colors
- Gradient-styled, rounded 8-button action grid
- Friendly warnings instead of crashes on empty text/no image

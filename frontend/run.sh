#!/bin/bash
# Forzar configuración de tema antes de iniciar Streamlit
export STREAMLIT_THEME=light
export STREAMLIT_SERVER_HEADLESS=true

# Iniciar Streamlit con configuración mínima
streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.fileWatcherType=none \
    --theme.base=light \
    --theme.primaryColor=#6c5ce7 \
    --theme.backgroundColor=#f5f7fa \
    --theme.secondaryBackgroundColor=#e6f0ff \
    --theme.textColor=#1a1a1a

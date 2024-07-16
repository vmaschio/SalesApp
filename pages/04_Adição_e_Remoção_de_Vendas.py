from pathlib import Path
import streamlit as st
import pandas as pd
from utilidades import leitura_de_dados

leitura_de_dados()

df_vendas = st.session_state['dados']['df_vendas']
df_filiais = st.session_state['dados']['df_filiais']
df_produtos = st.session_state['dados']['df_produtos']

st.dataframe(df_vendas)
st.dataframe(df_filiais)
st.dataframe(df_produtos)
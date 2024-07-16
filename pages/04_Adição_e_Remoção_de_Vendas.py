from pathlib import Path
from datetime import datetime
import streamlit as st
import pandas as pd
from utilidades import leitura_de_dados

leitura_de_dados()

df_vendas = st.session_state['dados']['df_vendas']
df_filiais = st.session_state['dados']['df_filiais']
df_produtos = st.session_state['dados']['df_produtos']

df_filiais['cidade/estado'] = df_filiais['cidade'] + '/' + df_filiais['estado']
cidades_filiais = df_filiais['cidade/estado'].to_list()

st.sidebar.markdown('## Adição de vendas')
filial_selecionada = st.sidebar.selectbox('Selecione a filial',
                                          cidades_filiais)
vendedores = df_filiais.loc[df_filiais['cidade/estado'] == filial_selecionada, 'vendedores'].iloc[0]
vendedores = vendedores.strip('][').replace("'",'').split(', ')
vendedor_selecionado = st.sidebar.selectbox('Selecione o vendedor:',
                                            vendedores)
produtos = df_produtos['nome'].to_list()
produto_selecionado = st.sidebar.selectbox('Selecione o produto:',
                                            vendedores)
nome_cliente = st.sidebar.text_input('Nome do cliente')
genero_selecionado = st.sidebar.selectbox('Gênero do cliente:',
                                          ['masculino', 'feminino'])
forma_pagamento = st.sidebar.selectbox('Forma de pagamento:',
                                       ['boleto', 'pix', 'credito'])
adicionar_venda = st.sidebar.button('Adicionar Venda')
if adicionar_venda:
    lista_adicionar = [df_vendas['id_venda'].max()+1,
                       filial_selecionada.split('/')[0],
                       vendedor_selecionado,
                       produto_selecionado,
                       nome_cliente,
                       genero_selecionado,
                       forma_pagamento]
    hora_adicionar = datetime.now()
    df_vendas.loc[hora_adicionar] = lista_adicionar
    caminho_datasets = st.session_state['caminho_datasets']
    df_vendas.to_csv(caminho_datasets / 'vendas.csv', decimal=',', sep=';')

st.sidebar.markdown('## Edição de Vendas')
id_edicao = st.sidebar.number_input('Id venda a ser editado:', 0, df_vendas['id_venda'].max(), key='edit_id')
iniciar_edicao = st.sidebar.button('Editar Venda', key='edit_button')

if iniciar_edicao or 'editando' in st.session_state:
    if iniciar_edicao:
        st.session_state.editando = True
        st.session_state.id_edicao = id_edicao
        venda_edicao = df_vendas[df_vendas['id_venda'] == id_edicao]
        st.session_state.filial_selecionada_ed = venda_edicao.iloc[0]['filial'] + '/' + df_filiais.loc[df_filiais['cidade'] == venda_edicao.iloc[0]['filial']]['estado'].values[0]
        st.session_state.vendedor_selecionado_ed = venda_edicao.iloc[0]['vendedor']
        st.session_state.produto_selecionado_ed = venda_edicao.iloc[0]['produto']
        st.session_state.nome_cliente_ed = venda_edicao.iloc[0]['cliente_nome']
        st.session_state.genero_selecionado_ed = venda_edicao.iloc[0]['cliente_genero']
        st.session_state.forma_pagamento_ed = venda_edicao.iloc[0]['forma_pagamento']
    else:
        id_edicao = st.session_state.id_edicao

    filial_selecionada_ed = st.sidebar.selectbox('Selecione a filial', cidades_filiais, 
                                                 index=cidades_filiais.index(st.session_state.filial_selecionada_ed), key='edit_filial')
    vendedores_ed = df_filiais.loc[df_filiais['cidade/estado'] == filial_selecionada_ed, 'vendedores'].iloc[0]
    vendedores_ed = vendedores_ed.strip('][').replace("'", '').split(', ')
    vendedor_selecionado_ed = st.sidebar.selectbox('Selecione o vendedor:', vendedores_ed, index=vendedores_ed.index(st.session_state.vendedor_selecionado_ed) if st.session_state.vendedor_selecionado_ed in vendedores_ed else 0, key='edit_vendedor')
    produto_selecionado_ed = st.sidebar.selectbox('Selecione o produto:', produtos, index=produtos.index(st.session_state.produto_selecionado_ed), key='edit_produto')
    nome_cliente_ed = st.sidebar.text_input('Nome do cliente', value=st.session_state.nome_cliente_ed, key='edit_nome_cliente')
    genero_selecionado_ed = st.sidebar.selectbox('Gênero do cliente:', ['masculino', 'feminino'], index=['masculino', 'feminino'].index(st.session_state.genero_selecionado_ed), key='edit_genero')
    forma_pagamento_ed = st.sidebar.selectbox('Forma de pagamento:', ['boleto', 'pix', 'credito'], index=['boleto', 'pix', 'credito'].index(st.session_state.forma_pagamento_ed), key='edit_forma_pagamento')
    
    confirmar_edicao = st.sidebar.button('Confirmar Edição', key='confirm_edit_button')
    if confirmar_edicao:
        df_vendas.loc[df_vendas['id_venda'] == id_edicao, ['filial', 'vendedor', 'produto', 'cliente_nome', 'cliente_genero', 'forma_pagamento']] = [
            filial_selecionada_ed.split('/')[0],
            vendedor_selecionado_ed,
            produto_selecionado_ed,
            nome_cliente_ed,
            genero_selecionado_ed,
            forma_pagamento_ed
        ]
        caminho_datasets = st.session_state['caminho_datasets']
        df_vendas.to_csv(caminho_datasets / 'vendas.csv', decimal=',', sep=';')
        st.session_state['dados']['df_vendas'] = df_vendas
        st.session_state.editando = False

st.sidebar.markdown('## Remoção de Vendas')
id_remocao = st.sidebar.number_input('Id venda a ser removido:',
                                     0,
                                     df_vendas['id_venda'].max())
remover_venda = st.sidebar.button('Remover Venda')
if remover_venda:
    df_vendas = df_vendas[df_vendas['id_venda'] != id_remocao]
    caminho_datasets = st.session_state['caminho_datasets']
    df_vendas.to_csv(caminho_datasets / 'vendas.csv', decimal=',', sep=';')
    st.session_state['dados']['df_vendas'] = df_vendas
    

st.dataframe(df_vendas)
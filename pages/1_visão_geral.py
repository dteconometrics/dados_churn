# Pacotes 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st 


st.set_page_config(page_title="Dados Gerais",
                   page_icon="", 
                   layout="wide")


## Estilos  

custom_css = """
<style>
    body {
        background-color: #f0f2f6; /* Fundo geral */
        color: #333333; /* Texto principal */
        font-family: Arial, sans-serif;
    }
    .metric-box {
        background-color: #007BFF; /* Fundo azul */
        color: white; /* Texto branco */
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
</style>
"""



st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)

# CSS Personalizado para reduzir o tamanho do Value Box
custom_css = """
<style>
    .metric-box {
        padding: 10px; /* Reduz o espaçamento interno */
        border-radius: 8px; /* Bordas arredondadas menores */
        text-align: center;
        background-color: #007BFF; /* Cor de fundo */
        color: white; /* Cor do texto */
        font-weight: bold;
        font-size: 16px; /* Reduz o tamanho do texto */
    }
    .metric-box p {
        font-size: 18px; /* Reduz o tamanho do valor */
        margin: 0;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)


## Importação dos Dados 


df = pd.read_excel('df_final.xlsx')



# Calcular os totais para o value Box 

# Calculando as métricas
total_lojas = df['loja'].nunique()  # Número total de lojas únicas
cancelaram = len(df[df['churn'] == 1])  # Total de clientes que cancelaram
total_clientes_ativos = len(df[df['churn'] == 0])  # Total de clientes ativos

# Função para simplificar os números grandes
def format_large_numbers(number):
    if abs(number) >= 1_000_000_000:
        return f'R${number / 1_000_000_000:.2f}B'
    elif abs(number) >= 1_000_000:
        return f'R${number / 1_000_000:.2f}M'
    elif abs(number) >= 1_000:
        return f'R${number / 1_000:.2f}K'
    else:
        return f'R${number:.2f}'







## Dados Tratados anteriormente 

# Para o Streamlit 

# Visualização com Streamlit
#st.title(" Visualiação")

# Adicionando filtros adicionais
st.sidebar.header("Visão geral: Propoção do cancelamento, Cancelamento por estado, por loja e evolução")

# Filtros Gerais 

#loja =  ["Todos"] + list(df['loja'].unique())

# Seleção de filtros na barra lateral

#loja_selecionada = st.sidebar.selectbox("Selecione a loja", loja)


# Aplicando filtros

df_filtrado = df.copy()



# Mostra uma mensagem no corpo principal da aplicação
st.markdown('### Metricas')


col1, col2, col3 = st.columns(3)

# Value Box: Total de Lojas
with col1:
    st.markdown(f"""
    <div class="metric-box">
        <h3>Total de Lojas</h3>
        <p>{total_lojas}</p>
    </div>
    """, unsafe_allow_html=True)

# Value Box: Total Cancelamentos
with col2:
    st.markdown(f"""
    <div class="metric-box">
        <h3>Total Cancelamentos</h3>
        <p>{cancelaram}</p>
    </div>
    """, unsafe_allow_html=True)

# Value Box: Clientes Ativos
with col3:
    st.markdown(f"""
    <div class="metric-box">
        <h3>Clientes Ativos</h3>
        <p>{total_clientes_ativos}</p>
    </div>
    """, unsafe_allow_html=True)
    
# Divider entre seções
st.divider()

# Criação de colunas para a visualização dos gráficos
col1, col2  = st.columns(2)
col3, col4  = st.columns(2)   


with col1:
    fig1 = px.pie(df, names='churn', title='Proporção de Cancelamento', color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig1, use_container_width=True)

cancelamento_por_estado = df.groupby('estado')['churn'].sum().reset_index()
with col2:
    fig2 = px.bar(cancelamento_por_estado.reset_index(), x='estado', y='churn', 
                  title='Cancelamentos por Estado', color='estado', text_auto=True)
    st.plotly_chart(fig2, use_container_width=True)    


with col3:
    fig3 = px.bar(df.groupby('loja')['churn'].sum().reset_index(), x='loja', y='churn', 
                  title='Cancelamentos por Loja', color='churn', text_auto=True)
    st.plotly_chart(fig3, use_container_width=True)



df_filtrado = df[df['data_de_cancelamento'] >= '2021-01-01']


df_filtrado['mes_ano'] = df_filtrado['data_de_cancelamento'].dt.to_period('M').astype(str)


cancelamento_mensal = df_filtrado.groupby('mes_ano')['churn'].sum().reset_index()
cancelamento_mensal.columns = ['mes_ano', 'total_cancelamento']

# Calcular a média mensal
media_mensal = cancelamento_mensal['total_cancelamento'].mean()

# Gráfico de linha com média mensal
with col4:
    fig4 = go.Figure()

    # Adicionar linha de cancelamentos mensais
    fig4.add_trace(go.Scatter(
        x=cancelamento_mensal['mes_ano'], 
        y=cancelamento_mensal['total_cancelamento'],
        mode='lines+markers',
        name='Cancelamentos Mensais',
        line=dict(color='blue'),
        marker=dict(size=6)
    ))

    # Adicionar linha horizontal da média mensal
    fig4.add_trace(go.Scatter(
        x=cancelamento_mensal['mes_ano'], 
        y=[media_mensal] * len(cancelamento_mensal),
        mode='lines',
        name=f'Média Mensal ({media_mensal:.0f})',
        line=dict(color='red', dash='dash')
    ))

    # Layout do gráfico
    fig4.update_layout(
        title='Evolução Mensal de Cancelamentos a partir de 2021',
        xaxis_title='Mês/Ano',
        yaxis_title='Total de Cancelamentos',
        template='plotly_white',
        showlegend=True
    )

    # Mostrar o gráfico
    st.plotly_chart(fig4, use_container_width=True)

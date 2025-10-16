AZULS = [ '#174A7E', '#4A81BF', "#6495ED", '#2596BE', '#94AFC5', '#CDDBF3']
CINZAS = ['#231F20', '#414040', '#555655', '#A6A6A5', '#BFBEBE', '#CED4DA', '#FFFFFF']
VERMELHOS =[ '#C3514E','#E6BAB7', '#F79747' ]
VERDES =['#0C8040', '#9ABB59', '#9ECCB3']

import pandas as pd 
import plotly.graph_objects as go


# Carregar os dados do PIB dos estados brasileiros
df_sp = pd.read_csv("https://raw.githubusercontent.com/alura-cursos/dataviz-graficos-composicao-relacionamento/main/dados/pib_br_2002_2020_estados.csv")

# Criando um df com os dados desejados
df_sp = df_sp.query("sigla_uf == 'SP' and ano == 2020")[["va", "impostos_liquidos", "pib"]]
df_sp.rename ( columns = {"pib":"PIB", "impostos_liquidos":"Impostos Líquidos", "va":"Valor Agregado Bruto"}, inplace = True)

# Alterando o df para passar os Indicadores para uma única coluna e seus valores em outra coluna
df_sp = df_sp.melt(var_name = "Indicadores", value_name = "Valores")

# Adicionando colunas com os valores formatados e as medidas
df_sp["Valores_str"] = (df_sp["Valores"]/1e12).map("R$ {:,.3f} tri".format)
df_sp["Medidas"] = ["absolute", "relative","totals"]

df_sp

#Gerando o Gráfico

fig = go.Figure(go.Waterfall(name="", measure=df_sp["Medidas"],
                             x =df_sp["Indicadores"], y = df_sp["Valores"],
                             text = df_sp["Valores_str"], textposition ="outside",
                             connector_line = dict(color = CINZAS[0] ),
                             totals_marker = dict(color = AZULS[3] ),
                             increasing_marker = dict(color =VERDES[1] ),
                             )
 )

#Personalizando o gráfico

fig.update_layout (width=800, height=400, font_family="Arial", font_size=14,
                  font_color =CINZAS[2] , title_font_color = CINZAS[0], title_font_size = 20,
                  title = "Composição do PIB do Estado de São Paulo - 2020" + 
                  f'<br><sup size=1 styke="color:{CINZAS[1]}">Valores em trilhões de Reais (R$)</sup>',
                  plot_bgcolor =CINZAS[6], yaxis_range=[0,2.6e12], hovermode='closest')

# Retirando os ticks do eixo y
fig.update_yaxes(showticklabels=False)

# Dados ao passar o mouse
fig.update_traces(hovertemplate = "<b>%{x}</b> = %{text}")

fig.show()
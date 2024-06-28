import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title= 'Survey Results')
st.header("Survey Results 2021")


## ---- LOAD DATA
data = pd.read_excel('Survey_Results.xlsx', sheet_name="DATA", usecols='B:D', header= 3)
participants = pd.read_excel('Survey_Results.xlsx', sheet_name="DATA", usecols='F:G', header= 3)
participants.dropna(inplace= True)


department = data['Department'].unique().tolist()
ages = data['Age'].unique().tolist()

age_selection = st.slider("Age:",
                          min_value= min(ages),
                          max_value= max(ages),
                          value= (min(ages), max(ages)))
deparment_selection = st.multiselect('Department:',
                                     department,
                                     default= department)


mask = (data['Age'].between(*age_selection)) & (data['Department'].isin(deparment_selection))
number_of_result = data[mask].shape[0]
st.markdown(f'Available Results :{number_of_result}')


df_grouped = data[mask].groupby(by = ['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age' : 'Votes'})
df_grouped = df_grouped.reset_index()

bar_chart = px.bar(df_grouped,
                   x = 'Rating',
                   y = 'Votes',
                   text= 'Votes',
                   color_discrete_sequence=['#F63362']*len(df_grouped),
                   template='plotly_white')

st.plotly_chart(bar_chart)

col1, col2 = st.columns(2)
image = Image.open('Images/survey.jpg')
col1.image(image, caption=' designed By slidesgo / freepiK',
         use_column_width=True)
col2.dataframe(data[mask])


pie_chart = px.pie(participants, title='Total No of Participants',
                   values='Participants',
                   names = 'Departments')
st.plotly_chart(pie_chart)











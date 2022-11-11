from calendar import month
from tkinter import Y
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import matplotlib.pyplot as plt
import datetime
import numpy as np

st.set_page_config(page_title='Survey Results')
st.header('Survey Results 2021')
st.subheader("useful info in pictorial representation")


# "C:\Users\saich\OneDrive\Desktop"
#C:\Users\saich\OneDrive\Documents



###--- LOAD DATAFRAME
excel_file='D:/LAB/HO Utility Info/bills_Homestead_Oaks_HO_Electric.xls'
#sheet_name= 'DATA'
# Days_Billed
df=pd.read_excel(excel_file,usecols='B:H',header=0)

#st.dataframe(df)

st.sidebar.header("Please filter here:")
days_billed=st.sidebar.multiselect('select no. of days:',options=df["Days_Billed"].unique(),default=df["Days_Billed"].unique())

# year=st.slider('select an year:',min_value=2015,max_value=2022,step=1)
# year2=st.')

# df_selection= df.query("Days_Billed==@days_billed & Year==@year")
df_selection= df.query("Days_Billed==@days_billed")
# df.loc[3,'Start_Date']
st.dataframe(df_selection)


# H=pd.to_datetime(df['Start_Date'],format='%m/%d/%Y')
# df=datetime.strptime(df['Start_Date'],'%m/%d/%Y')
# st.dataframe(df.year)
# st.dataframe()
date_col=pd.DatetimeIndex(df['Start_Date'])
# st.dataframe(date_col)
df['Year']=date_col.year
df['Month']=date_col.month
df['Total_bill']=(df['Bill_Amount']+df['Third_Party_Bill']).astype(float)
# st.dataframe(df)

year=df['Year'].unique().tolist()
mnth=df['Month'].unique().tolist().sort()


months_billed=st.sidebar.multiselect('Please select months:',options=df["Month"].unique(),default=df["Month"].unique())


year_selection=st.sidebar.slider('select an year:',min_value=min(year),max_value=max(year),value=(min(year),max(year)))

#--- filter dataframe based on selection

mask=(df['Year'].between(*year_selection)) #& (df['Days_Billed']==days_billed  & (df['Month']==months_billed)
number_of_result=df[mask].shape[0]
st.markdown(f'*Avaliable Results: {number_of_result}*')


df_selection= df.query("Days_Billed==@days_billed & Month==@months_billed ")
st.dataframe(df_selection)

#--- Group dataframe after selection

df_grouped=df[mask].groupby(by=['Days_Billed']).count()[['Year']]
df_grouped=df_grouped.rename(columns={'Year':'Total_bill'})
df_grouped=df_grouped.reset_index()


bar_chart2=px.bar(df_grouped,x='Days_Billed',y='Total_bill',text='Total_bill',color_discrete_sequence=['#F63366']*len(df_grouped),template='plotly_white')
st.plotly_chart(bar_chart2)


# df_selection= df.query("Days_Billed==@days_billed & Month==@months_billed")
# st.dataframe(df_selection)

#-- bar_ chart implementation....


# sales_by_Days_Billed=(
#     df_selection.groupby(by=["Days_Billed"].sum()[["Total"]].sort_values(by="Total"))

df=pd.DataFrame({'Bill_Amount':df_selection["Bill_Amount"],'Days_Billed':df_selection['Days_Billed']})

# df # if you uncomment this df will print the two columns of Bill_Amount and "Days_Billed" seperately ..

st.bar_chart(df)




#----pie chart


# plt.pie(float('Total_bill'),labels='Year')
# plt.show()

pie_chart=px.pie(df_selection,title='For Year and Total_bill',values='Total_bill',names="Year")

st.plotly_chart(pie_chart)

pie_chart1=px.pie(df_selection,title="For Total_bill and Month",values='Total_bill',names="Month")
st.plotly_chart(pie_chart1)


# line-chart
line_chart_data=df_selection.copy()
hour_cross_tab=pd.crosstab(line_chart_data['Month'],line_chart_data['Bill_Amount'])
print(hour_cross_tab)

fig=px.line(hour_cross_tab)

st.write(fig)

#scatter-plots
st.subheader("the scatter plot between year and bill amount")
fig1,ax=plt.subplots(1,1)
ax.scatter(x=df_selection['Year'],y=df['Bill_Amount'])
st.pyplot(fig1)

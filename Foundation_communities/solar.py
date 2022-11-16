from calendar import month
from tkinter import Y
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import matplotlib.pyplot as plt
import datetime
import numpy as np
import altair as alt
import plotly.figure_factory as ff

st.set_page_config(page_title='Survey Results')
st.header('Survey Results On solar_PV_Generated_Tenant_Elec From 2015-2022')
st.subheader("Useful Info in Pictorial Representation")

excel_file="D:/LAB/HO Utility Info/bills_Homestead_Oaks_Aggregate_Solar_PV_Generated_Tenant_Elec.xls"


df=pd.read_excel(excel_file,usecols='B:G',header=0)





st.sidebar.header("Please filter here:")
days_billed=st.sidebar.multiselect('select no. of days:',options=df["Days_Billed"].unique(),default=df["Days_Billed"].unique())


df_selection= df.query("Days_Billed==@days_billed")
df_selection=df_selection.reset_index()
# st.dataframe(df_selection)



st.subheader('please fill the check box')
if st.checkbox('show the data of the solar_pv_generated_tenant_elec'):
    st.subheader('Original data of the solar_pv_generated_tenant_elec')
    st.write(df_selection)


date_col=pd.DatetimeIndex(df['Start_Date'])
# st.dataframe(date_col)
df['Month']=date_col.month
df['Year']=date_col.year


mnth=df['Month'].unique().tolist().sort()
year=df['Year'].unique().tolist()



months_billed=st.sidebar.multiselect('Please select months:',options=df["Month"].unique(),default=df["Month"].unique())

year_billed=st.sidebar.multiselect('Please select years:',options=df["Year"].unique(),default=df["Year"].unique())

df_selection= df.query("Days_Billed==@days_billed & Month==@months_billed & Year==@year_billed")
df_selection=df_selection.reset_index()
st.dataframe(df_selection)

total_usage=int(df_selection['Usage'].sum())
average_usage=round(df_selection['Usage'].mean(),1)
average_bill=round(df_selection['Bill_Amount'].mean(),2)

left_column,middle_column,right_column=st.columns(3)

with left_column:
    st.subheader("Total Usage:")
    st.subheader(f'{total_usage:,} kWh')
with middle_column:
    st.subheader('Average Usage')
    st.subheader(f'{average_usage:}')
with right_column:
    st.subheader("Average bill")
    st.subheader(f'US $ {average_bill}')


st.subheader("Below are the Bar charts representation")

st.bar_chart(df_selection['Usage'])

st.bar_chart(df_selection['Bill_Amount'])


agree = st.button('Click to see pie_charts')
if agree:
 

#pie_charts

    st.subheader("Below are the Pie_charts  representation")

    pie_chart=px.pie(df_selection,title='For Year and Usage',values='Usage',names="Year")

    st.plotly_chart(pie_chart)

    pie_chart1=px.pie(df_selection,title="For Usage and Month(all six years)",values='Usage',names="Month")
    st.plotly_chart(pie_chart1)


# line-chart

st.subheader("Below are the line charts representation")


line_chart_data=df_selection.copy()
hour_cross_tab=pd.crosstab(line_chart_data['Month'],line_chart_data['Usage'])
print(hour_cross_tab)

fig=px.line(hour_cross_tab)

st.write(fig)

st.line_chart(df_selection['Bill_Amount'])

st.line_chart(df_selection['Usage'])


#histogram

st.subheader("the Histogram between Year,Usage and bill_amount")
df = pd.DataFrame(df_selection, columns = ['Year','Usage','Bill_Amount'])
df.hist()
plt.show()
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()

st.line_chart(df)



# area_charts

st.subheader("the  between Area_chart Year,Usage and bill_amount")
chart_data = pd.DataFrame(df_selection, columns = ['Year','Usage','Bill_Amount'])

st.area_chart(chart_data)

#scatter-plots
st.subheader("the scatter plot between year and Usage")
fig1,ax=plt.subplots(1,1)
ax.scatter(x=df_selection['Year'],y=df['Usage'])
st.pyplot(fig1)


st.subheader("the scatter plot between month and Usage")
fig2,ax=plt.subplots(1,1)
ax.scatter(x=df_selection['Month'],y=df['Usage'])
st.pyplot(fig2)

st.subheader("the scatter plot between Year and bill_amount")
fig3,ax=plt.subplots(1,1)
ax.scatter(x=df_selection['Month'],y=df['Bill_Amount'])
st.pyplot(fig3)
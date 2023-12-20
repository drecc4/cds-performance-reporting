import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
import random
import plotly.graph_objects as go



#----------------------------------------------------------------------------------------------------------------------------------

#Page Functions -- move later


def select_geo_on_condition(select_role):

    if select_role == 'Region Director':
        select_geo = st.sidebar.selectbox(label='Select Your Region', options=set(list(lookup_school_region.values())))
    elif select_role == 'District Manager':
        select_geo = st.sidebar.selectbox(label='Select Your District', options=set(list(lookup_school_district.values())))
    elif select_role == 'School Director':
        select_geo = st.sidebar.selectbox(label='Select Your School', options=list(df_open_schools.SchoolID.unique()))
    else:
        select_geo = st.write(' ')
    return(select_geo)


def dynamic_report_title_one(select_role, select_geo):
    if select_role == 'Region Director':
        title = f'{select_role} Report Template for the {select_geo} Region'
    elif select_role == 'District Manager':
        title = f'{select_role} Report Template for District #{select_geo}'
    elif select_role == 'School Director':
        title = f'{select_role} Report Template for School #{select_geo}'
    else:
        title = f'{select_role} Report Template'
    return(title)


def select_pdf_report_export(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf"> Click Here to Download</a>'


#----------------------------------------------------------------------------------------------------------------------------------

#Reference Data


#School Hierarchy
df_school_hierarchy = pd.read_excel('./data/2023.07.01 - schoolHierarchy.xlsx')
df_open_schools = df_school_hierarchy.loc[df_school_hierarchy['SchoolOpen'] == 1]
lookup_school_state = dict(zip(df_open_schools.SchoolID, df_open_schools.State))
lookup_school_district = dict(zip(df_open_schools.SchoolID, df_open_schools.District))
lookup_school_region = dict(zip(df_open_schools.SchoolID, df_open_schools.Region))


#----------------------------------------------------------------------------------------------------------------------------------

#Sidebar

#Logo
st.sidebar.image('./assets/cds-logo.png', width=100)

#User Inputs
st.sidebar.write('---')
st.sidebar.write(' ')
select_role = st.sidebar.selectbox(label='Select Your Role', options=['ELT Member', 'Region Director', 'District Manager', 'School Director'], index=1)
st.sidebar.write(' ')
select_geo = select_geo_on_condition(select_role)
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write('---')


#PDF Export
st.sidebar.write('#### Want to download your latest Monthly Performance Assessment?')
select_export_pdf = st.sidebar.button(label="Click Here to Create Report", use_container_width=False,)


if select_export_pdf:
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)

    pdf.add_page()
    pdf.set_fill_color(r=248,g=248,b=248)
    pdf.rect(h=pdf.h, w=pdf.w, x=0, y=0, style="DF")
    
    pdf.set_font('Arial', 'B', 20)
    pdf.set_y(10)
    pdf.cell(10, 20, f'Monthly Performance Assessment')

    pdf.set_font('Arial', '', 12)
    pdf.set_y(18)
    pdf.cell(10, 20, f'{dynamic_report_title_one(select_role, select_geo)}')
    
    html = select_pdf_report_export(pdf.output(dest="S").encode("latin-1"), "test")

    st.sidebar.markdown(html, unsafe_allow_html=True)


#----------------------------------------------------------------------------------------------------------------------------------


#Title
st.title('CDS Performance Dashboard')
st.write(f'##### {dynamic_report_title_one(select_role, select_geo)}')
st.write('---')


#Sample Plot

sample_data_x = list(range(1,13))
sample_data_y = [random.randint(1, 9) for x in sample_data_x]
sample_data_y2 = [random.randint(1, 9) for x in sample_data_x]


fig = go.Figure(data=[
    go.Bar(name='Last Year', x=sample_data_x, y=sample_data_y, text=sample_data_y),
    go.Bar(name='This Year', x=sample_data_x, y=sample_data_y2, text=sample_data_y2)
])

fig.update_xaxes(dtick=1)
fig.update_layout(title='Example Plot #1', title_font_size=22,
                  legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="right",x=1))

st.plotly_chart(fig, use_container_width=True)

#show data
d = {'Month': sample_data_x, 'Last Year': sample_data_y, 'This Year': sample_data_y2}
df_plot = pd.DataFrame(data=d).T

with st.expander("View Data"):
    st.dataframe(df_plot)



import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import requests
import json
import plotly.express as px


st.set_page_config(layout="wide")
my_db=mysql.connector.connect(
    host="localhost",
    user="root@localhost",
    password="Charu@9601",
    database='PhonePay',
    port='3306'
)
cursor =my_db.cursor()

image_path = "C:/Users/charu/OneDrive/Pictures/PhonePe_Logo.png"
image = Image.open(image_path)
col1, col2 = st.columns([1,3])
with col1:
    st.image(image)
st.markdown("<hr style='border: 2px solid purple;'>", unsafe_allow_html=True)
with col2:
    st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

selected = option_menu(None,
                       options=["Tables","Transactions-Insights",
                                "Users-Insights","Analysis"],
                       icons=["cash-coin", "bi-people"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"container": {"width": "100%"},
                               "options": {"margin": "10px"},
                               "icon": {"color": "white", "font-size": "24px"},
                               "nav-link": {"font-size": "24px", "text-align": "center", "margin": "15px", "--hover-color": "#6F36AD"},
                               })  


cursor.execute("SELECT *FROM  aggregated_transaction")
data=cursor.fetchall()
df1 = pd.DataFrame(data, columns=cursor.column_names)
   

cursor.execute("SELECT *FROM aggregated_user") 
data=cursor.fetchall()
df2= pd.DataFrame(data, columns=cursor.column_names)
    

cursor.execute("SELECT *FROM map_transaction") 
data=cursor.fetchall()
df3 = pd.DataFrame(data, columns=cursor.column_names)
      

cursor.execute("SELECT *FROM map_user") 
data=cursor.fetchall()
df4 = pd.DataFrame(data, columns=cursor.column_names)
    

cursor.execute("SELECT *FROM top_transaction") 
data=cursor.fetchall()
df5 = pd.DataFrame(data, columns=cursor.column_names)
    

cursor.execute("SELECT *FROM top_user") 
data=cursor.fetchall()
df6 = pd.DataFrame(data, columns=cursor.column_names)

url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
response= requests.get(url)
data1= json.loads(response.content)
states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
states_name_tra.sort()


def Transcation_amount_count_Y(df, year):

    Agg_tran= df[df['Year'] == year]
    Agg_tran.reset_index(drop= True,inplace= True)
    Agg_tran.loc[:, 'Transacion_count'] = pd.to_numeric(Agg_tran['Transacion_count'])
    Agg_tran.loc[:, 'Transacion_amount'] = pd.to_numeric(Agg_tran['Transacion_amount'])
    b=Agg_tran.groupby("State")[["Transacion_count","Transacion_amount"]].sum()
    b.reset_index(inplace= True)
   
    col1,col2 =st.columns(2)
    with col1:
        fig_amount=px.bar(b,x="State",y="Transacion_amount",title=f"{year} Agg_Transcation_Amount",color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)

        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(b,x="State",y="Transacion_count",title=f"{year} Agg_Transcation_Count",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)
    with col1:
       
        fig_india_1= px.choropleth(b, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                        color= "Transacion_amount", color_continuous_scale= "Sunsetdark",
                                        range_color= (b["Transacion_amount"].min(),b["Transacion_amount"].max()),
                                        hover_name= "State",title = f"{year} TRANSACTION AMOUNT",
                                        fitbounds= "locations",width =650, height= 600)
        fig_india_1.update_geos(visible =False)
        st.plotly_chart(fig_india_1)  
    with col2:
       
        fig_india_1= px.choropleth(b, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                    color= "Transacion_count", color_continuous_scale= "Sunsetdark",
                                    range_color= (b["Transacion_count"].min(),b["Transacion_count"].max()),
                                    hover_name= "State",title = f"{year} TRANSACTION COUNT",
                                    fitbounds= "locations",width =650, height= 600)
        fig_india_1.update_geos(visible =False)
        st.plotly_chart(fig_india_1)

def Transaction_type(df,Transacion_type):
    a= df[df['Transacion_type'] == Transacion_type]
    b=a.groupby("State")[["Transacion_count","Transacion_amount"]].sum()
    b.reset_index(inplace= True)
    if Transacion_type == Transacion_type:
        fig_line = px.line(b, x='State', y='Transacion_count', 
                    title='Transaction Count Trend Over Time', 
                    color_discrete_sequence=['blue'], 
                    markers=True,                   
                    hover_data={'Transacion_count': True}, 
                    labels={'Transacion_count': 'Transaction Count', 'Year': 'Year'},width =1000, height= 700)  
        fig_line.update_traces(marker_color='red')
        fig_line.update_traces( marker_size=10)
        fig_line.update_traces(marker_symbol='diamond')
        fig_line.update_layout(plot_bgcolor='black')
        st.markdown("<h1 style='text-align: center;", unsafe_allow_html=True)
        st.plotly_chart(fig_line)    

def Map_transaction(df,states,years_):
        States= df[(df["State"]== states)]
        States.reset_index(drop=True,inplace=True)
        States.loc[:, 'People_Count'] = pd.to_numeric(States['People_Count'],errors='coerce')
        States.loc[:, 'Tran_Amount'] =pd.to_numeric(States['Tran_Amount'],errors='coerce')
        b=States.groupby(["Year","Dis_Name", "State"])[["People_Count","Tran_Amount"]].sum()
        b.reset_index(inplace= True)
        data_year = b[b["Year"] == years_]

        col1,col2=st.columns(2)
        with col1:
            fig_map_tran=px.pie(data_year,values="People_Count",names="Dis_Name", color="Dis_Name",title="District People Count Using Transaction ")
            st.plotly_chart(fig_map_tran)
            
        with col2:
            fig_map_tran=px.pie(data_year,values="Tran_Amount",names="Dis_Name", color="Dis_Name",title="District Transaction Amount")
            st.plotly_chart(fig_map_tran)
def Map(df):
        col1,col2=st.columns(2)
        with col1:
            fig_people_count = px.choropleth(df, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                                 color="People_Count", color_continuous_scale="tealrose",
                                 hover_name="State", title=" People Count",
                                 labels={"People_Count": "People Count"}, fitbounds="locations",
                                 width=650, height=600)
            fig_people_count.update_geos(visible=False)
            st.plotly_chart(fig_people_count)    

        with col2:
            fig_people_amount= px.choropleth(df, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                                 color="Tran_Amount", color_continuous_scale="tealrose",
                                 hover_name="State", title="Transaction Amount",
                                 labels={"Tran_Amount": "Transaction Amount"}, fitbounds="locations",
                                 width=650, height=600)
            fig_people_amount.update_geos(visible=False)  
            st.plotly_chart(fig_people_amount)  

def Top_tran(df,Quarter_,Selected_States):
    Quarter = df[df["Quater"]==Quarter_]
    Quarter.reset_index(drop=True,inplace=True)
    b=Quarter.groupby(["State","Year","Quater"])[["Count","Amount"]].sum()
    b.reset_index(inplace= True)
    filtered_data = b[b["State"] == Selected_States]
    col1,col2=st.columns(2)
    with col1:
        fig_Top_tran= px.pie(filtered_data,values="Count",color="Year",names="Year",hole=0.5,title=f"State Transaction count in {Quarter_} Quarter",width=600, height=400)
        st.plotly_chart(fig_Top_tran) 
    with col2:    
        fig_Top_tran= px.pie(filtered_data,values="Amount",color="Year",names="Year",hole=0.5,title=f"State Transaction Amount in {Quarter_} Quarter",width=600, height=400)
        st.plotly_chart(fig_Top_tran)  

def Agg_User(year,states_):
    Year_data=df2[(df2["Year"]==year) & (df2["State"] == states_)]
    Year_data.reset_index(drop=True,inplace=True)
    b=Year_data.groupby(["Quater","Brand","State"])[["Count","Percentage"]].sum()
    b.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_Agg_User=px.bar(b,x="Brand",y="Count",color_discrete_sequence=px.colors.sequential.Cividis_r,barmode="stack",color="Quater",title="People Usage of each Brand",width=600, height=400)
        st.plotly_chart(fig_Agg_User)
    with col2:
        fig_Aggr_Per=px.pie(b,values="Percentage",names="Brand",title= "Brand User percentage",width=600, height=400)
        st.plotly_chart(fig_Aggr_Per)

def Agg_user_map(df):

    col1,col2=st.columns(2)
    with col1:  
        fig_people_count = px.choropleth(df, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                                 color="Count", color_continuous_scale="tealrose",
                                 hover_name="State", title="Brand User Count",
                                 labels={"Count": "Count"}, fitbounds="locations",
                                 width=600, height=600)
        fig_people_count.update_geos(visible=False)
        st.plotly_chart(fig_people_count)

    with col2:
        fig_people_count = px.choropleth(df, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                                 color="Percentage", color_continuous_scale="tealrose",
                                 hover_name="State",title=" Brand User Percentage",
                                 labels={"Percentage": "Percentage"}, fitbounds="locations",
                                 width=600, height=600)
        fig_people_count.update_geos(visible=False)
        st.plotly_chart(fig_people_count)   

def Map_User(df,states,years_):

    States= df[(df["State"]== states)]
    States.reset_index(drop=True,inplace=True)
    b=States.groupby(["Year","District", "State"])[["Registered_User","Opened_Apps"]].sum()
    b.reset_index(inplace= True)
    data_year = b[b["Year"] == years_]

    col1,col2=st.columns(2)
    with col1:
        fig_map_user=px.pie(data_year,values="Registered_User",names="District", color="District",title="District Register User Count")
        st.plotly_chart(fig_map_user)
        
    with col2:
        fig_map_user = px.pie(data_year,values="Opened_Apps",names="District", color="District",title="District Opened Apps Count")
        st.plotly_chart(fig_map_user)

def Map_user_(df):
        col1,col2=st.columns(2)
        with col1:
            fig_people_count = px.choropleth(df, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                                 color="Registered_User", color_continuous_scale="tealrose",
                                 hover_name="State", title=" Registered User Count",
                                 labels={"Registered_User": "Registered_User"}, fitbounds="locations",
                                 width=650, height=600)
            fig_people_count.update_geos(visible=False)
            st.plotly_chart(fig_people_count)    

        with col2:
            fig_people_amount= px.choropleth(df, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                                 color="Opened_Apps", color_continuous_scale="tealrose",
                                 hover_name="State", title="Opened Apps",
                                 labels={"Opened_Apps": "Opened_Apps"}, fitbounds="locations",
                                 width=650, height=600)
            fig_people_amount.update_geos(visible=False)  
            st.plotly_chart(fig_people_amount) 

def Top_user(df,Quarter_,Selected_States):
    Quarter = df[df["Quater"]==Quarter_]
    Quarter.reset_index(drop=True,inplace=True)
    b=Quarter.groupby(["State","Year","Quater"])[["RegisteredUsers"]].sum()
    b.reset_index(inplace=True)
    filtered_data = b[b["State"] == Selected_States]
    fig_Top_tran= px.pie(filtered_data,values="RegisteredUsers",color="Year",names="Year",hole=0.5,title=f"State registered count in {Quarter_} Quarter",width=600, height=400)
    st.plotly_chart(fig_Top_tran) 
   
def Top_user_line(df,Quarter_,Year_):

    Quarter = df[df["Quater"]==Quarter_]
    Quarter.reset_index(drop=True,inplace=True)
    b=Quarter.groupby(["State","Year","Quater"])[["RegisteredUsers"]].sum()
    b.reset_index(inplace=True)    
    filtered_data_ = b[b["Year"] == Year_ ]
    fig_line = px.line(filtered_data_, x="State", y="RegisteredUsers", 
                        color= "Year",title="State registered count in  Quarter",
                        width=600, height=400,color_discrete_map={2018: 'Olive', 2019: 'red', 2020: 'green', 2021: 'orange', 2022: 'Yellow',2023 : 'Magenta'})
    st.plotly_chart(fig_line)

def ques1():
    lt= df1[["State", "Transacion_amount"]]
    lt1= lt.groupby("State")["Transacion_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "State", y= "Transacion_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques2():
    brand= df2[["Brand","Count"]]
    brand1= brand.groupby("Brand")["Count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Count", names= "Brand", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques3():
    htd= df3[["Dis_Name", "Tran_Amount"]]
    htd1= htd.groupby("Dis_Name")["Tran_Amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Tran_Amount", names= "Dis_Name", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)
def ques4():
    htd= df3[["Dis_Name", "Tran_Amount"]]
    htd1= htd.groupby("Dis_Name")["Tran_Amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Tran_Amount", names= "Dis_Name", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)
def ques5():
    sa= df4[["State", "Opened_Apps"]]
    sa1= sa.groupby("State")["Opened_Apps"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "State", y= "Opened_Apps", title=" Highest Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)
def ques6():
    sa= df4[["State", "Opened_Apps"]]
    sa1= sa.groupby("State")["Opened_Apps"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "State", y= "Opened_Apps", title="Lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)
def ques7():
    stc= df1[["State", "Transacion_count"]]
    stc1= stc.groupby("State")["Transacion_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "State", y= "Transacion_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= df1[["State", "Transacion_count"]]
    stc1= stc.groupby("State")["Transacion_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "State", y= "Transacion_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)
def ques9():
    lt= df1[["State", "Transacion_amount"]]
    lt1= lt.groupby("State")["Transacion_amount"].sum().sort_values(ascending= False)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "State", y= "Transacion_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)
def ques10():
    dt= df3[["Dis_Name", "Tran_Amount"]]
    dt1= dt.groupby("Dis_Name")["Tran_Amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Dis_Name", y= "Tran_Amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)


if  selected == "Tables":
    a= st.radio("Select an option", ["Transaction","User"])
    if a =="Transaction":
      b= st.selectbox("Select your questions",("Aggregation","Map","Top"))
      if b== "Aggregation" :
         st.table(df1)
      if b == "Map":
         st.table(df2)  
      if b == "Top":
         st.table(df3)    
    if a == "User":
        c= st.selectbox("Select your questions",("Aggregation","Map","Top")) 
        if c == "Aggregation" :
         st.table(df4) 
        if c == "Map":
          st.table(df5)    
        if c == "Top":
          st.table(df6)


if selected == "Transactions-Insights":
    a=st.radio("Select the transaction",["Aggregation_Transaction",
                                        "Map_transaction",
                                        "Top_transaction"])
    if a=="Aggregation_Transaction":
        years= st.slider("Select the Year",df1["Year"].min(),df1["Year"].max(),df1["Year"].min())
        Transcation_amount_count_Y(df1, years)
        a=st.selectbox("Select Transaction Type",("Recharge & bill payments",
                                                   'Peer-to-peer payments',
                                                    'Merchant payments',
                                                    'Financial Services',
                                                    'Others'))
        Transaction_type(df1,a)    
 
    if a == "Map_transaction":
                State_name = st.selectbox("Select State Names",('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                            'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                            'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                                            'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                            'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                            'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                            'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                            'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                            'Uttarakhand', 'West Bengal'))
                
                selected_year = st.selectbox("Select Year", (2018,
                                                        2019,
                                                        2020,
                                                        2021,
                                                        2022,
                                                        2023))
                Map_transaction(df3, State_name, selected_year)
                Map(df3)

    if a == "Top_transaction":
        State_name = st.selectbox("Select State Names",('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                            'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                            'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                                            'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                            'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                            'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                            'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                            'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                            'Uttarakhand', 'West Bengal'))
        Quarter = st.selectbox("Select Quarter",(1,
                                                 2,
                                                 3,
                                                 4))
        Top_tran(df5,Quarter,State_name)

elif   selected == "Users-Insights":
    a=st.radio("Select the transaction",["Aggregation_User",
                                        "Map_User",
                                        "Top_User"])   
    if a==  "Aggregation_User":
            State_name = st.selectbox("Select State Names",('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                            'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                            'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                                            'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                            'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                            'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                            'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                            'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                            'Uttarakhand', 'West Bengal'))
                
            selected_year = st.selectbox("Select Year", (2018,
                                                        2019,
                                                        2020,
                                                        2021,
                                                        2022,
                                                        2023))
                 
            Agg_User(selected_year,State_name)
            Agg_user_map(df2)

    if a == "Map_User":
            State_name = st.selectbox("Select State Names",('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                            'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                            'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                                            'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                            'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                            'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                            'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                            'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                            'Uttarakhand', 'West Bengal'))
                
            selected_year = st.selectbox("Select Year", (2018,
                                                        2019,
                                                        2020,
                                                        2021,
                                                        2022,
                                                        2023))
            Map_User(df4, State_name, selected_year)
            Map_user_(df4)

    if a== "Top_User":
        State_name = st.selectbox("Select State Names",('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                            'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                            'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                                            'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                            'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                            'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                            'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                            'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                            'Uttarakhand', 'West Bengal'))
        Quarter = st.selectbox("Select Quarter",(1,
                                                 2,
                                                 3,
                                                 4))  
              
        
        Top_user(df6,Quarter,State_name) 
        selected_year = st.selectbox("Select Year", (2018,
                                                        2019,
                                                        2020,
                                                        2021,
                                                        2022,
                                                        2023))
        Top_user_line(df6,Quarter,selected_year)

elif selected=="Analysis":
    a= st.selectbox("Select Questions",("1.LOWEST TRANSACTION AMOUNT and STATES",
                                        "2.Top Mobile Brands of Transaction_count",
                                        "3.TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                                        "4.TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                                        "5.Highest Top 10 States With AppOpens",
                                        "6.Lowest 10 States With AppOpens",
                                        "7.STATES WITH LOWEST TRANSACTION COUNT",
                                        "8.STATES WITH HIGHEST TRANSACTION COUNT",
                                        "9.HIGHEST TRANSACTION AMOUNT and STATES",
                                        "10.DISTRICTS WITH LOWEST TRANSACTION AMOUNT"))
    if a=="1.LOWEST TRANSACTION AMOUNT and STATES":
        ques1()
    if a=="2.Top Mobile Brands of Transaction_count":
        ques2()   
    if a=="3.TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT":
        ques3()
    if a=="4.TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT":
        ques4()
    if a=="5.Highest Top 10 States With AppOpens":
        ques5()
    if a=="6.Lowest 10 States With AppOpens":
        ques6()
    if a=="7.STATES WITH LOWEST TRANSACTION COUNT":
        ques7()
    if a=="8.STATES WITH HIGHEST TRANSACTION COUNT":
        ques8()
    if a=="9.HIGHEST TRANSACTION AMOUNT and STATES":
        ques9()
    if a=="10.DISTRICTS WITH LOWEST TRANSACTION AMOUNT":
        ques10()                                 

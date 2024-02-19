import pandas as pd
import json
import os


import mysql.connector

dbs=mysql.connector.connect(
    host="localhost",
    user="root@localhost",
    password="Charu@9601",
    database='PhonePay',
    port='3306'
)
cursor=dbs.cursor()



Agg_tran_clm={'State':[], 'Year':[],'Quater':[],'Transacion_type':[], 'Transacion_count':[], 'Transacion_amount':[]}

path = "C:\\Users\\charu\\OneDrive\\Desktop\\kc.py\\pulse\\data\\aggregated\\transaction\\country\\india\\state"
state_list=os.listdir(path)
for i in state_list:
    p_i = os.path.join(path, i)
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=os.path.join(p_i,j)
        Agg_j=os.listdir(p_j)
        for k in Agg_j:
            p_it=os.path.join(p_j,k) 
            Data=open(p_it,'r')
            D=json.load(Data)
            for z in D['data']['transactionData']:
              Name=z['name']
              count=(z['paymentInstruments'][0]['count'])
              amount=(z['paymentInstruments'][0]['amount'])
              Agg_tran_clm['Transacion_type'].append(Name)
              Agg_tran_clm['Transacion_count'].append(count)
              Agg_tran_clm['Transacion_amount'].append(amount)
              Agg_tran_clm['State'].append(i)
              Agg_tran_clm['Year'].append(j)
              Agg_tran_clm['Quater'].append(int(k.strip('.json')))

              d1=pd.DataFrame(Agg_tran_clm)

d1["State"]=d1["State"].str.replace("-"," ")
d1["State"]=d1["State"].str.title()
d1["State"] = d1["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
d1['State'] = d1['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", 'Dadra and Nagar Haveli and Daman and Diu')

Agg_user_clm={'State':[], 'Year':[],'Quater':[],'Brand':[],'Count':[],'Percentage':[]}

path="C:\\Users\\charu\\OneDrive\\Desktop\\kc.py\\pulse\\data\\aggregated\\user\\country\\india\\state"
state_list=os.listdir(path)
for i in state_list:
    p_i = os.path.join(path, i)
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=os.path.join(p_i,j)
        Agg_j=os.listdir(p_j)
        for k in Agg_j:
            p_it=os.path.join(p_j,k) 
            Data=open(p_it,'r')
            D=json.load(Data)
            try:
                for z in D['data']['usersByDevice']:
                    Brand=z['brand']
                    Count='{:,.0f}'.format(z['count'])
                    Percentage=(z['percentage'])
                    Agg_user_clm['State'].append(i)
                    Agg_user_clm['Year'].append(j)
                    Agg_user_clm['Quater'].append(int(k.strip('.json')))
                    Agg_user_clm['Brand'].append(Brand)
                    Agg_user_clm['Count'].append(Count)
                    Agg_user_clm['Percentage'].append(Percentage)
                    d2=pd.DataFrame(Agg_user_clm)
                    
            except:
                pass
d2["State"]=d2["State"].str.replace("-"," ")
d2["State"]=d2["State"].str.title()
d2["State"] = d2["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
d2['State'] = d2['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", 'Dadra and Nagar Haveli and Daman and Diu')

map_tran_clm={'State':[], 'Year':[],'Quater':[],'Dis_Name':[],'People_Count':[],'Tran_Amount':[]}
path="C:\\Users\\charu\\OneDrive\\Desktop\\kc.py\\pulse\\data\\map\\transaction\\hover\\country\\india\\state"

state_list=os.listdir(path)
for i in state_list:
    p_i = os.path.join(path, i)
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=os.path.join(p_i,j)
        Agg_j=os.listdir(p_j)
        for k in Agg_j:
            p_it=os.path.join(p_j,k) 
            Data=open(p_it,'r')
            D=json.load(Data)
            for z in D['data']['hoverDataList']:
                Dis_Name=z['name']
                People_Count='{:,.0f}'.format(z['metric'][0]['count'])
                Amount='{:,.0f}'.format(z['metric'][0]['amount'])
                map_tran_clm['State'].append(i)
                map_tran_clm['Year'].append(j)
                map_tran_clm['Quater'].append(int(k.strip('.json')))
                map_tran_clm['Dis_Name'].append(Dis_Name)
                map_tran_clm['People_Count'].append(People_Count)
                map_tran_clm['Tran_Amount'].append(Amount)
                d3=pd.DataFrame(map_tran_clm)
                
d3["State"]=d3["State"].str.replace("-"," ")
d3["State"]=d3["State"].str.title()
d3["State"] = d3["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
d3['State'] = d3['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", 'Dadra and Nagar Haveli and Daman and Diu')
               
map_user_clm={'State':[], 'Year':[],'Quater':[],'District':[],'Registered_User':[],'Opened_Apps':[]}
path="C:\\Users\\charu\\OneDrive\\Desktop\\kc.py\\pulse\\data\\map\\user\\hover\\country\\india\\state"

state_list=os.listdir(path)
for i in state_list:
    p_i = os.path.join(path, i)
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=os.path.join(p_i,j)
        Agg_j=os.listdir(p_j)
        for k in Agg_j:
            p_it=os.path.join(p_j,k) 
            Data=open(p_it,'r')
            D=json.load(Data)
            for z in D['data']['hoverData'].items():
                District=z[0]
                Register_Data='{:,.0f}'.format(z[1]['registeredUsers'])
                Appeopens='{:,.0f}'.format(z[1]['appOpens'])
                map_user_clm['State'].append(i)
                map_user_clm['Year'].append(j)
                map_user_clm['Quater'].append(int(k.strip('.json')))
                map_user_clm['District'].append(District)
                map_user_clm['Registered_User'].append(Register_Data)
                map_user_clm['Opened_Apps'].append(Appeopens)
                d4=pd.DataFrame(map_user_clm)

d4["State"]=d4["State"].str.replace("-"," ")
d4["State"]=d4["State"].str.title()
d4["State"] = d4["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
d4['State'] = d4['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", 'Dadra and Nagar Haveli and Daman and Diu')
                            
top_tran_clm={'State':[], 'Year':[],'Quater':[],'Entity_Name':[],'Count':[],'Amount':[]}
path="C:\\Users\\charu\\OneDrive\\Desktop\\kc.py\\pulse\\data\\top\\transaction\\country\\india\\state"

state_list=os.listdir(path)
for i in state_list:
    p_i = os.path.join(path, i)
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=os.path.join(p_i,j)
        Agg_j=os.listdir(p_j)
        for k in Agg_j:
            p_it=os.path.join(p_j,k) 
            Data=open(p_it,'r')
            D=json.load(Data)
            for z in D['data']['pincodes']:
                Entity_Name=z['entityName']
                Count='{:,.0f}'.format(z['metric']['count'])
                Amount='{:,.0f}'.format(z['metric']['amount'])
                top_tran_clm['State'].append(i)
                top_tran_clm['Year'].append(j)
                top_tran_clm['Quater'].append(int(k.strip('.json')))
                top_tran_clm['Entity_Name'].append(Entity_Name)
                top_tran_clm['Count'].append(Count)
                top_tran_clm['Amount'].append(Amount)
                d5=pd.DataFrame(top_tran_clm)

d5["State"]=d5["State"].str.replace("-"," ")
d5["State"]=d5["State"].str.title()
d5["State"] = d5["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
d5['State'] = d5['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", 'Dadra and Nagar Haveli and Daman and Diu')
                  
top_user_clm={'State':[], 'Year':[],'Quater':[],'Name':[],'RegisteredUsers':[]}
path="C:\\Users\\charu\\OneDrive\\Desktop\\kc.py\\pulse\\data\\top\\user\\country\\india\\state"

state_list=os.listdir(path)
for i in state_list:
    p_i = os.path.join(path, i)
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=os.path.join(p_i,j)
        Agg_j=os.listdir(p_j)
        for k in Agg_j:
            p_it=os.path.join(p_j,k) 
            Data=open(p_it,'r')
            D=json.load(Data)
            for z in D['data']['pincodes']:
                Name=z['name']
                Register_no='{:,.0f}'.format(z['registeredUsers'])
                top_user_clm['State'].append(i)
                top_user_clm['Year'].append(j)
                top_user_clm['Quater'].append(int(k.strip('.json'))) 
                top_user_clm['Name'].append(Name)  
                top_user_clm['RegisteredUsers'].append(Register_no) 
                d6=pd.DataFrame(top_user_clm)        

d6["State"]=d6["State"].str.replace("-"," ")
d6["State"]=d6["State"].str.title()
d6["State"] = d6["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
d6['State'] = d6['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", 'Dadra and Nagar Haveli and Daman and Diu')
#def table1():
drop='''drop table if exists Aggregated_Transaction'''
cursor.execute(drop)
dbs.commit()

d1['Transacion_count'] = d1['Transacion_count'].replace(',', '', regex=True).astype(float)
d1['Transacion_amount'] = d1['Transacion_amount'].replace(',', '', regex=True).astype(float)

a= '''create table if not exists Aggregated_Transaction(State varchar(100),
                                                            Year bigint,
                                                            Quater bigint,
                                                            Transacion_type varchar(100),
                                                            Transacion_count  bigint,
                                                            Transacion_amount bigint)'''

cursor.execute(a)
dbs.commit()

for index,row in d1.iterrows():
    inser_table='''insert into Aggregated_Transaction(State,
                                                    Year,
                                                    Quater,
                                                    Transacion_type,
                                                    Transacion_count,
                                                    Transacion_amount)
                                                    
                                                    values(%s,%s,%s,%s,%s,%s)'''
    values=(row['State'],
            row['Year'],
            row['Quater'],
            row['Transacion_type'],
            row['Transacion_count'],
            row['Transacion_amount'])
    try:

        cursor.execute(inser_table,values)
        dbs.commit()

    except:
        print('d')    

def table2():
        drop='''drop table if exists Aggregated_User'''
        cursor.execute(drop)
        dbs.commit()

        d2['Count'] = d2['Count'].replace(',', '', regex=True).astype(float)

        a='''create table if not exists Aggregated_User(State varchar(100),
                                                        Year bigint,
                                                        Quater bigint,
                                                        Brand varchar(100),
                                                        Count bigint,
                                                        Percentage float)'''

        cursor.execute(a)
        dbs.commit()

        for index,row in d2.iterrows():
            inser_table='''insert into Aggregated_User(State,
                                                        Year,
                                                        Quater,
                                                        Brand,
                                                        Count,
                                                        Percentage)
                                                            
                                                    values(%s,%s,%s,%s,%s,%s)'''
            values=(row['State'],
                    row['Year'],
                    row['Quater'],
                    row['Brand'],
                    row['Count'],
                    row['Percentage'])
            try:

                cursor.execute(inser_table,values)
                dbs.commit()

            except mysql.connector.Error as err:
                    print("Error:", err) 

def table3():
    drop='''drop table if exists map_transaction'''
    cursor.execute(drop)
    dbs.commit()

    d3['People_Count'] = d3['People_Count'].replace(',', '', regex=True).astype(float)
    d3['Tran_Amount'] = d3['Tran_Amount'].replace(',', '', regex=True).astype(float)

    a='''create table if not exists map_transaction(State varchar(100),
                                                    Year bigint,
                                                    Quater bigint,
                                                    Dis_Name varchar(100),
                                                    People_Count bigint,
                                                    Tran_Amount float)'''

    cursor.execute(a)
    dbs.commit()

    for index,row in d3.iterrows():
        inser_table='''insert into map_transaction(State,
                                                    Year,
                                                    Quater,
                                                    Dis_Name,
                                                    People_Count,
                                                    Tran_Amount)
                                                        
                                                values(%s,%s,%s,%s,%s,%s)'''
        values=(row['State'],
                row['Year'],
                row['Quater'],
                row['Dis_Name'],
                row['People_Count'],
                row['Tran_Amount'])
        try:

            cursor.execute(inser_table,values)
            dbs.commit()

        except mysql.connector.Error as err:
                        print("Error:", err)    

def table4():
    drop='''drop table if exists map_User'''
    cursor.execute(drop)
    dbs.commit()

    d4['Registered_User'] = d4['Registered_User'].replace(',', '', regex=True).astype(float)
    d4['Opened_Apps'] = d4['Opened_Apps'].replace(',', '', regex=True).astype(float)

    a='''create table if not exists map_User(State varchar(100),
                                                    Year bigint,
                                                    Quater bigint,
                                                    District varchar(100),
                                                    Registered_User bigint,
                                                    Opened_Apps bigint)'''

    cursor.execute(a)
    dbs.commit()

    for index,row in d4.iterrows():
        inser_table='''insert into map_User(State,
                                                    Year,
                                                    Quater,
                                                    District,
                                                    Registered_User,
                                                    Opened_Apps)
                                                        
                                                values(%s,%s,%s,%s,%s,%s)'''
        values=(row['State'],
                row['Year'],
                row['Quater'],
                row['District'],
                row['Registered_User'],
                row['Opened_Apps'])
        try:

            cursor.execute(inser_table,values)
            dbs.commit()

        except mysql.connector.Error as err:
                        print("Error:", err)  

def table5():
    drop='''drop table if exists Top_transaction'''
    cursor.execute(drop)
    dbs.commit()

    d5['Count'] = d5['Count'].replace(',', '', regex=True).astype(float)
    d5['Amount'] = d5['Amount'].replace(',', '', regex=True).astype(float)

    a='''create table if not exists Top_transaction(State varchar(100),
                                                    Year bigint,
                                                    Quater bigint,
                                                    Entity_Name bigint,
                                                    Count bigint,
                                                    Amount bigint)'''

    cursor.execute(a)
    dbs.commit()

    for index,row in d5.iterrows():
        inser_table='''insert into Top_transaction(State,
                                                    Year,
                                                    Quater,
                                                    Entity_Name,
                                                    Count,
                                                    Amount)
                                                        
                                                values(%s,%s,%s,%s,%s,%s)'''
        values=(row['State'],
                row['Year'],
                row['Quater'],
                row['Entity_Name'],
                row['Count'],
                row['Amount'])
        try:

            cursor.execute(inser_table,values)
            dbs.commit()

        except mysql.connector.Error as err:
                        print("Error:", err)     

def table6():
    drop='''drop table if exists Top_User'''
    cursor.execute(drop)
    dbs.commit()
    d6["RegisteredUsers"]=d6["RegisteredUsers"].replace(",","",regex=True).astype(float)

    a='''create table if not exists Top_User(State varchar(100),
                                            Year bigint,
                                            Quater bigint,
                                            Name bigint,
                                            RegisteredUsers bigint
                                            )'''

    cursor.execute(a)
    dbs.commit()

    for index,row in d6.iterrows():
        inser_table='''insert into Top_User(State,
                                                    Year,
                                                    Quater,
                                                    Name,
                                                    RegisteredUsers)
                                                        
                                                values(%s,%s,%s,%s,%s)'''
        values=(row['State'],
                row['Year'],
                row['Quater'],
                row['Name'],
                row['RegisteredUsers']
            )
        try:

            cursor.execute(inser_table,values)
            dbs.commit()

        except:
            print('d')                                                                           
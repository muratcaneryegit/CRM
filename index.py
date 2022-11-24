import streamlit as st
import sqlite3
import pandas as pd

conn=sqlite3.connect("crm.db")
c=conn.cursor()

def brandtable():
    c.execute(""" CREATE TABLE IF NOT EXISTS brands(
    name TEXT 
    )""")
    conn.commit()
def producttable():
    c.execute("""CREATE TABLE IF NOT EXISTS products(
    name TEXT,
    brand TEXT,
    price REAL,
    stock INTEGER
    )""")
    conn.commit()

def addproduct(name,brand,price,stock):
    c.execute("INSERT INTO products VALUES (?,?,?,?)",(name,brand,price,stock))
    conn.commit()


def addbrand(name):
    name=name.upper()
    c.execute("INSERT INTO brands VALUES (?)",(name,))
    conn.commit()

def gettable(tablename,number="*"):
    make="SELECT rowid, * FROM "+tablename
    c.execute(make)
    if number=="*":
        result=c.fetchall()
    else:
        result=c.fetchmany(number)

    return result

def editbrand(name,newname):
    c.execute("UPDATE brands SET name=? WHERE name=?",(newname,name))
    conn.commit()

def deletebrand(name):
    c.execute("DELETE FROM brands WHERE name=?",(name,))
    conn.commit()

def branddf(tablename,number="*"):
    make= "SELECT rowid, * FROM " + tablename
    c.execute(make)
    if number == "*":
        result = c.fetchall()
    else:
        result = c.fetchmany(number)

    df=pd.DataFrame(result)
    df.columns=["ID","Name"]
    return df


def productdf(tablename,number="*"):
    make = "SELECT rowid, * FROM " + tablename
    c.execute(make)
    if number == "*":
        result = c.fetchall()
    else:
        result = c.fetchmany(number)

    df=pd.DataFrame(result)
    df.columns=["ID","Name","Brand","Price","Stock"]
    return df

brandtable()
producttable()
menu=st.sidebar.selectbox("Please Select",["Home Page","Brand","Product","Order"])

if menu =="Brand":

    menu2=st.sidebar.selectbox("Please Select",["Add Brand","Edit Brand","Update Brand"])
    if menu2=="Add Brand":
        with st.form("addbrand",clear_on_submit=True):
            name=st.text_input("Brand Name")
            submitted=st.form_submit_button("Add Brand")
            if submitted:
                addbrand(name)
                st.success("Added")
                st.balloons()
        st.table(branddf("brands",number="*"))

    elif menu2=="Edit Brand":
        with st.form("editbrand",clear_on_submit=True):
            name=st.selectbox("Select Brand",list(branddf("brands")['Name']))
            newname=st.text_input("New Name")
            submitted=st.form_submit_button("Edit")
            if submitted:
                editbrand(name,newname)
                st.success("Edited")
                st.balloons()
        st.table(branddf("brands",number="*"))

    elif menu2=="Delete Brand":
        with st.form("deletebrand",clear_on_submit=True):
            name=st.selectbox("Choose Brand",list(branddf("brands")['Name']))
            submitted = st.form_submit_button("Delete")
            if submitted:
                deletebrand(name)
                st.success("Deleted")
                st.snow()
        st.table(branddf("brands", number="*"))


if menu=="Product":
    menu2=st.selectbox("Please Select",["Add Product","Edit Product","Delete Product"])
    if menu2=="Add Product":
        with st.form("addproduct2",clear_on_submit=True):
            name=st.text_input("Product Name")
            brand=st.selectbox("Select Brand",list(branddf("brands")['Name']))
            price=st.number_input("Enter Price")
            stock=st.number_input("Enter Stock",step=1,value=100)
            submitted=st.form_submit_button("add")
            if submitted:
                addproduct(name, brand, price, stock)
                st.success("The Product Has Been Successfully Added")
                st.balloons()

        st.table(productdf("products", number="*"))

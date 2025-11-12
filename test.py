import pandas as pd
import streamlit as st
file = st.file_uploader("Upload the excel file")
if file:
    df = pd.read_excel(file, header = [1,2,3])
    columns = []
    for i in df.columns:
        if "Unnamed" in i[1]:
            col_name = i[0]
        elif "Unnamed" in i[2]:
            col_name = "_".join([i[0], i[1]])
            if "Rs." in col_name:
                col_name = columns[-1]+"_Rs."
            elif "Value" in col_name:
                col_name = columns[-1]+"_Value"
        else:
            col_name = "_".join([i[0], i[1], i[2]])
        columns.append(col_name)
    dataset = pd.read_excel(file, header=None)
    dataset.drop(index=[0,1,2,3], axis = 0, inplace = True)
    dataset.columns = columns
    v_name = st.text_input("Village Name")
    f_name=st.text_input("Family Head Name")
    category=st.text_input("Enter Category Name") 
    if st.button("Button"):
        v = dataset[
        (dataset["Village Name"] == v_name) |
        (dataset["Family Head Name"] == f_name) |
        (dataset["Catagiry"] == category)]
        st.write("Data")
        st.dataframe(v)

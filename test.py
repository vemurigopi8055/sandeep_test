import pandas as pd
import streamlit as st

if "show_search" not in st.session_state:
    st.session_state.show_search = False

if "show_count" not in st.session_state:
    st.session_state.show_count = False

def show_search_ui():
    st.session_state.show_search = True
    st.session_state.show_count = False

def show_count_ui():
    st.session_state.show_count = True
    st.session_state.show_search = False


file = st.file_uploader("Upload the Excel File")

if file:
    df = pd.read_excel(file, header=[1,2,3])
    columns = []

    for i in df.columns:
        if "Unnamed" in i[1]:
            col_name = i[0]
        elif "Unnamed" in i[2]:
            col_name = "_".join([i[0], i[1]])
            if "Rs." in col_name:
                col_name = columns[-1] + "_Rs."
            elif "Value" in col_name:
                col_name = columns[-1] + "_Value"
        else:
            col_name = "_".join([i[0], i[1], i[2]])
        columns.append(col_name)

    dataset = pd.read_excel(file, header=None)
    dataset.drop(index=[0,1,2,3], axis=0, inplace=True)
    dataset.columns = columns

    st.subheader("Choose an action")

    col1, col2 = st.columns(2)
    with col1:
        st.button("SEARCH", on_click=show_search_ui)
    with col2:
        st.button("COUNT", on_click=show_count_ui)

    if st.session_state.show_search:
        st.header("Search Filters")
        v_name = st.text_input("Village Name")
        p_name = st.text_input("Panchayat Name")
        m_name = st.text_input("Mandal Name")
        d_name = st.text_input("District Name")
        f_name = st.text_input("Family Head Name")

        category_options = dataset["Catagiry"].unique().tolist()
        category_options.insert(0, "select")
        category = st.selectbox("Choose Category", category_options)

        caste_options = dataset["Cast"].unique().tolist()
        caste_options.insert(0, "select")
        caste = st.selectbox("Choose Caste", caste_options)

        age_options = ["select", "below 18", "18 to 50", "above 50"]
        age = st.selectbox("Age Group", age_options)

        filter_list = [v_name, p_name, m_name, d_name, f_name,
                       category, caste, age]

        doc_list = ["Village Name", "Panchayat/ Area", "Mandal", "District",
                    "Family Head Name", "Catagiry", "Cast", "Age"]

        if st.button("RUN SEARCH"):
            result = dataset.copy()
            for i in range(len(filter_list)):
                if filter_list[i] in ['', 'select']:
                    continue
                else:
                    if doc_list[i] not in ["Numer of Child", "Physically Challanged Persons", "Age"]:
                        result = result[result[doc_list[i]] == filter_list[i]]
                    elif doc_list[i] == "Age":
                        if filter_list[i] == "below 18":
                            result = result[result[doc_list[i]] < 18]
                        elif filter_list[i] == "18 to 50":
                            result = result[(result[doc_list[i]] >= 18) & (result[doc_list[i]] < 50)]
                        else:
                            result = result[result[doc_list[i]] >= 50]

            st.subheader(f"Search Results:{len(result)}")
            st.dataframe(result)

    if st.session_state.show_count:
        st.header("Count Records")

        c_village = st.text_input("Village Name")
        gender_categrory = st.selectbox("Choose Gender Category", ["select", "Children", "Handicapped"])
        gender = st.selectbox("Gender", ["select", "Male", "Female"])

        if st.button("RUN COUNT"):
            result = dataset.copy()

            if c_village != "":
                result = result[result["Village Name"] == c_village]

            if gender_categrory != "select":
                if gender_categrory == "Children":
                    if gender == "Male":
                        result = result[result["Numer of Child_Male"]>0]
                        count = result["Numer of Child_Male"].sum()
                    else:
                        result = result[result["Numer of Child_Female"]>0]
                        count = result["Numer of Child_Female"].sum()
                else:
                    if gender == "Male":
                        result = result[result["Physically Challanged Persons_Male"]>0]
                        count = result["Physically Challanged Persons_Male"].sum()
                    else:
                        result = result[result["Physically Challanged Persons_Female"]>0]
                        count = result["Physically Challanged Persons_Female"].sum()

            st.subheader("Total Count")
            st.subheader(count)

# import pandas as pd
# import streamlit as st

# if "show_search" not in st.session_state:
#     st.session_state.show_search = False

# if "show_count" not in st.session_state:
#     st.session_state.show_count = False

# def show_search_ui():
#     st.session_state.show_search = True
#     st.session_state.show_count = False

# def show_count_ui():
#     st.session_state.show_count = True
#     st.session_state.show_search = False


# file = st.file_uploader("Upload the Excel File")

# if file:
#     df = pd.read_excel(file, header=[1,2,3])
#     columns = []

#     for i in df.columns:
#         if "Unnamed" in i[1]:
#             col_name = i[0]
#         elif "Unnamed" in i[2]:
#             col_name = "_".join([i[0], i[1]])
#             if "Rs." in col_name:
#                 col_name = columns[-1] + "_Rs."
#             elif "Value" in col_name:
#                 col_name = columns[-1] + "_Value"
#         else:
#             col_name = "_".join([i[0], i[1], i[2]])
#         columns.append(col_name)

#     dataset = pd.read_excel(file, header=None)
#     dataset.drop(index=[0,1,2,3], axis=0, inplace=True)
#     dataset.columns = columns

#     st.subheader("Choose an action")

#     col1, col2 = st.columns(2)
#     with col1:
#         st.button("SEARCH", on_click=show_search_ui)
#     with col2:
#         st.button("COUNT", on_click=show_count_ui)

#     if st.session_state.show_search:
#         st.header("Search Filters")
#         v_name = st.text_input("Village Name")
#         p_name = st.text_input("Panchayat Name")
#         m_name = st.text_input("Mandal Name")
#         d_name = st.text_input("District Name")
#         f_name = st.text_input("Family Head Name")

#         category_options = dataset["Catagiry"].unique().tolist()
#         category_options.insert(0, "select")
#         category = st.selectbox("Choose Category", category_options)

#         caste_options = dataset["Cast"].unique().tolist()
#         caste_options.insert(0, "select")
#         caste = st.selectbox("Choose Caste", caste_options)

#         age_options = ["select", "below 18", "18 to 50", "above 50"]
#         age = st.selectbox("Age Group", age_options)

#         filter_list = [v_name, p_name, m_name, d_name, f_name,
#                        category, caste, age]

#         doc_list = ["Village Name", "Panchayat/ Area", "Mandal", "District",
#                     "Family Head Name", "Catagiry", "Cast", "Age"]

#         if st.button("RUN SEARCH"):
#             result = dataset.copy()
#             for i in range(len(filter_list)):
#                 if filter_list[i] in ['', 'select']:
#                     continue
#                 else:
#                     if doc_list[i] not in ["Numer of Child", "Physically Challanged Persons", "Age"]:
#                         result = result[result[doc_list[i]] == filter_list[i]]
#                     elif doc_list[i] == "Age":
#                         if filter_list[i] == "below 18":
#                             result = result[result[doc_list[i]] < 18]
#                         elif filter_list[i] == "18 to 50":
#                             result = result[(result[doc_list[i]] >= 18) & (result[doc_list[i]] < 50)]
#                         else:
#                             result = result[result[doc_list[i]] >= 50]

#             st.subheader(f"Search Results:{len(result)}")
#             st.dataframe(result)

#     if st.session_state.show_count:
#         st.header("Count Records")

#         c_village = st.text_input("Village Name")
#         gender_categrory = st.selectbox("Choose Gender Category", ["select", "Children", "Handicapped"])
#         gender = st.selectbox("Gender", ["select", "Male", "Female"])

#         if st.button("RUN COUNT"):
#             result = dataset.copy()

#             if c_village != "":
#                 result = result[result["Village Name"] == c_village]

#             if gender_categrory != "select":
#                 if gender_categrory == "Children":
#                     if gender == "Male":
#                         result = result[result["Numer of Child_Male"]>0]
#                         count = result["Numer of Child_Male"].sum()
#                     else:
#                         result = result[result["Numer of Child_Female"]>0]
#                         count = result["Numer of Child_Female"].sum()
#                 else:
#                     if gender == "Male":
#                         result = result[result["Physically Challanged Persons_Male"]>0]
#                         count = result["Physically Challanged Persons_Male"].sum()
#                     else:
#                         result = result[result["Physically Challanged Persons_Female"]>0]
#                         count = result["Physically Challanged Persons_Female"].sum()

#             st.subheader("Total Count")
#             st.subheader(count)




























import pandas as pd
import streamlit as st
from PIL import Image

# --------- PAGE CONFIG ---------
st.set_page_config(
    page_title="S N I R D – Data Explorer",
    layout="wide",
    page_icon="🌾"
)

# --------- CUSTOM TEAL THEME (INPUTS + BUTTONS + SUCCESS BOX UPDATED) ---------
st.markdown("""
<style>

/* Main background */
body, .stApp {
    background-color: #ffffff;
}

/* Header divider */
hr {
    border: 1px solid #B2EBF2;
}

/* Labels */
label {
    font-weight: 600 !important;
    color: #004D40 !important;
}

/* -------- INPUT FIELDS (MATCH TEAL BUTTON COLOR) -------- */
input[type=text], select, textarea, .stTextInput>div>div>input {
    background-color: #E0F2F1 !important;
    border: 2px solid #009688 !important;
    color: #004D40 !important;
    border-radius: 6px !important;
    padding: 4px 10px !important;
    font-size: 15px !important;
}

input:hover, .stTextInput:hover input {
    border-color: #00796B !important;
}

input:focus, .stTextInput:focus-within input {
    border-color: #004D40 !important;
    box-shadow: 0 0 6px #80CBC4 !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background-color: #E0F2F1 !important;
    border: 2px solid #009688 !important;
    color: #004D40 !important;
    border-radius: 6px !important;
}

/* -------- BUTTONS -------- */
div.stButton > button {
    background-color: #009688 !important;
    color: white !important;
    border-radius: 8px;
    padding: 8px 18px;
    font-size: 16px;
    border: 1px solid #00796B;
}

div.stButton > button:hover {
    background-color: #00796B !important;
    border-color: #00695C !important;
}

/* -------- HEADERS -------- */
h2, h3, h4 {
    color: #004D40 !important;
    font-weight: 700 !important;
}

/* DataFrame header */
.dataframe thead th {
    background-color: #B2DFDB !important;
    color: #004D40 !important;
    font-weight: 700 !important;
}

/* -------- SUCCESS BOX: FULL WHITE -------- */
.stAlert {
    background-color: #00796B !important;
       /* White box */
    border: 2px solid #009688 !important;   /* Teal border */
    color: #004D40 !important;              /* Teal text */
    border-radius: 8px !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)



# --------- HEADER IMAGE (CENTERED) ---------
try:
    header_image = Image.open("testing.png")
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.image(header_image, width=650)
except:
    st.warning("Header image not found. Please place testing.png in the same folder.")

st.markdown("<hr>", unsafe_allow_html=True)



# --------- STATE HANDLERS ---------
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



# --------- FILE UPLOADER ---------
st.markdown("### 📤 Upload Excel File")
file = st.file_uploader("Choose .xlsx file", type=["xlsx"])



# ------------------------------------------------------
#                    PROCESS FILE
# ------------------------------------------------------
if file:

    df = pd.read_excel(file, header=[1, 2, 3])
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
    dataset.drop(index=[0, 1, 2, 3], axis=0, inplace=True)
    dataset.columns = columns


    # --------- ACTION BUTTONS ---------
    st.markdown("### ⚙️ Choose Action")
    col1, col2 = st.columns(2)

    with col1:
        st.button("🔍 SEARCH RECORDS", on_click=show_search_ui, use_container_width=True)
    with col2:
        st.button("📊 COUNT SUMMARY", on_click=show_count_ui, use_container_width=True)



    # ------------------------------------------------------
    #                    SEARCH SECTION
    # ------------------------------------------------------
    if st.session_state.show_search:
        st.markdown("## 🔍 Search Records")

        colA, colB, colC, colD = st.columns(4)
        with colA:
            v_name = st.text_input("🏘 Village")
        with colB:
            p_name = st.text_input("📍 Panchayat")
        with colC:
            m_name = st.text_input("🗺 Mandal")
        with colD:
            d_name = st.text_input("🌏 District")

        f_name = st.text_input("👨‍👩‍👦 Family Head")

        col1, col2 = st.columns(2)
        with col1:
            category_options = dataset["Catagiry"].unique().tolist()
            category_options.insert(0, "select")
            category = st.selectbox("📁 Category", category_options)

        with col2:
            caste_options = dataset["Cast"].unique().tolist()
            caste_options.insert(0, "select")
            caste = st.selectbox("🧬 Caste", caste_options)

        age = st.selectbox("🎂 Age Group", ["select", "below 18", "18 to 50", "above 50"])

        filter_list = [v_name, p_name, m_name, d_name, f_name, category, caste, age]
        doc_list = ["Village Name", "Panchayat/ Area", "Mandal", "District",
                    "Family Head Name", "Catagiry", "Cast", "Age"]

        if st.button("▶ RUN SEARCH", type="primary"):
            result = dataset.copy()

            for i in range(len(filter_list)):
                if filter_list[i] in ['', 'select']:
                    continue
                else:
                    if doc_list[i] not in ["Numer of Child", "Physically Challanged Persons", "Age"]:
                        result = result[result[doc_list[i]] == filter_list[i]]
                    elif doc_list[i] == "Age":
                        if filter_list[i] == "below 18":
                            result = result[result["Age"] < 18]
                        elif filter_list[i] == "18 to 50":
                            result = result[(result["Age"] >= 18) & (result["Age"] < 50)]
                        else:
                            result = result[result["Age"] >= 50]

            st.success(f"✔ {len(result)} Records Found")

            st.dataframe(result, use_container_width=True, height=350)



    # ------------------------------------------------------
    #                    COUNT SECTION
    # ------------------------------------------------------
    if st.session_state.show_count:
        st.markdown("## 📊 Count Summary")

        c_village = st.text_input("🏘 Village Name")
        gender_categrory = st.selectbox("👥 Group", ["select", "Children", "Handicapped"])
        gender = st.selectbox("⚧ Gender", ["select", "Male", "Female"])

        if st.button("▶ RUN COUNT"):
            result = dataset.copy()

            if c_village != "":
                result = result[result["Village Name"] == c_village]

            if gender_categrory != "select":
                if gender_categrory == "Children":
                    if gender == "Male":
                        result = result[result["Numer of Child_Male"] > 0]
                        count = result["Numer of Child_Male"].sum()
                    else:
                        result = result[result["Numer of Child_Female"] > 0]
                        count = result["Numer of Child_Female"].sum()
                else:
                    if gender == "Male":
                        result = result[result["Physically Challanged Persons_Male"] > 0]
                        count = result["Physically Challanged Persons_Male"].sum()
                    else:
                        result = result[result["Physically Challanged Persons_Female"] > 0]
                        count = result["Physically Challanged Persons_Female"].sum()

            st.success(f"### ✔ Total Count: **{count}**")

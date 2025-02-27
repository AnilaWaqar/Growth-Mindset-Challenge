import streamlit as st
import pandas as pandas
import os
from io import BytesIO

st.set_page_config(page_title = "Data Sweeper", layout='wide')

#custom css
st.markdown(
    """
<style>
.stApp{
background-color: black;
color: white;
}
</style>
""",unsafe_allow_html=True
)

#title and description 
st.title( "📀 Date Sweeper sterling integration by Anila Waqar")
st.write("Transform your files bewteen CVS and Excel formats with built in data cleaning and visiualization by creating a project in Q3")


#file uploader
uploaded_files = st.file_uploader("Upload your files(accepts CSV or Excel):", type=["cvs", "xlsx"], accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splittext(file.name)[-1].lower()


        if file_ext ==".CSV" :
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df =pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue

        #file details
        st.write("🔍 Preview the head of the DataFrame")
        st.dataFrame(df.head())

        #data cleaning options
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)


            with col1:
                if st.button(f"Remove duplicayes from the file : {file.name}"):
                    df. drop_duplicates(inplace=True)
                    st.write(" ✅ Duplicates Removed!")

                    with col2:
                        if st.button(f"Fill missing values for {file.name}"):
                            numeric_cols = df.select_dtypes(includes = ['number']).columns
                            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].means())
                            st.write("✅ Missing values have been filled")

                            st.subheader("🎯 Select Columns to Keep")
                            columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
                            df = df[columns]


    #data Visualization
                            st.subheader("📉 Data Visualization")
if st.checkbox(f"show visualization for {file.name}"):
    st.bar_chart(df.select_dtypes(includes='number').iloc[:,:2])

    #Conversion Options
    st.subheader("🔄 Conversion Options")
    conversions_type = st.radio(f"Convert {file.name} to:",["CVS , EXCEL"], key=file.name)
    if st.button(f"Convert{file.name}"):
        buffer = BytesIO()
        if conversions_type == "CSV":
            df.to.csv(buffer,index=False)
            file_name=file.name.replace(file_ext, ".csv")
            mime_type = "text/csv"

elif conversion_type == "Excel" :
    df.to.to_excel(buffer, index=False)
    file_name = file.name.replace(file_ext, ".xlsx")

mime_type ="aplication/vnd.openxmlformats-officedocumenet.spreadsheetml.sheet"
buffer.seek(0)

st.download_button(
    label=f"Download {file.name} as {conversions_type}",
    data=buffer,
    file_name=file_name,
    mime=mime_type

    st.success("🚀 All files processed successfully !")
)

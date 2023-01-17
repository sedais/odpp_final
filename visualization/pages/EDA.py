import streamlit as st
import os, sys
from pymongo import MongoClient
import pandas as pd

# appending the parent directory path
# sys.path.append(r'C:\Users\a892215\Projects\ODPP\ODPP\visualization')
#
# # importing the methods
# from visualization.web_scraper_ifixit import get_content_from_mongo


st.set_page_config(page_title="Exploratory Data Analysis", page_icon="📈")

st.markdown("# Exploratory Data Analysis 📈")
st.sidebar.header("Exploratory Data Analysis")
st.write(
    """Exploratory Data Analysis refers to the critical process of performing initial investigations on data so as to 
    discover patterns,to spot anomalies,to test hypothesis and to check assumptions with the help of summary statistics 
    and graphical representations. Here you can find Exploratory Data Analysis for the IFixIt Data!"""
)


@st.cache
def load_ifixit_data():
    print("Getting IFixIt data from mongo...")
    try:

        # Connect to the MongoDB server
        client = MongoClient(
            "mongodb+srv://odpp_user:lo0fVGfZLPZtWvQB@cluster0.65tresj.mongodb.net/?retryWrites=true&w=majority")

        # Choose the database and collection
        db = client.ifixit_db
        collection = db.phones

        data = pd.DataFrame(collection.find())
        print(data.head())
    except Exception as e:
        print(e)
    return data



# data = get_content_from_mongo()
# return data

print("in fix sentiment")
data = load_ifixit_data()
print(data.head())
s = data['score'].value_counts().sort_index()
df_chart = s.to_frame()
st.subheader("Number of Phones by Scores")
st.bar_chart(df_chart)
st.write(
    "Here we can see that  more than half of the analyzed phones, received a repairability score above the the mean value 5.6136")

s2 = data.groupby(['brand'])['score'].mean()
data_mean = s2.to_frame().reset_index()
data_mean['score'] = round(data_mean['score'], 2)
data_mean = data_mean.sort_values(by=['score'], ascending=False)
print(data_mean.head())
st.subheader("Average Score by Brand")
st.bar_chart(data_mean, x='brand', y='score')
st.write(
    "Highest average repairability score is achieved with Fairphone brand. The second place is shared by the Blackberry and Nokia. It is also to see that Apple and Samsung has relatively low scores due to previous models being less suitable for repairability.")

s3 = data.groupby(['year'])['score'].mean()
data_year = s3.to_frame().reset_index()
data_year['score'] = round(data_year['score'], 2)

st.subheader("Average Score by Year")
st.bar_chart(data_year, x='year', y='score')
st.write(
    "The correlation value of -0.24 between the year and the brand shows us there is a negative correlation between to variables. Meaning, as the year increases, the average repairability score decreases.")

# s4 = data.groupby(['year', 'brand'])['score'].mean()
# data_year_2 = s4.to_frame().reset_index()
# data_year_2['score'] = round(data_year_2['score'], 2)
#
# st.subheader("Average Score by Year and Brand")
# st.write("Highest average repairability score is achieved with Fairphone brand. The second place is shared by the Blackberry and Nokia. It is also to see that Apple and Samsung has relatively low scores due to previous models being less suitable for rapairability")
# st.bar_chart(data_year_2, x=('year', 'brand'), y='score')

df_apple = data[data['brand'] == "Apple"]
df_apple_mean = df_apple.groupby(['year'])['score'].mean()
df_apple = df_apple_mean.to_frame().reset_index()

st.subheader("Average Score by Year of Apple Phones")
st.line_chart(df_apple, x='year', y='score')
st.write(
    "Even though we can see Apple iPhone repairability has been increased over the years, we cannot say that it shows an upward trend.")

#df_samsung = data[(data['brand'] == "Samsung") | (data['brand'] == "Apple")]
df_samsung = data[data['brand'] == "Samsung"]
print("here samsung")
print(df_samsung)
df_samsung_mean = df_samsung.groupby(['year'])['score'].mean()
df_samsung = df_samsung_mean.to_frame().reset_index()

st.subheader("Average Score by Year of Samsung Phones")
st.line_chart(df_samsung, x='year', y='score')
st.write(
    "Interestingly Samsung phones shows a downward trend over the year, meaning as the technology advanced repairability of the Samsung phones have been decreased.")

# s = data[data['brand'] == "Samsung"][['score', 'year']]
# a = data[data['brand'] == "Apple"][['score', 'year']]
# chart_data = pd.DataFrame(
#     {'apple': a,
#     'samsung': s}, index='year')
# st.line_chart(chart_data)

brand_list = data.brand.unique()
selected_brand = st.selectbox('Select a brand', brand_list)
st.write(f'selected: {selected_brand}')
df=data[data['brand'] == selected_brand]
df_mean=df.groupby(['year'])['score'].mean()
st.line_chart(df_mean.to_frame().reset_index(), x='year', y='score')



status_text = st.sidebar.empty()
# status_text.text("See the takeaways at the end of the page")

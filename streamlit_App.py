import streamlit as st
import pandas as pd
import sklearn
import xgboost
import category_encoders
import joblib
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
geolocator = Nominatim(user_agent="latlong")
model = joblib.load("Final_Model_Group_4.pkl")
inputs = joblib.load("Inputs_Group_4.pkl")


def Prediction(Airline, Source,Destination,Stops,Day_of_Journey_in_numbers,Month_of_Journey,Dep_Hour,Arrival_Hour,Arrival_Period,Dep_Period,Duration_Categorized,Distance_Categorized, Meal):
    df = pd.DataFrame(columns=inputs)
    df.at[0,'Airline'] = Airline
    df.at[0,'Source'] = Source
    df.at[0,'Destination'] = Destination
    df.at[0,'Stops'] = Stops
    df.at[0,'Day_of_Journey_in_numbers'] = Day_of_Journey_in_numbers
    df.at[0,'Month_of_Journey'] = Month_of_Journey
    df.at[0,'Dep_Hour'] = Dep_Hour
    df.at[0,'Arrival_Hour'] = Arrival_Hour
    df.at[0,'Arrival_Period'] = Arrival_Period
    df.at[0,'Dep_Period'] = Dep_Period
    df.at[0,'Duration_Categorized'] = Duration_Categorized
    df.at[0,'Distance_Categorized'] = Distance_Categorized
    df.at[0,'Meal'] = Meal
    result = model.predict(df)
    return result[0]
    
def get_day_period(r):
    if int(r) in range(5,13) : 
        return "Morning"
    elif int(r) in range(13,18):
        return "Afternoon"
    elif int(r) in range(18,23):
        return "Evening"
    else:
        return "Night" 
        
def get_distance_categorized(source, destination):
    loc = geolocator.geocode(source)
    source_lat = loc.raw['lat']
    soruce_long = loc.raw["lon"]
    source_tuple = (source_lat,soruce_long)
    
    loc = geolocator.geocode(destination)
    destination_lat = loc.raw['lat']
    destination_long = loc.raw["lon"]
    destination_tuple = (destination_lat,destination_long)
    distance = great_circle(source_tuple , destination_tuple).kilometers
    if distance <= 1000 :
        return 'short Dist'
    elif distance <=2000:
        return 'Medium Dist'
    else :
        return 'Long Dist'

def main():
    st.title("Flights Price Prediction")
    Airline = st.selectbox("Airline" , ['Air India', 'Jet Airways', 'IndiGo', 'SpiceJet','Multiple carriers', 'GoAir', 'Vistara', 'Air Asia'])
    Source = st.selectbox("Source" , ['Kolkata', 'Delhi', 'Banglore', 'Chennai', 'Mumbai'])
    Destination = st.selectbox("Destination" , ['Banglore', 'Cochin', 'New Delhi', 'Kolkata', 'Delhi', 'Hyderabad'])
    Stops = st.selectbox("Stops" , [2, 1, 0, 3, 4])
    Day_of_Journey_in_numbers = st.selectbox("Day_of_Journey_in_numbers" , range(1,32))
    Month_of_Journey = st.selectbox("Month_of_Journey" ,['May', 'June', 'March', 'April'] )
    Dep_Hour = st.selectbox("Dep_Hour" , range(0,24))
    Arrival_Hour = st.selectbox("Arrival_Hour" , range(0,24))
    Dep_Period = get_day_period(Dep_Hour)
    Arrival_Period = get_day_period(Arrival_Hour)
    Duration = st.slider("Duration" , min_value=100 , max_value=1000 , value = 120 , step = 20)
    if Duration <= 750 :
        Duration_Categorized =  'short Duration'
    elif Duration<=1500:
        Duration_Categorized =  'Medium Duration'
    else:
        Duration_Categorized =  'Long Duration'

    Distance_Categorized = get_distance_categorized(Source,Destination )
    Meal = st.selectbox("Meal" , [0,1])
    if st.button("Predict"):
        result = Prediction(Airline, Source,Destination,Stops,Day_of_Journey_in_numbers,Month_of_Journey,Dep_Hour,Arrival_Hour,Arrival_Period,Dep_Period,Duration_Categorized,Distance_Categorized, Meal)
        st.text(result)
main()
    
    

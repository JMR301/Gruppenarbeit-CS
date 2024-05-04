import streamlit as st

st.title("Hallo Nutzer/in!")

#Suchleiste
st.text_input ("Welchen Influencer möchtest du gerne suchen?", key="influencer search")
 #die Variable x kann dann weiterverwendet werden um den Influencer auszugeben

#Filter
st.header ("Deine Filter")

#Filter1 
st.subheader ("Abonnierende:") 
import streamlit as st

values = st.slider(
    'Wie viele Abonnierende soll dein Influencer haben?',
    0, 100000, (250, 750)) #CR7 Followeranzahl als Maximum auswählen
st.write('Deine aktuell Abonnierenden Wunschzahl:', values)

#Filter2
st.subheader ("Land der Zielgruppe:") 
import streamlit as st

options = st.multiselect(
    'In welchem Land soll deine Zielgruppe angesprochen werden?',
    ['Spanien', 'USA'],
    ['Spanien'])

st.write('Dein ausgewähltes Land:', options)

#Filter3
st.subheader ("Kategorie:") 
import streamlit as st

options = st.multiselect(
    'In welcher Katogorie soll dein Influencer/in tätig sein?',
    ['Musik', 'Kino/Schauspiel', 'Sport', 'Lifestyle'],
    ['Musik'])

st.write('Deine ausgewählte Kategorie:', options)

#Filter4
st.subheader ("Durchschnittliche Likes:") 
import streamlit as st

values = st.slider(
    'Wie viele Likes soll dein/e Influener/in durchschnittlich haben?',
    0, 30000, (500, 1000)) #Anpassen
st.write('Values:', values)

#Filter5
st.subheader ("Engagement Rate:") 
import streamlit as st

values = st.slider(
    'Wie hoch soll die Engagement Rate deines/er Influencer/in sein?',
    0.00, 1.00, (0.50, 0.58)) #Anpassen
st.write('Values:', values)

st.link_button("Finde deine Influencer/innen", "https://streamlit.io/gallery") #enter valid URL
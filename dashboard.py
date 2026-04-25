import streamlit as st
import boto3, json

s3 = boto3.client('s3', endpoint_url='http://localhost:9000', 
                  aws_access_key_id='minioadmin', aws_secret_access_key='minioadmin')

st.title("📊 Tableau de Bord : Tensions Iran-USA")

try:
    obj = s3.get_object(Bucket='gold', Key='rapport_tendances_conflit.json')
    data = json.loads(obj['Body'].read().decode('utf-8'))

    st.subheader("Nombre d'articles par source")
    st.bar_chart(data['articles_par_source'])

    st.subheader("Top 10 des mots-clés dominants")
    st.table(list(data['mots_cles'].items()))
    
    st.write(f"Dernière mise à jour : {data['total']} articles analysés.")
except Exception as e:
    st.error(f"Erreur d'affichage : {e}")
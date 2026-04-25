import boto3, json, re

s3 = boto3.client('s3', endpoint_url='http://localhost:9000', 
                  aws_access_key_id='minioadmin', aws_secret_access_key='minioadmin')

def nettoyer_html(html):
    return re.sub('<[^<]+?>', '', str(html)).strip()

def transformer_donnees():
    reponse = s3.list_objects_v2(Bucket='bronze')
    if 'Contents' not in reponse:
        print("Bucket Bronze vide.")
        return

    for obj in reponse['Contents']:
        key = obj['Key']
        try:
            data_s3 = s3.get_object(Bucket='bronze', Key=key)
            article = json.loads(data_s3['Body'].read().decode('utf-8'))
            
            # Vérification CRITIQUE : s'assurer que c'est un dictionnaire
            if isinstance(article, dict) and 'html_content' in article:
                article['contenu_propre'] = nettoyer_html(article['html_content'])
                article['langue'] = "FR" if "hespress" in article['url'].lower() else "EN"
                
                if len(article['contenu_propre']) > 15:
                    del article['html_content'] 
                    s3.put_object(Bucket='silver', Key=f"silver_{key}", Body=json.dumps(article))
            else:
                print(f"⚠️ Format ignoré pour : {key}")
        except Exception as e:
            print(f"❌ Erreur sur {key} : {e}")
            
    print("✨ Transformation Silver terminée sans erreur.")

if __name__ == "__main__":
    transformer_donnees()
import boto3, json

s3 = boto3.client('s3', endpoint_url='http://localhost:9000', 
                  aws_access_key_id='minioadmin', aws_secret_access_key='minioadmin')

def verifier_qualite():
    try:
        obj = s3.get_object(Bucket='gold', Key='rapport_tendances_conflit.json')
        data = json.loads(obj['Body'].read().decode('utf-8'))
        
        errors = []
        if data.get("total", 0) == 0:
            errors.append("Erreur : Aucun article dans le rapport Gold.")
        if not data.get("articles_par_source"):
            errors.append("Erreur : Statistiques de sources manquantes.")
            
        if errors:
            print(f"❌ Qualité ÉCHOUÉE : {errors}")
        else:
            print("✅ Qualité VALIDÉE : Les données sont complètes et cohérentes.")
            
    except Exception as e:
        print(f"❌ Erreur lors du contrôle qualité : {e}")

if __name__ == "__main__":
    verifier_qualite()
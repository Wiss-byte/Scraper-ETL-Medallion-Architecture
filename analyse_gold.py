import boto3, json
from collections import Counter

s3 = boto3.client('s3', endpoint_url='http://localhost:9000', 
                  aws_access_key_id='minioadmin', aws_secret_access_key='minioadmin')

def generer_donnees_gold():
    reponse = s3.list_objects_v2(Bucket='silver')
    if 'Contents' not in reponse:
        print("Bucket Silver vide.")
        return

    articles = []
    for obj in reponse['Contents']:
        try:
            data_s3 = s3.get_object(Bucket='silver', Key=obj['Key'])
            data = json.loads(data_s3['Body'].read().decode('utf-8'))
            
            # Vérification pour éviter le TypeError
            if isinstance(data, dict):
                articles.append(data)
            else:
                print(f"⚠️ Format invalide ignoré dans Silver : {obj['Key']}")
        except Exception as e:
            print(f"❌ Erreur lecture Silver ({obj['Key']}) : {e}")
    
    if not articles:
        print("Aucun article valide à analyser.")
        return

    # Agrégation des statistiques
    stats_sources = Counter([a['source'] for a in articles if 'source' in a])
    
    # Extraction des mots-clés (plus de 5 lettres)
    mots_bruts = " ".join([a['contenu_propre'] for a in articles if 'contenu_propre' in a]).lower().split()
    top_mots = Counter([m for m in mots_bruts if len(m) > 5]).most_common(12)

    rapport = {
        "articles_par_source": dict(stats_sources),
        "mots_cles": dict(top_mots),
        "total": len(articles)
    }
    
    s3.put_object(Bucket='gold', Key='rapport_tendances_conflit.json', Body=json.dumps(rapport))
    print("📊 Couche Gold générée avec succès : Statistiques prêtes !")

if __name__ == "__main__":
    generer_donnees_gold()
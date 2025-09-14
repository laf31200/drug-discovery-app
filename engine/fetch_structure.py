import requests
import sys

# Vérifie qu'un identifiant est fourni
if len(sys.argv) < 2:
    print("Usage: python fetch_structure.py <PDB_ID|UniProt_ID|Protein_Name>")
    sys.exit(1)

query_id = sys.argv[1]


def search_UniProt(query_id):
    """Recherche un ID UniProt depuis un nom, puis télécharge via AlphaFold si trouvé."""
    print(f"[INFO] Recherche UniProt pour {query_id}...")
    url = f"https://rest.uniprot.org/uniprotkb/search?query={query_id}&format=json&size=1&fields=accession"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            if data.get("results"):
                uniprot_id = data["results"][0]["primaryAccession"]
                print(f"[OK] Correspondance: {query_id} -> {uniprot_id}")
                search_AFB(uniprot_id)
            else:
                print(f"[ERROR] Aucun résultat UniProt pour '{query_id}'.")
        else:
            print(f"[ERROR] UniProt HTTP {r.status_code}.")
    except requests.exceptions.Timeout:
        print(f"[ERROR] Timeout UniProt pour '{query_id}'.")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Réseau UniProt: {e}")


def search_PDB(query_id):
    """Télécharge une structure PDB si disponible."""
    print(f"[INFO] Téléchargement PDB: {query_id}")
    url = f"https://files.rcsb.org/download/{query_id}.pdb"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200 and ("ATOM" in r.text or "HEADER" in r.text):
            with open(f"{query_id}.pdb", "w") as f:
                f.write(r.text)
            print(f"[OK] Fichier '{query_id}.pdb' téléchargé.")
        else:
            print(f"[ERROR] PDB HTTP {r.status_code} ou contenu invalide.")
    except requests.exceptions.Timeout:
        print(f"[ERROR] Timeout PDB pour '{query_id}'.")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Réseau PDB: {e}")


def search_AFB(query_id):
    """Télécharge un modèle AlphaFold pour un ID UniProt."""
    print(f"[INFO] Téléchargement AlphaFold: {query_id}")
    url = f"https://alphafold.ebi.ac.uk/files/AF-{query_id}-F1-model_v4.pdb"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200 and "ATOM" in r.text:
            with open(f"AF-{query_id}.pdb", "w") as f:
                f.write(r.text)
            print(f"[OK] Fichier 'AF-{query_id}.pdb' téléchargé.")
        else:
            print(f"[ERROR] AlphaFold HTTP {r.status_code} ou contenu invalide.")
    except requests.exceptions.Timeout:
        print(f"[ERROR] Timeout AlphaFold pour '{query_id}'.")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Réseau AlphaFold: {e}")


def is_pdb_id(query_id):
    """Retourne True si l'ID existe dans la PDB."""
    url = f"https://files.rcsb.org/download/{query_id}.pdb"
    try:
        r = requests.head(url, timeout=10)
        return r.status_code == 200
    except requests.exceptions.RequestException:
        return False


def is_uniprot_id(query_id):
    """Retourne True si l'ID existe dans AlphaFold DB."""
    url = f"https://alphafold.ebi.ac.uk/files/AF-{query_id}-F1-model_v4.pdb"
    try:
        r = requests.head(url, timeout=10)
        return r.status_code == 200
    except requests.exceptions.RequestException:
        return False


# Logique principale: PDB -> AlphaFold -> UniProt
if is_pdb_id(query_id):
    search_PDB(query_id)
elif is_uniprot_id(query_id):
    search_AFB(query_id)
else:
    search_UniProt(query_id)

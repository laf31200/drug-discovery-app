"""
run_pipeline.py

Pipeline complet :
1. Télécharge une structure protéique (PDB ou UniProt ID).
2. Prépare la protéine (nettoyage + ajout d’hydrogènes).
3. Produit un fichier final prêt pour le docking.

Utilisation :
    python run_pipeline.py <PDB_or_UniProt_ID>
Exemple :
    python3 run_pipeline.py 1IEP
    python3 run_pipeline.py P00533
"""
import sys 
import subprocess
import os

if len(sys.argv) < 2 :
    print("Utilisation : python run_pipeline.py <PDB_or_UniProt_ID>")
    sys.exit(1)

prot_id = sys.argv[1]
subprocess.run(["python3","fetch_structure.py",f"{prot_id}"])
# Étape 2 : identifier le fichier produit
# -> on cherche d'abord .pdb classique, puis AlphaFold
if os.path.exists(f"{prot_id}.pdb"):
    pdb_file = f"{prot_id}.pdb"
elif os.path.exists(f"AF-{prot_id}.pdb"):
    pdb_file = f"AF-{prot_id}.pdb"
else:
    print(f"Aucun fichier .pdb trouvé pour {prot_id}")
    sys.exit(1)

subprocess.run(["python3","clean_structure.py",pdb_file])
print(f"[✓] Pipeline terminé. Fichier final : {os.path.splitext(pdb_file)[0]}_prepared.pdb")
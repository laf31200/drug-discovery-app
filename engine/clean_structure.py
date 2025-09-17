"""
clean_structure.py

Pipeline de préparation de protéines pour le docking :
1. Nettoyage du fichier PDB (suppression des molécules d’eau, ligands, ions).
2. Ajout des hydrogènes manquants avec Open Babel.
3. Sauvegarde du fichier final prêt pour le docking.

Entrée :  fichier .pdb brut (ex. 1IEP.pdb)
Sortie :  fichier .pdb préparé (ex. 1IEP_prepared.pdb)

Utilisation :
    python clean_structure.py <fichier.pdb>
"""



from Bio import PDB
from openbabel import pybel
import os
import sys

# Vérification des arguments
if len(sys.argv) < 2:
    print("Utilisation : python clean_structure.py <fichier.pdb>")
    sys.exit(1)

prot = sys.argv[1]
basename, _ = os.path.splitext(prot)
# Chargement de la structure brute
parser = PDB.PDBParser(QUIET=True)
structure = parser.get_structure("protein", prot)
# Sélection : garder uniquement les acides aminés standards
class Nowater_No_ligand(PDB.Select):
    def accept_residue(self, residue):
        return residue.id[0] == " "
# Sauvegarde d'un fichier nettoyé (sans eau, ligands, ions)
io = PDB.PDBIO()
io.set_structure(structure)
io.save(f"{basename}_no_water_no_ligand.pdb", Nowater_No_ligand())
# Chargement dans Open Babel pour ajout des hydrogènes

mol = next(pybel.readfile("pdb", f"{basename}_no_water_no_ligand.pdb"))
print("Atomes avant :", mol.OBMol.NumAtoms(), "dont lourds:", mol.OBMol.NumHvyAtoms())
mol.OBMol.AddHydrogens()
print("Atomes après :", mol.OBMol.NumAtoms(), "dont lourds:", mol.OBMol.NumHvyAtoms())
# Sauvegarde finale et suppression du fichier temporaire
mol.write("pdb", f"{basename}_prepared.pdb", overwrite=True)
os.remove(f"{basename}_no_water_no_ligand.pdb")

print(f"[OK] Fichier préparé : {basename}_prepared.pdb")

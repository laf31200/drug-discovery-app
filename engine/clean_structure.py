from Bio import PDB

parser = PDB.PDBParser(QUIET=True)
structure = parser.get_structure("protein","1IEP.pdb")


for model in structure:
    for chain in model:
        for residue in chain:
            if residue.get_resname() != "HOH":
                print(residue.get_resname(),residue.get_id()[1],chain.get_id())

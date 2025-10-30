from sys import argv
import pandas as pd

def extract_unique_accessions(target_filepath,target_col="Assembly Accession",sep="\t"):
    """Return unique accessions from tsv at target_filepath"""

    df = pd.read_csv(target_filepath,sep=sep)
    if target_col not in list(df.columns):
        raise ValueError(f"{target_col} not in any of columns:{df.columns}")
    
    accessions = df[target_col].unique()
    accessions = list(accessions)
    accessions = list(set(list(accessions)))
    return accessions

def accessions_to_file(accessions,df_filepath):
    """Save accessions as a text file"""
    f = open(df_filepath,"w+")
    for a in accessions:
        a = a.strip() #ensure no trailing whitespace
        f.write(a+"\n")
    f.close()

if __name__ == "__main__":
    if len(argv) < 3:
        raise IOError("Usage: python get_unique_accession <input_filepath> <output_filepath>")
    target_filepath = argv[1]
    output_filepath = argv[2]
    unique_accessions = extract_unique_accessions(target_filepath)
    n_unique_accessions = len(unique_accessions)
    print(f"Found {n_unique_accessions} unique accessions")
    print(f"Writing accessions to file: {output_filepath}")
    accessions_to_file(unique_accessions,output_filepath)

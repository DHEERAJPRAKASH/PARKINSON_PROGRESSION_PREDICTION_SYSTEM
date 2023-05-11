import pandas as pd
import numpy as np

def loadData():
    prot_1 = pd.read_csv("static/datas/proteins_Uniprot_updrs1.csv")
    prot_2 = pd.read_csv("static/datas/proteins_Uniprot_updrs2.csv")
    prot_3 = pd.read_csv("static/datas/proteins_Uniprot_updrs3.csv")
    prot_4 = pd.read_csv("static/datas/proteins_Uniprot_updrs4.csv")

    pept_1 = pd.read_csv("static/datas/peptides_PeptideAbundance_updrs1.csv")
    pept_2 = pd.read_csv("static/datas/peptides_PeptideAbundance_updrs2.csv")
    pept_3 = pd.read_csv("static/datas/peptides_PeptideAbundance_updrs3.csv")
    pept_4 = pd.read_csv("static/datas/peptides_PeptideAbundance_updrs4.csv")

    df_0_1 = pd.read_csv("static/datas/df_0_1.csv")
    df_0_2 = pd.read_csv("static/datas/df_0_2.csv")
    df_0_3 = pd.read_csv("static/datas/df_0_3.csv")
    df_0_4 = pd.read_csv("static/datas/df_0_4.csv")

    df_proteins_fts = [prot_1, prot_2, prot_3, prot_4]
    df_peptides_fts = [pept_1, pept_2, pept_3, pept_4]
    df_lst = [df_0_1, df_0_2, df_0_3, df_0_4]

    return df_proteins_fts,df_peptides_fts,df_lst

def smape(y_true,y_pred):
    smap=np.zeros(len(y_true))
    num=np.abs(y_true-y_pred)
    dem=((np.abs(y_true)+np.abs(y_pred))/2)
    pos_ind=(y_true!=0)|(y_pred!=0)
    smap[pos_ind]=num[pos_ind]/dem[pos_ind]
    return 100*np.mean(smap)
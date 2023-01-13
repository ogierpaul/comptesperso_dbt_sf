import pandas as pd
import glob
import re
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector

def latest_excel_from_finanzguru(path:str) -> pd.DataFrame:
    """
    :param path:
    :return:
    """
    usual_dirs = ['/Users/paul_ogier/Downloads', '/Users/paul_ogier/Documents/comptes']
    pattern = r"^\d{8}-Export-Alle_Buchungen.xlsx$"
    files = []
    for d in usual_dirs:
        for filepath in glob.glob(d + "/*.*"):
            filename = filepath.split('/')[-1]
            if re.match(pattern, filename):
                files.append((filename, filepath))
    if len(files) > 0:
        files = sorted(files, reverse=True)
        most_recent_file = files[0][1]
    else:
        raise FileNotFoundError("No file found using this pattern")
    df = pd.read_excel(most_recent_file)
    return df


def remove_unused_cols(df: pd.DataFrame) -> pd.DataFrame:
    unused_cols = ['Waehrung', 'E-Ref', 'Mandatsreferenz', 'Notiz', 'Analyse-Woche', 'Analyse-Monat',
                   'Analyse-Quartal', 'Analyse-Jahr', 'Tags']
    for c in unused_cols:
        if c in df.columns:
            df = df.drop(c, axis=1)
    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    d = {'Buchungstag': 'date_enregistrement',
         'Betrag': 'montant',
         'Kontostand': 'solde_compte',
         'Beguenstigter/Auftraggeber': 'beneficiaire',
         'IBAN Beguenstigter/Auftraggeber': 'beneficiaire_iban',
         'Verwendungszweck': 'transaction_description',
         'Glaeubiger-ID': 'beneficiaire_iban2',
         'Analyse-Hauptkategorie': 'categorie_L1',
         'Analyse-Unterkategorie': 'categorie_L2',
         'Analyse-Vertrag': 'contrat',
         'Analyse-Vertragsturnus': 'contrat_recurrence',
         'Analyse-Vertrags-ID': 'contrat_id',
         'Analyse-Umbuchung': 'transfer',
         'Analyse-Vom frei verfuegbaren Einkommen ausgeschlossen': 'exclus_revenus',
         'Analyse-Umsatzart': 'transaction_methode',
         'Analyse-Betrag': 'revenus_depenses'}
    df = df.rename(columns=d)
    return df

def prepare_file(df: pd.DataFrame) -> pd.DataFrame:
    df = remove_unused_cols(df)
    df = rename_columns(df)
    return df

if __name__ == '__main__':
    filepath = latest_excel_from_finanzguru()
    print(filepath)

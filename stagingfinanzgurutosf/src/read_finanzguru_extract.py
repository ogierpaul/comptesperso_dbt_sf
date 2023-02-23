import pandas as pd
import glob
import re
import hashlib
import datetime

global_expected_columns = ['DATE_ENREGISTREMENT', 'NAME_PERSONAL_ACCOUNT', 'MONTANT',
       'SOLDE_COMPTE', 'BENEFICIAIRE', 'BENEFICIAIRE_IBAN',
       'TRANSACTION_DESCRIPTION', 'BENEFICIAIRE_IBAN2', 'CATEGORIE_L1',
       'CATEGORIE_L2', 'CONTRAT', 'CONTRAT_RECURRENCE', 'CONTRAT_ID',
       'TRANSFER', 'EXCLUS_REVENUS', 'TRANSACTION_METHODE',
       'REVENUS_DEPENSES', 'PERSONAL_IBAN', 'FILENAME', 'PROCESSING_DATE']

def _hello_world() -> str:
    """
    This dummy function is used to test the integration with pytest
    :return: dummy text for use in pytest
    """
    return 'Hello World'


def latest_excel_from_finanzguru() -> (pd.DataFrame, str):
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
    print(most_recent_file)
    return df, most_recent_file

def remove_unused_cols(df: pd.DataFrame) -> pd.DataFrame:
    unused_cols = ['Waehrung', 'E-Ref', 'Mandatsreferenz', 'Notiz', 'Analyse-Woche', 'Analyse-Monat',
                   'Analyse-Quartal', 'Analyse-Jahr', 'Tags']
    for c in unused_cols:
        if c in df.columns:
            df = df.drop(c, axis=1)
    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    d = {'Buchungstag': 'DATE_ENREGISTREMENT',
         'Betrag': 'MONTANT',
         'Kontostand': 'SOLDE_COMPTE',
         'Beguenstigter/Auftraggeber': 'BENEFICIAIRE',
         'IBAN Beguenstigter/Auftraggeber': 'BENEFICIAIRE_IBAN',
         'Verwendungszweck': 'TRANSACTION_DESCRIPTION',
         'Glaeubiger-ID': 'BENEFICIAIRE_IBAN2',
         'Analyse-Hauptkategorie': 'CATEGORIE_L1',
         'Analyse-Unterkategorie': 'CATEGORIE_L2',
         'Analyse-Vertrag': 'CONTRAT',
         'Analyse-Vertragsturnus': 'CONTRAT_RECURRENCE',
         'Analyse-Vertrags-ID': 'CONTRAT_ID',
         'Analyse-Umbuchung': 'TRANSFER',
         'Analyse-Vom frei verfuegbaren Einkommen ausgeschlossen': 'EXCLUS_REVENUS',
         'Analyse-Umsatzart': 'TRANSACTION_METHODE',
         'Analyse-Betrag': 'REVENUS_DEPENSES',
         'Referenzkonto' : 'PERSONAL_IBAN',
         'Name Referenzkonto': 'NAME_PERSONAL_ACCOUNT'}
    df = df.rename(columns=d)
    return df

def add_uid(df: pd.DataFrame) -> pd.DataFrame:
    def to_str(s) -> str:
        if pd.isnull(s):
            return ''
        else:
            return str(s)
    def to_md5(s:str) -> str:
        return hashlib.md5(s.encode('utf-8')).hexdigest()[:8]
    uid_name = 'TRANSACTION_ID'
    hashed_cols = ['DATE_ENREGISTREMENT', 'MONTANT', 'PERSONAL_IBAN', 'BENEFICIAIRE', 'BENEFICIAIRE_IBAN', 'TRANSACTION_DESCRIPTION', 'SOLDE_COMPTE']
    df[uid_name] = df[hashed_cols].applymap(to_str).apply(lambda r:'|'.join(r), axis=1).apply(to_md5)
    uid_counts = df[uid_name].value_counts()
    if uid_counts.max() > 1:
        duplicates = uid_counts.loc[uid_counts > 1].index
        raise KeyError(f'In column {uid_name}: duplicate values for values: {duplicates} ' )
    df.set_index(uid_name, inplace=True)
    return df


def prepare_excel_for_upload(df: pd.DataFrame, filename:str) -> pd.DataFrame:
    df = remove_unused_cols(df)
    df = rename_columns(df)
    df['FILENAME'] = filename
    df['PROCESSING_DATE'] = datetime.datetime.now().strftime('%Y-%m-%d')
    df = df[global_expected_columns]
    df = add_uid(df)
    df.columns = [c.upper() for c in df.columns]
    return df

def write_df_to_csv(df:pd.DataFrame, fp:str) -> None:
    df.to_csv(fp, encoding='utf-8', index=True, sep='|')


def latest_excel_as_df_prepared() -> pd.DataFrame:
    (df, filename) = latest_excel_from_finanzguru()
    return prepare_excel_for_upload(df, filename)

if __name__ == '__main__':
    df = latest_excel_from_finanzguru()
    df = prepare_excel_for_upload(df)
    fp = '/Users/paul_ogier/Desktop/export_finanzguru.csv'
    write_df_to_csv(df, fp)
    pass

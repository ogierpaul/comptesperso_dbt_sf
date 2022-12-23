import pandas as pd
import glob
import re

def latest_excel_from_finanzguru()->str:
    """
    :param path:
    :return:
    """
    dir_to_search = ['/Users/paul_ogier/Downloads', '/Users/paul_ogier/Documents/comptes']
    pattern = r"^\d{8}-Export-Alle_Buchungen.xlsx$"
    files = []
    for d in dir_to_search:
        for filepath in glob.glob(d + "/*.*"):
            filename = filepath.split('/')[-1]
            if re.match(pattern, filename):
                files.append((filename, filepath))
    if len(files) > 0:
        files = sorted(files, reverse=True)
        most_recent_file = files[0][1]
    else:
        raise FileNotFoundError("No file found using this pattern")
    return most_recent_file

def to_snowflake(fp) -> pd.DataFrame:
    df = pd.read_excel(fp)
    
    pass

if __name__ == '__main__':
    filepath = latest_excel_from_finanzguru()
    print(filepath)

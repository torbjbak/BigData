from typing import Union, Any
import pandas as pd

def get_filename(month: str, directory: str = 'dataset') -> str:
    PREFIX = 'Sales'
    YEAR = '2019'
    return f"{directory}/{PREFIX}_{month}_{YEAR}.csv"

def get_csv_files(directory: str) -> pd.DataFrame:
    MONTHS = [
        'January', 
        'February', 
        'March', 
        'April',  
        'May', 
        'June', 
        'July', 
        'August', 
        'September',
        'October', 
        'November', 
        'December'
    ]

    csv_files = []
    for month in MONTHS:
        csv_filename = get_filename(month, directory)
        csv_file = pd.read_csv(csv_filename, index_col=0)
        csv_files.append(csv_file)

    return pd.concat(csv_files, ignore_index=True).reset_index(drop=True)

def remove_noise_columns(csv_file: pd.DataFrame, columns: list) -> pd.DataFrame:
    for column in columns:
        del csv_file[column]

    return csv_file.reset_index(drop=True)

# def get_month_number(csv_file: Union[Any, pd.DataFrame, pd.Series, pd.Index]) -> Union[Any, pd.DataFrame, pd.Series, pd.Index]:
def get_month_number(csv_file: Any) -> pd.DataFrame:
    dates = csv_file['Order Date']
    return dates.astype('str').str[0:2]

def add_column(csv_file: Union[pd.DataFrame, pd.Series], column: str, values: Any) -> Union[pd.DataFrame, pd.Series]:
    csv_file[column] = values
    return csv_file

def convert_to_numeric(csv_file: Any, column: str) -> pd.Series:
    csv_file[column] = pd.to_numeric(csv_file[column], errors='coerce')
    return csv_file[pd.to_numeric(csv_file[column], errors='coerce').notnull()]

def write_csv(csv_file: Union[pd.DataFrame, pd.Series], csv_filename: str) -> Union[None, str]:
    csv_file.reset_index(drop=True).to_csv(csv_filename)

if __name__ == "__main__":
    csv_file = get_csv_files('data')
    print(csv_file.head())
    print(csv_file.tail())
    csv_file = remove_noise_columns(csv_file, ['x_t', 'perf']).reset_index(drop=True)
    print(csv_file.tail())

    month_numbers = get_month_number(csv_file)
    csv_file = add_column(csv_file, 'Month', month_numbers)
    csv_file = convert_to_numeric(csv_file, 'Month')

    csv_file = convert_to_numeric(csv_file, 'Quantity Ordered')
    csv_file = convert_to_numeric(csv_file, 'Price Each')
    sum = csv_file['Quantity Ordered'].mul(csv_file['Price Each'])
    csv_file = add_column(csv_file, 'Sum', sum)
    print(csv_file.tail())

    csv_file = csv_file.groupby(['Month']).sum().sort_values('Sum', ascending=False)
    csv_file = remove_noise_columns(csv_file, ['Price Each']).reset_index(drop=True)
    print(csv_file) 
    write_csv(csv_file, 'result/oppgave_f.csv')
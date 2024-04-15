import pandas as pd
import os
 
async def text_to_excel(text):
    text_file_parent = "src\services\sqlService"
    text_file = 'excelText.txt'
    with open(os.path.join(text_file_parent, text_file), 'w') as fp:
       pass
    text_file_path = "src\\services\\sqlService\\excelText.txt"
    file = open(text_file_path, 'w')
    file.write(text)
    file.flush()
    # excel = "src\\services\\sqlService\\temp.txt"
    with open(text_file_path, "r") as file:
     data = file.read()
    file.close()
    os.remove(text_file_path)
    excel_file_path = "src\services\sqlService\output.xlsx"
    if os.path.exists(excel_file_path):
       os.remove(excel_file_path)
    # with open(excel_file_path, 'w') as new_csv_file:
    #     pass
 
    # Split rows based on '||'
    rows = data.split('\n')
 
    # Split cells based on '|'
    data_list = [row.split('|') for row in rows]
    data_list.pop(2)
 
    # Convert to DataFrame
    df = pd.DataFrame(data_list)
 
    # Write DataFrame to Excel
    df.to_excel('src\\services\\sqlService\\output.xlsx', index=False)
 
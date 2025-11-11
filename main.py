import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

def fetchHW(startyear: int = None, endyear: int = None):
    if not startyear or not endyear:
        print(">> ERROR: you need to enter a start year and end year.")
        return
    
    elif startyear > endyear:
        print(">> ERROR: start year cannot be greater than end year.")
        return

    else:
        print() # SABRINA CARPENTER DOES NOT KNOW HOW TO PRINT NEWLINES PROPERLY

    start_time = time.time()
    df_all_cars_list = []

    for year in range(endyear-startyear+1):
        year += startyear
        print(f"Fetching cars from {year}...")
        url = f"https://hotwheels.fandom.com/wiki/List_of_{year}_Hot_Wheels"
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        
        for table in soup.find_all('table', 'wikitable'):
            headers = ["ToyID", "Col.#", "ModelName", "Series", "SeriesNumber", "Photo"]
            rows = []
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) == len(headers):
                    row_data = [col.text.strip() for col in cols[:-1]]
                    
                    series_data = []
                    series_cell = cols[headers.index('Series')]
                    for content in series_cell.stripped_strings:
                        series_data.append(content)
                    row_data[headers.index('Series')] = ', '.join(series_data)
                    
                    img_link = cols[-1].find('a', 'image')
                    row_data.append(img_link.get('href') if img_link else None)
                    row_data.append(year)
                    
                    if row_data[0]:
                        rows.append(row_data)
            
            df_all_cars_list.append(pd.DataFrame(rows, columns=headers + ['Year']))

    df = pd.concat(df_all_cars_list, ignore_index=True).replace("", None)
    df_all_cars = df.drop(df.columns[1], axis=1)

    json_data = df_all_cars.to_json(orient='records', indent=2, force_ascii=False).replace("\\/", "/").replace(r"\u200b", "")

    filename = f"hotwheels_{startyear}_{endyear}_cars.json"
    with open(filename, "w", encoding="utf-8") as json_file:
        json_file.write(json_data)

    end_time = time.time()
    print(f"\n>> data saved to {filename} ({end_time - start_time:.2f} seconds)")

if __name__ == "__main__":
    print("============================\nHot Wheels Car Data Fetcher\n============================\n")
    fetchHW(int(input("> input the starting year: ")), int(input("> input the ending year: ")))
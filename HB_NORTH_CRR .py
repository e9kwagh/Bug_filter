"""HB-north"""

import csv 
import os
from datetime import datetime

def extractor():
    filename = os.path.abspath("HB_NORTH_CRR .csv")
    with open(filename, "r", encoding="utf-8-sig") as hour:
        unsorted = list(csv.DictReader(hour)) 
        file_sorted = sorted(unsorted, key=lambda x: x['fordate'])
    return file_sorted

def bug_filter():
    file = extractor()
    all_dates = sorted(list(set([row["fordate"] for row in file])))
    peakwd, peakwe, off_peak = [], [], []
    result_list = []
    collections = []

    for date in all_dates:
        rows_for_date = [row for row in file if row["fordate"].startswith(date)]
        result_list.append(rows_for_date)

    for datas in result_list:
        peakwd_for_date = [data for data in datas if data["shape"] == 'PeakWD']
        peakwe_for_date = [data for data in datas if data["shape"] == 'PeakWE']
        off_peak_for_date = [data for data in datas if data["shape"] == 'Off-peak']

        peakwd_for_date = sorted(peakwd_for_date, key=lambda x: int(x.get('sequence', 0)), reverse=True)
        peakwe_for_date = sorted(peakwe_for_date, key=lambda x: int(x.get('sequence', 0)), reverse=True)
        off_peak_for_date = sorted(off_peak_for_date, key=lambda x: int(x.get('sequence', 0)), reverse=True)

        peak_wd = peakwd_for_date[0] if peakwd_for_date else None
        peak_we = peakwe_for_date[0] if peakwe_for_date else None
        off_peak = off_peak_for_date[0] if off_peak_for_date else None

        collections.extend([off_peak, peak_wd, peak_we])

    

    with open("bug_filtered.csv", 'w', newline="",encoding='utf-8') as file:
        headers = collections[0].keys()
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(collections)

   

   
     


if __name__ == "__main__":
    print(bug_filter())




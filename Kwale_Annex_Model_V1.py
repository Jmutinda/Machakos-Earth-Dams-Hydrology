"""Kwale daily CHIRPS runoff model. Uncalibrated; not dependable yield.
Usage: python Kwale_Annex_Model_V1.py INPUT.csv
Parameters reproduced from original run_batch.py. Source CSV area precision retained for exact reproduction.
"""
import argparse, csv
from pathlib import Path
from datetime import date, timedelta
from collections import defaultdict

SITE='Kwale_catchment'
AREA_KM2=9.794  # Report-rounded value; actual computation uses source area_km2
PARAMS={"low":(0.107,11.90),"central":(0.223,7.94),"high":(0.278,6.38)}
START=date(1981,1,1)
END=date(2025,12,31)

def write_csv(path, rows, columns):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=columns)
        w.writeheader();w.writerows(rows)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    args=parser.parse_args()
    params=PARAMS
    for name,(k,t) in params.items():
        if not 0<=k<=1 or t<0: raise ValueError(f'Invalid {name} parameters')
    rain={}
    source_area=None
    with args.source.open(newline='',encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r['site']!=SITE: continue
            area=float(r['area_km2'])
            if source_area is not None and abs(area-source_area)>1e-9: raise ValueError('Inconsistent area metadata')
            source_area=area
            day=date.fromisoformat(r['date'])
            if START<=day<=END:
                p=float(r['rainfall_mm'])
                if p<0 or day in rain: raise ValueError(f'Invalid or duplicate daily record: {day}')
                rain[day]=p
    expected=(END-START).days+1
    if len(rain)!=expected or any(START+timedelta(days=i) not in rain for i in range(expected)):
        raise ValueError('Incomplete Kwale daily rainfall series')
    daily=[];monthly=defaultdict(lambda:defaultdict(float));annual=defaultdict(lambda:defaultdict(float))
    fields=['rainfall_mm']+[f'{s}_runoff_{u}' for s in params for u in ('mm','m3')]
    for day,p in sorted(rain.items()):
        row={'date':day.isoformat(),'rainfall_mm':p}
        for name,(k,t) in params.items():
            depth=k*max(p-t,0)
            row[f'{name}_runoff_mm']=depth
            row[f'{name}_runoff_m3']=depth*source_area*1000
        daily.append(row)
        for key,table in ((day.year,annual),((day.year,day.month),monthly)):
            for field in fields: table[key][field]+=row[field]
    base=Path(__file__).resolve().parent
    write_csv(base/'Kwale_Model_V1_Daily.csv',daily,['date']+fields)
    write_csv(base/'Kwale_Model_V1_Monthly.csv',[{'year':y,'month':m,**monthly[y,m]} for y,m in sorted(monthly)],['year','month']+fields)
    write_csv(base/'Kwale_Model_V1_Annual.csv',[{'year':y,**annual[y]} for y in sorted(annual)],['year']+fields)
    print(f'Validated {expected} days. Central mean annual runoff: {sum(annual[y]["central_runoff_m3"] for y in annual)/len(annual):,.0f} m³')

if __name__=='__main__': main()

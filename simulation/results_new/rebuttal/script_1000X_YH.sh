: '
python3 eagle_simulation.py temp.tr.YH no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 10000 no 0 2 no Hawk 0 0 0 && mv finished_file h.10000J.1000X.10000N.YH
python3 eagle_simulation.py temp.tr.YH no yes -1 -1 100 98 0 2 5 MEAN 0 0 ATC 10000 10 10000 no 0 2 no CLWL 0 0 0 && mv finished_file yaqc.10000J.1000X.10000N.YH 
python3 eagle_simulation.py temp.tr.YH no yes -1 -1 100 98 0 2 5 MEAN 0 0 ATC 10000 10 10000 yes 8 2 no DLWL 0 0 0 && mv finished_file yaqd.10000J.1000X.10000N.YH
'
python3 eagle_simulation.py temp.tr.YH no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 10000 no 0 2 no Murmuration 10 0 no FCFS && mv finished_file m.10000J.1000X.10000N.1000S.YH.fcfs
python3 eagle_simulation.py temp.tr.YH no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 10000 yes 0 2 no Murmuration 10 0 no SRJF && mv finished_file m.10000J.1000X.10000N.1000S.YH.srjf

: '
python3 eagle_simulation.py temp.tr.YH no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 5000 no 0 2 no Hawk 0 0 0 && mv finished_file h.10000J.1000X.5000N.YH
python3 eagle_simulation.py temp.tr.YH no yes -1 -1 100 98 0 2 5 MEAN 0 0 ATC 10000 10 5000 no 0 2 no CLWL 0 0 0 && mv finished_file yaqc.10000J.1000X.5000N.YH 
python3 eagle_simulation.py temp.tr.YH no yes -1 -1 100 98 0 2 5 MEAN 0 0 ATC 10000 10 5000 yes 8 2 no DLWL 0 0 0 && mv finished_file yaqd.10000J.1000X.5000N.YH 
'
python3 eagle_simulation.py temp.tr.YH no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 5000 no 0 2 no Murmuration 10 0 no FCFS && mv finished_file m.10000J.1000X.5000N.1000S.YH.fcfs
python3 eagle_simulation.py temp.tr.YH no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 5000 yes 0 2 no Murmuration 10 0 no SRJF && mv finished_file m.10000J.1000X.5000N.1000S.YH.srjf

: '
python3 eagle_simulation.py temp.tr.YH no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 15000 no 0 2 no Hawk 0 0 0 && mv finished_file h.10000J.1000X.15000N.YH
python3 eagle_simulation.py temp.tr.YH no yes -1 -1 100 98 0 2 5 MEAN 0 0 ATC 10000 10 15000 no 0 2 no CLWL 0 0 0 && mv finished_file yaqc.10000J.1000X.15000N.YH 
python3 eagle_simulation.py temp.tr.YH no yes -1 -1 100 98 0 2 5 MEAN 0 0 ATC 10000 10 15000 yes 8 2 no DLWL 0 0 0 && mv finished_file yaqd.10000J.1000X.15000N.YH 
'
python3 eagle_simulation.py temp.tr.YH no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 15000 no 0 2 no Murmuration 10 0 no FCFS && mv finished_file m.10000J.1000X.15000N.1000S.YH.fcfs
python3 eagle_simulation.py temp.tr.YH no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 15000 yes 0 2 no Murmuration 10 0 no SRJF && mv finished_file m.10000J.1000X.15000N.1000S.YH.srjf

: '
python3 eagle_simulation.py temp.tr.YH no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no Hawk 0 0 0 && mv finished_file h.10000J.1000X.1000N.YH
python3 eagle_simulation.py temp.tr.YH no yes -1 -1 100 98 0 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no CLWL 0 0 0 && mv finished_file yaqc.10000J.1000X.1000N.YH 
python3 eagle_simulation.py temp.tr.YH no yes -1 -1 100 98 0 2 5 MEAN 0 0 ATC 10000 10 1000 yes 8 2 no DLWL 0 0 0 && mv finished_file yaqd.10000J.1000X.1000N.YH 
'
python3 eagle_simulation.py temp.tr.YH no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no Murmuration 10 0 no FCFS && mv finished_file m.10000J.1000X.1000N.1000S.YH.fcfs
python3 eagle_simulation.py temp.tr.YH no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 1000 yes 0 2 no Murmuration 10 0 no SRJF && mv finished_file m.10000J.1000X.1000N.1000S.YH.srjf

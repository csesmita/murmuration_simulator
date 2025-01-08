: '
python3 eagle_simulation.py temp.tr.CCc no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 10000 no 0 2 no Hawk 0 0 0 && mv finished_file h.10000J.1000X.10000N.CCc
python3 eagle_simulation.py temp.tr.CCc no yes -1 -1 100 91 0 2 5 MEAN 0 0 ATC 10000 10 10000 no 0 2 no CLWL 0 0 0 && mv finished_file yaqc.10000J.1000X.10000N.CCc 
'
python3 eagle_simulation.py temp.tr.CCc no yes -1 -1 100 91 0 2 5 MEAN 0 0 ATC 10000 10 10000 yes 8 2 no DLWL 0 0 no FCFS no && mv finished_file yaqd.10000J.1000X.10000N.CCc
python3 eagle_simulation.py temp.tr.CCc no yes 272.7830 272.7830 100 91 0 2 5 MEAN 0 0 ATC 10000 10 10000 yes 0 20 yes Eagle 0 0 no FCFS no && mv finished_file eagle.10000J.1000X.10000N.CCc 
: '

python3 eagle_simulation.py temp.tr.CCc no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 10000 no 0 2 no Murmuration 10 0 no FCFS && mv finished_file m.10000J.1000X.10000N.1000S.CCc.fcfs
python3 eagle_simulation.py temp.tr.CCc no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 10000 yes 0 2 no Murmuration 10 0 no SRJF && mv finished_file m.10000J.1000X.10000N.1000S.CCc.srjf 

python3 eagle_simulation.py temp.tr.CCc no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 5000 no 0 2 no Hawk 0 0 0 && mv finished_file h.10000J.1000X.5000N.CCc
python3 eagle_simulation.py temp.tr.CCc no yes -1 -1 100 91 0 2 5 MEAN 0 0 ATC 10000 10 5000 no 0 2 no CLWL 0 0 0 && mv finished_file yaqc.10000J.1000X.5000N.CCc 
'
python3 eagle_simulation.py temp.tr.CCc no yes -1 -1 100 91 0 2 5 MEAN 0 0 ATC 10000 10 5000 yes 8 2 no DLWL 0 0 no FCFS no && mv finished_file yaqd.10000J.1000X.5000N.CCc
python3 eagle_simulation.py temp.tr.CCc no yes 272.7830 272.7830 100 91 0 2 5 MEAN 0 0 ATC 10000 10 5000 yes 0 20 yes Eagle 0 0 no FCFS no && mv finished_file eagle.10000J.1000X.5000N.CCc 

: '
python3 eagle_simulation.py temp.tr.CCc no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 5000 no 0 2 no Murmuration 10 0 no FCFS && mv finished_file m.10000J.1000X.5000N.1000S.CCc.fcfs
python3 eagle_simulation.py temp.tr.CCc no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 5000 yes 0 2 no Murmuration 10 0 no SRJF && mv finished_file m.10000J.1000X.5000N.1000S.CCc.srjf

python3 eagle_simulation.py temp.tr.CCc no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 15000 no 0 2 no Hawk 0 0 0 && mv finished_file h.10000J.1000X.15000N.CCc
python3 eagle_simulation.py temp.tr.CCc no yes -1 -1 100 91 0 2 5 MEAN 0 0 ATC 10000 10 15000 no 0 2 no CLWL 0 0 0 && mv finished_file yaqc.10000J.1000X.15000N.CCc 
'
python3 eagle_simulation.py temp.tr.CCc no yes -1 -1 100 91 0 2 5 MEAN 0 0 ATC 10000 10 15000 yes 8 2 no DLWL 0 0 no FCFS no && mv finished_file yaqd.10000J.1000X.15000N.CCc
python3 eagle_simulation.py temp.tr.CCc no yes 272.7830 272.7830 100 91 0 2 5 MEAN 0 0 ATC 10000 10 15000 yes 0 20 yes Eagle 0 0 no FCFS no && mv finished_file eagle.10000J.1000X.15000N.CCc 
: '
python3 eagle_simulation.py temp.tr.CCc no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 15000 no 0 2 no Murmuration 10 0 no FCFS && mv finished_file m.10000J.1000X.15000N.1000S.CCc.fcfs
python3 eagle_simulation.py temp.tr.CCc no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 15000 yes 0 2 no Murmuration 10 0 no SRJF && mv finished_file m.10000J.1000X.15000N.1000S.CCc.srjf

python3 eagle_simulation.py temp.tr.CCc no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no Hawk 0 0 0 && mv finished_file h.10000J.1000X.1000N.CCc
python3 eagle_simulation.py temp.tr.CCc no yes -1 -1 100 91 0 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no CLWL 0 0 0 && mv finished_file yaqc.10000J.1000X.1000N.CCc 
'
python3 eagle_simulation.py temp.tr.CCc no yes -1 -1 100 91 0 2 5 MEAN 0 0 ATC 10000 10 1000 yes 8 2 no DLWL 0 0 no FCFS no && mv finished_file yaqd.10000J.1000X.1000N.CCc
python3 eagle_simulation.py temp.tr.CCc no yes 272.7830 272.7830 100 91 0 2 5 MEAN 0 0 ATC 10000 10 1000 yes 0 20 yes Eagle 0 0 no FCFS no && mv finished_file eagle.10000J.1000X.1000N.CCc 
: '
python3 eagle_simulation.py temp.tr.CCc no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no Murmuration 10 0 no FCFS && mv finished_file m.10000J.1000X.1000N.1000S.CCc.fcfs
python3 eagle_simulation.py temp.tr.CCc no no -1 -1 100 100 0 2 5 MEAN 0 0 ATC 10000 10 1000 yes 0 2 no Murmuration 10 0 no SRJF && mv finished_file m.10000J.1000X.1000N.1000S.CCc.srjf
'

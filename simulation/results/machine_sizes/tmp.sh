#Sparrow
python3 eagle_simulation.py YH.tr no no 90.5811 90.5811 100 100 1 2 5 MEAN 0 0 ATC 0 0 1000 no 0 2 no Hawk 0 0 && mv finished_file s.11 && python3 eagle_simulation.py YH.tr no no 90.5811 90.5811 100 100 1 2 5 MEAN 0 0 ATC 0 0 2000 no 0 2 no Hawk 0 0 && mv finished_file s.12 && python3 eagle_simulation.py YH.tr no no 90.5811 90.5811 100 100 1 2 5 MEAN 0 0 ATC 0 0 3000 no 0 2 no Hawk 0 0 && mv finished_file s.13 && python3 eagle_simulation.py YH.tr no no 90.5811 90.5811 100 100 1 2 5 MEAN 0 0 ATC 0 0 4000 no 0 2 no Hawk 0 0 && mv finished_file s.14
#Murmuration
python3 eagle_simulation.py YH.tr no no -1 90.5811 100 100 1 2 5 MEAN 0 0 ATC 0 0 1000 no 0 2 no Murmuration 1 0 && mv finished_file m.11 && python3 eagle_simulation.py YH.tr no no -1 90.5811 100 100 1 2 5 MEAN 0 0 ATC 0 0 2000 no 0 2 no Murmuration 1 0 && mv finished_file m.12 && python3 eagle_simulation.py YH.tr no no -1 90.5811 100 100 1 2 5 MEAN 0 0 ATC 0 0 3000 no 0 2 no Murmuration 1 0 && mv finished_file m.13 && python3 eagle_simulation.py YH.tr no no -1 90.5811 100 100 1 2 5 MEAN 0 0 ATC 0 0 4000 no 0 2 no Murmuration 1 0 && mv finished_file m.14
#Hawk
python3 eagle_simulation.py YH.tr yes yes 90.5811 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no Hawk 0 0 && mv finished_file h.11 && python3 eagle_simulation.py YH.tr yes yes 90.5811 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 2000 no 0 2 no Hawk 0 0 && mv finished_file h.12 && python3 eagle_simulation.py YH.tr yes yes 90.5811 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 3000 no 0 2 no Hawk 0 0 && mv finished_file h.13 && python3 eagle_simulation.py YH.tr yes yes 90.5811 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 4000 no 0 2 no Hawk 0 0 && mv finished_file h.14
#Eagle
python3 eagle_simulation.py YH.tr no yes 90.5811 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 1000 yes 0 20 yes Eagle 0 0 && mv finished_file e.11 && python3 eagle_simulation.py YH.tr no yes 90.5811 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 2000 yes 0 20 yes Eagle 0 0 && mv finished_file e.12 && python3 eagle_simulation.py YH.tr no yes 90.5811 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 3000 yes 0 20 yes Eagle 0 0 && mv finished_file e.13 && python3 eagle_simulation.py YH.tr no yes 90.5811 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 4000 yes 0 20 yes Eagle 0 0 && mv finished_file e.14
#Yaq-C
python3 eagle_simulation.py YH.tr no yes -1 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no CLWL 0 0 && mv finished_file yaqc.11
python3 eagle_simulation.py YH.tr no yes -1 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 2000 no 0 2 no CLWL 0 0 && mv finished_file yaqc.12
python3 eagle_simulation.py YH.tr no yes -1 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 3000 no 0 2 no CLWL 0 0 && mv finished_file yaqc.13
python3 eagle_simulation.py YH.tr no yes -1 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 4000 no 0 2 no CLWL 0 0 && mv finished_file yaqc.14
#Yaq-D
python3 eagle_simulation.py YH.tr no yes -1 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 1000 yes 8 2 no DLWL 0 0 && mv finished_file yaqd.11
python3 eagle_simulation.py YH.tr no yes -1 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 2000 yes 8 2 no DLWL 0 0 && mv finished_file yaqd.12
python3 eagle_simulation.py YH.tr no yes -1 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 3000 yes 8 2 no DLWL 0 0 && mv finished_file yaqd.13
python3 eagle_simulation.py YH.tr no yes -1 90.5811 100 98 1 2 5 MEAN 0 0 ATC 10000 10 4000 yes 8 2 no DLWL 0 0 && mv finished_file yaqd.14

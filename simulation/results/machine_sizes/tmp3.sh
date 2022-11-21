#Sparrow
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 1000 no 0 2 no Hawk 0 0 && mv finished_file s.11.-1_-1
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 2000 no 0 2 no Hawk 0 0 && mv finished_file s.12.-1_-1
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 3000 no 0 2 no Hawk 0 0 && mv finished_file s.13.-1_-1
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 4000 no 0 2 no Hawk 0 0 && mv finished_file s.14.-1_-1
#Hawk
pypy3 eagle_simulation.py YH.tr yes yes -1 -1 100 98 1 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no Hawk 0 0 && mv finished_file h.11.-1_-1
pypy3 eagle_simulation.py YH.tr yes yes -1 -1 100 98 1 2 5 MEAN 0 0 ATC 10000 10 2000 no 0 2 no Hawk 0 0 && mv finished_file h.12.-1_-1
pypy3 eagle_simulation.py YH.tr yes yes -1 -1 100 98 1 2 5 MEAN 0 0 ATC 10000 10 3000 no 0 2 no Hawk 0 0 && mv finished_file h.13.-1_-1
pypy3 eagle_simulation.py YH.tr yes yes -1 -1 100 98 1 2 5 MEAN 0 0 ATC 10000 10 4000 no 0 2 no Hawk 0 0 && mv finished_file h.14.-1_-1
#Eagle
pypy3 eagle_simulation.py YH.tr no yes -1 -1 100 98 1 2 5 MEAN 0 0 ATC 10000 10 1000 yes 0 20 yes Eagle 0 0 && mv finished_file e.11.-1_-1
pypy3 eagle_simulation.py YH.tr no yes -1 -1 100 98 1 2 5 MEAN 0 0 ATC 10000 10 2000 yes 0 20 yes Eagle 0 0 && mv finished_file e.12.-1_-1
pypy3 eagle_simulation.py YH.tr no yes -1 -1 100 98 1 2 5 MEAN 0 0 ATC 10000 10 3000 yes 0 20 yes Eagle 0 0 && mv finished_file e.13.-1_-1
pypy3 eagle_simulation.py YH.tr no yes -1 -1 100 98 1 2 5 MEAN 0 0 ATC 10000 10 4000 yes 0 20 yes Eagle 0 0 && mv finished_file e.14.-1_-1
#Yaq-C
pypy3 eagle_simulation.py YH.tr no yes -1 -1 100 100 1 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no CLWL 0 0 && mv finished_file yaqc.11.-1_-1.100_100
pypy3 eagle_simulation.py YH.tr no yes -1 -1 100 100 1 2 5 MEAN 0 0 ATC 10000 10 2000 no 0 2 no CLWL 0 0 && mv finished_file yaqc.12.-1_-1.100_100
pypy3 eagle_simulation.py YH.tr no yes -1 -1 100 100 1 2 5 MEAN 0 0 ATC 10000 10 3000 no 0 2 no CLWL 0 0 && mv finished_file yaqc.13.-1_-1.100_100
pypy3 eagle_simulation.py YH.tr no yes -1 -1 100 100 1 2 5 MEAN 0 0 ATC 10000 10 4000 no 0 2 no CLWL 0 0 && mv finished_file yaqc.14.-1_-1.100_100
#Yaq-D
pypy3 eagle_simulation.py YH.tr no yes -1 -1 100 100 1 2 5 MEAN 0 0 ATC 10000 10 1000 yes 8 2 no DLWL 0 0 && mv finished_file yaqd.11.-1_-1.100_100
pypy3 eagle_simulation.py YH.tr no yes -1 -1 100 100 1 2 5 MEAN 0 0 ATC 10000 10 2000 yes 8 2 no DLWL 0 0 && mv finished_file yaqd.12.-1_-1.100_100
pypy3 eagle_simulation.py YH.tr no yes -1 -1 100 100 1 2 5 MEAN 0 0 ATC 10000 10 3000 yes 8 2 no DLWL 0 0 && mv finished_file yaqd.13.-1_-1.100_100
pypy3 eagle_simulation.py YH.tr no yes -1 -1 100 100 1 2 5 MEAN 0 0 ATC 10000 10 4000 yes 8 2 no DLWL 0 0 && mv finished_file yaqd.14.-1_-1.100_100

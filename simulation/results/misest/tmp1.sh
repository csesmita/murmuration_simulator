: '
#Hawk
pypy3 eagle_simulation.py YH.tr yes yes 5 5 100 98 1 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no Hawk 0 0 && mv finished_file h.misest_shorter
pypy3 eagle_simulation.py YH.tr yes yes 300 300 100 98 1 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no Hawk 0 0 && mv finished_file h.misest_longer
pypy3 eagle_simulation.py YH.tr yes yes 90.5811 90.5811 100 80 1 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no Hawk 0 0 && mv finished_file h.workers_80
pypy3 eagle_simulation.py YH.tr yes yes 90.5811 90.5811 100 90 1 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no Hawk 0 0 && mv finished_file h.workers_90
pypy3 eagle_simulation.py YH.tr yes yes 600 600 100 98 1 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no Hawk 0 0 && mv finished_file h.misest_even_longer_600
pypy3 eagle_simulation.py YH.tr yes yes 900 900 100 98 1 2 5 MEAN 0 0 ATC 10000 10 1000 no 0 2 no Hawk 0 0 && mv finished_file h.misest_even_longer_900
#Eagle
pypy3 eagle_simulation.py YH.tr no yes 5 5 100 98 1 2 5 MEAN 0 0 ATC 10000 10 1000 yes 0 20 yes Eagle 0 0 && mv finished_file e.misest_shorter
pypy3 eagle_simulation.py YH.tr no yes 300 300 100 98 1 2 5 MEAN 0 0 ATC 10000 10 1000 yes 0 20 yes Eagle 0 0 && mv finished_file e.misest_longer
pypy3 eagle_simulation.py YH.tr no yes 90.5811 90.5811 100 80 1 2 5 MEAN 0 0 ATC 10000 10 1000 yes 0 20 yes Eagle 0 0 && mv finished_file e.workers_80
pypy3 eagle_simulation.py YH.tr no yes 90.5811 90.5811 100 90 1 2 5 MEAN 0 0 ATC 10000 10 1000 yes 0 20 yes Eagle 0 0 && mv finished_file e.workers_90
pypy3 eagle_simulation.py YH.tr no yes 600 600 100 98 1 2 5 MEAN 0 0 ATC 10000 10 1000 yes 0 20 yes Eagle 0 0 && mv finished_file e.misest_even_longer_600
pypy3 eagle_simulation.py YH.tr no yes 900 900 100 98 1 2 5 MEAN 0 0 ATC 10000 10 1000 yes 0 20 yes Eagle 0 0 && mv finished_file e.misest_even_longer_900
'
#Hawk
pypy3 eagle_simulation.py YH.tr yes yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 5000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_5000M_611
pypy3 eagle_simulation.py YH.tr yes yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 10000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_10000M_611
pypy3 eagle_simulation.py YH.tr yes yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 15000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_15000M_611
pypy3 eagle_simulation.py YH.tr yes yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 20000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_20000M_611
pypy3 eagle_simulation.py YH.tr yes yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 5000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_5000M_2360
pypy3 eagle_simulation.py YH.tr yes yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 10000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_10000M_2360
pypy3 eagle_simulation.py YH.tr yes yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 15000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_15000M_2360
pypy3 eagle_simulation.py YH.tr yes yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 20000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_20000M_2360
#Eagle
pypy3 eagle_simulation.py YH.tr no yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 5000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_5000M_611
pypy3 eagle_simulation.py YH.tr no yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 10000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_10000M_611
pypy3 eagle_simulation.py YH.tr no yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 15000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_15000M_611
pypy3 eagle_simulation.py YH.tr no yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 20000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_20000M_611
pypy3 eagle_simulation.py YH.tr no yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 5000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_5000M_2360
pypy3 eagle_simulation.py YH.tr no yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 10000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_10000M_2360
pypy3 eagle_simulation.py YH.tr no yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 15000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_15000M_2360
pypy3 eagle_simulation.py YH.tr no yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 20000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_20000M_2360

#Hawk
pypy3 eagle_simulation_smallest.py YH.tr yes yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 5000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_5000M_611.smallest
pypy3 eagle_simulation_smallest.py YH.tr yes yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 10000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_10000M_611.smallest
pypy3 eagle_simulation_smallest.py YH.tr yes yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 15000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_15000M_611.smallest
pypy3 eagle_simulation_smallest.py YH.tr yes yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 20000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_20000M_611.smallest
pypy3 eagle_simulation_smallest.py YH.tr yes yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 5000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_5000M_2360.smallest
pypy3 eagle_simulation_smallest.py YH.tr yes yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 10000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_10000M_2360.smallest
pypy3 eagle_simulation_smallest.py YH.tr yes yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 15000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_15000M_2360.smallest
pypy3 eagle_simulation_smallest.py YH.tr yes yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 20000 no 0 2 no Hawk 0 0 no && mv finished_file h.misest_20000M_2360.smallest
#Eagle
pypy3 eagle_simulation_smallest.py YH.tr no yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 5000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_5000M_611.smallest
pypy3 eagle_simulation_smallest.py YH.tr no yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 10000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_10000M_611.smallest
pypy3 eagle_simulation_smallest.py YH.tr no yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 15000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_15000M_611.smallest
pypy3 eagle_simulation_smallest.py YH.tr no yes 611 611 100 98 1 2 5 MEAN 0 0 ATC 10000 10 20000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_20000M_611.smallest
pypy3 eagle_simulation_smallest.py YH.tr no yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 5000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_5000M_2360.smallest
pypy3 eagle_simulation_smallest.py YH.tr no yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 10000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_10000M_2360.smallest
pypy3 eagle_simulation_smallest.py YH.tr no yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 15000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_15000M_2360.smallest
pypy3 eagle_simulation_smallest.py YH.tr no yes 2360 2360 100 98 1 2 5 MEAN 0 0 ATC 10000 10 20000 yes 0 20 yes Eagle 0 0 no && mv finished_file e.misest_20000M_2360.smallest

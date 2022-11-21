#This is to test no update delay should have same result across different scheduler ratios.
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 5000 no 0 2 no Murmuration 0.1 0 && mv finished_file m.11.10X_0.1

#25% schedulers 1ms / 10ms / 100ms delay
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 5000 no 0 2 no Murmuration 0.25 0.001 && mv finished_file m.11.10X_0.25S_1ms
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 5000 no 0 2 no Murmuration 0.25 0.01 && mv finished_file m.11.10X_0.25S_10ms
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 5000 no 0 2 no Murmuration 0.25 0.1 && mv finished_file m.11.10X_0.25S_100ms

#50% scheduler 1ms / 10ms / 100ms delay
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 5000 no 0 2 no Murmuration 0.5 0.001 && mv finished_file m.11.10X_0.5S_1ms
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 5000 no 0 2 no Murmuration 0.5 0.01 && mv finished_file m.11.10X_0.5S_10ms
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 5000 no 0 2 no Murmuration 0.5 0.1 && mv finished_file m.11.10X_0.5S_100ms

#75% scheduler 1ms / 10ms / 100ms delay
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 5000 no 0 2 no Murmuration 0.75 0.001 no && mv finished_file m.11.10X_0.75S_1ms
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 5000 no 0 2 no Murmuration 0.75 0.01 no && mv finished_file m.11.10X_0.75S_10ms
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 5000 no 0 2 no Murmuration 0.75 0.1 no && mv finished_file m.11.10X_0.75S_100ms

#100% scheduler 1ms / 10ms / 100ms delay
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 5000 no 0 2 no Murmuration 1 0.001 no && mv finished_file m.11.10X_1S_1ms
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 5000 no 0 2 no Murmuration 1 0.01 no && mv finished_file m.11.10X_1S_10ms
pypy3 eagle_simulation.py YH.tr no no -1 -1 100 100 1 2 5 MEAN 0 0 ATC 0 0 5000 no 0 2 no Murmuration 1 0.1 no && mv finished_file m.11.10X_1S_100ms

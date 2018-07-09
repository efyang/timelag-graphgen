#!/bin/bash
mkdir -p renderings
python 'src/main.py' -i 'data/TN_07012018.csv' 'Entries_CC' 'Exits_CC' "Tennessee CC" --coloring 1 --render "renderings/TN_CC_linear.mp4" &
python 'src/main.py' -i 'data/TN_07012018.csv' 'Entries_CC' 'Exits_CC' "Tennessee CC" --coloring 2 --render "renderings/TN_CC_seasonal.mp4" &
python 'src/main.py' -i 'data/TN_07012018.csv' 'Entries_CC' 'Exits_CC' "Tennessee CC" --coloring 3 --render "renderings/TN_CC_seasonal_discrete.mp4" &

python 'src/main.py' -i 'data/TN_07012018.csv' 'Entries_FC' 'Exits_FC' "Tennessee FC" --coloring 1 --render "renderings/TN_FC_linear.mp4" &
python 'src/main.py' -i 'data/TN_07012018.csv' 'Entries_FC' 'Exits_FC' "Tennessee FC" --coloring 2 --render "renderings/TN_FC_seasonal.mp4" &
python 'src/main.py' -i 'data/TN_07012018.csv' 'Entries_FC' 'Exits_FC' "Tennessee FC" --coloring 3 --render "renderings/TN_FC_seasonal_discrete.mp4" &

python 'src/main.py' -i 'data/TN_07012018.csv' 'Entries_KIN' 'Exits_KIN' "Tennessee KIN" --coloring 1 --render "renderings/TN_KIN_linear.mp4" &
python 'src/main.py' -i 'data/TN_07012018.csv' 'Entries_KIN' 'Exits_KIN' "Tennessee KIN" --coloring 2 --render "renderings/TN_KIN_seasonal.mp4" &
python 'src/main.py' -i 'data/TN_07012018.csv' 'Entries_KIN' 'Exits_KIN' "Tennessee KIN" --coloring 3 --render "renderings/TN_KIN_seasonal_discrete.mp4" &

wait
echo Done Rendering.

#!/bin/bash
limit=100
coloring=5
for filename in preprocessed_data/*.csv; do
    c1="${filename%_*}"
    stateid="${c1##*/}"
    if [ "$stateid" != "NAT" ]; then
        echo $stateid
        python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PCC --limit $limit --render "renderings/${stateid}_PCC_${coloring}.mp4" &
        python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PKC --limit $limit --render "renderings/${stateid}_PKC_${coloring}.mp4" &
        python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PFC --limit $limit --render "renderings/${stateid}_PFC_${coloring}.mp4" &
        python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype POT --limit $limit --render "renderings/${stateid}_POT_${coloring}.mp4" &
        python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PTC --limit $((2 * limit)) --render "renderings/${stateid}_PTC_${coloring}.mp4" &
        wait
    fi
done

stateid="NAT"
echo $stateid
python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PCC --limit $((5 * limit)) --render "renderings/${stateid}_PCC_${coloring}.mp4" &
python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PKC --limit $((5 * limit)) --render "renderings/${stateid}_PKC_${coloring}.mp4" &
python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PFC --limit $((5 * limit)) --render "renderings/${stateid}_PFC_${coloring}.mp4" &
python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype POT --limit $((5 * limit)) --render "renderings/${stateid}_POT_${coloring}.mp4" &
python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PTC --limit $((10 * limit)) --render "renderings/${stateid}_PTC_${coloring}.mp4" &
wait

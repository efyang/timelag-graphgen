#!/bin/bash
coloring=5
for filename in preprocessed_data/*.csv; do
    c1="${filename%_*}"
    stateid="${c1##*/}"
    if [ "$stateid" != "NAT" ]; then
        echo $stateid
        IFS=' ' read -r -a limits <<< `python src/find_limit.py $filename`
        python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PCC --limit ${limits[0]} --render "renderings/${stateid}_PCC_${coloring}.mp4" --dropyearly &
        python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PKC --limit ${limits[0]} --render "renderings/${stateid}_PKC_${coloring}.mp4" --dropyearly &
        python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PFC --limit ${limits[0]} --render "renderings/${stateid}_PFC_${coloring}.mp4" --dropyearly &
        python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype POT --limit ${limits[0]} --render "renderings/${stateid}_POT_${coloring}.mp4" --dropyearly &
        python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PTC --limit ${limits[1]} --render "renderings/${stateid}_PTC_${coloring}.mp4" --dropyearly &
        wait
    fi
done

filename='preprocessed_data/NAT_PREPROCESSED.csv'
echo $stateid
IFS=' ' read -r -a limits <<< `python src/find_limit.py $filename`
python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PCC --limit ${limits[0]} --render "renderings/${stateid}_PCC_${coloring}.mp4" --dropyearly &
python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PKC --limit ${limits[0]} --render "renderings/${stateid}_PKC_${coloring}.mp4" --dropyearly &
python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PFC --limit ${limits[0]} --render "renderings/${stateid}_PFC_${coloring}.mp4" --dropyearly &
python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype POT --limit ${limits[0]} --render "renderings/${stateid}_POT_${coloring}.mp4" --dropyearly &
python src/main2.py -i "$filename" -f weekssp -s "$stateid" --coloring 5 --caretype PTC --limit ${limits[1]} --render "renderings/${stateid}_PTC_${coloring}.mp4" --dropyearly &
wait

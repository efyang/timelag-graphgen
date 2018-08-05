#!/bin/bash
coloring=5
output_head="renderings/wave3"
mkdir -p $output_head
while IFS='' read -r stateid || [[ -n "$stateid" ]]; do
    echo $stateid
    output_prefix="$output_head/$stateid"
    mkdir -p $output_prefix
    filename="preprocessed_data/${stateid}_DAILY_PREPROCESSED.csv"
    IFS=' ' read -r -a limits <<< `python src/find_limit.py $filename`
    echo "${limits[*]}"
    echo "Render pictures"
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PCC --limit ${limits[0]} --render "$output_prefix/${stateid}_PCC_${coloring}.png" --lag 7 &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PKC --limit ${limits[0]} --render "$output_prefix/${stateid}_PKC_${coloring}.png" --lag 7 &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PFC --limit ${limits[0]} --render "$output_prefix/${stateid}_PFC_${coloring}.png" --lag 7 &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype POT --limit ${limits[0]} --render "$output_prefix/${stateid}_POT_${coloring}.png" --lag 7 &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PTC --limit ${limits[1]} --render "$output_prefix/${stateid}_PTC_${coloring}.png" --lag 7 &
    wait

    echo "Render animations"
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PCC --limit ${limits[0]} --render "$output_prefix/${stateid}_PCC_${coloring}.mp4" --dropyearly --lag 7 &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PKC --limit ${limits[0]} --render "$output_prefix/${stateid}_PKC_${coloring}.mp4" --dropyearly --lag 7 &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PFC --limit ${limits[0]} --render "$output_prefix/${stateid}_PFC_${coloring}.mp4" --dropyearly --lag 7 &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype POT --limit ${limits[0]} --render "$output_prefix/${stateid}_POT_${coloring}.mp4" --dropyearly --lag 7 &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PTC --limit ${limits[1]} --render "$output_prefix/${stateid}_PTC_${coloring}.mp4" --dropyearly --lag 7 &
    wait
done < src/wave3_states.txt

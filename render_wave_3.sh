#!/bin/bash
coloring=5
output_head=$2
lag=$1
echo "lag: $lag"
mkdir -p $output_head
while IFS='' read -r stateid || [[ -n "$stateid" ]]; IFS='' read -r stateid2 || [[ -n "$stateid2" ]]; do
    echo $stateid
    echo $stateid2
    output_prefix="$output_head/$stateid"
    output_prefix2="$output_head/$stateid2"
    mkdir -p $output_prefix
    mkdir -p $output_prefix2
    filename="preprocessed_data/${stateid}_DAILY_PREPROCESSED.csv"
    filename2="preprocessed_data/${stateid2}_DAILY_PREPROCESSED.csv"

    IFS=' ' read -r -a limits <<< `python src/find_limit.py $filename`
    echo "${limits[*]}"
    IFS=' ' read -r -a limits2 <<< `python src/find_limit.py $filename2`
    echo "${limits2[*]}"

    echo "Render pictures"
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PCC --limit ${limits[0]} --render "$output_prefix/${stateid}_PCC_${coloring}.png" --lag $lag &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PKC --limit ${limits[0]} --render "$output_prefix/${stateid}_PKC_${coloring}.png" --lag $lag &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PFC --limit ${limits[0]} --render "$output_prefix/${stateid}_PFC_${coloring}.png" --lag $lag &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype POT --limit ${limits[0]} --render "$output_prefix/${stateid}_POT_${coloring}.png" --lag $lag &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PTC --limit ${limits[1]} --render "$output_prefix/${stateid}_PTC_${coloring}.png" --lag $lag &

    python src/main2.py -i "$filename2" -f dayssp -s "$stateid2" --coloring 3 --caretype PCC --limit ${limits2[0]} --render "$output_prefix2/${stateid2}_PCC_${coloring}.png" --lag $lag &
    python src/main2.py -i "$filename2" -f dayssp -s "$stateid2" --coloring 3 --caretype PKC --limit ${limits2[0]} --render "$output_prefix2/${stateid2}_PKC_${coloring}.png" --lag $lag &
    python src/main2.py -i "$filename2" -f dayssp -s "$stateid2" --coloring 3 --caretype PFC --limit ${limits2[0]} --render "$output_prefix2/${stateid2}_PFC_${coloring}.png" --lag $lag &
    python src/main2.py -i "$filename2" -f dayssp -s "$stateid2" --coloring 3 --caretype POT --limit ${limits2[0]} --render "$output_prefix2/${stateid2}_POT_${coloring}.png" --lag $lag &
    python src/main2.py -i "$filename2" -f dayssp -s "$stateid2" --coloring 3 --caretype PTC --limit ${limits2[1]} --render "$output_prefix2/${stateid2}_PTC_${coloring}.png" --lag $lag &

    wait

    echo "Render animations"
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PCC --limit ${limits[0]} --render "$output_prefix/${stateid}_PCC_${coloring}.mp4" --dropyearly --lag $lag --ppf 7 &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PKC --limit ${limits[0]} --render "$output_prefix/${stateid}_PKC_${coloring}.mp4" --dropyearly --lag $lag --ppf 7 &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PFC --limit ${limits[0]} --render "$output_prefix/${stateid}_PFC_${coloring}.mp4" --dropyearly --lag $lag --ppf 7 &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype POT --limit ${limits[0]} --render "$output_prefix/${stateid}_POT_${coloring}.mp4" --dropyearly --lag $lag --ppf 7 &
    python src/main2.py -i "$filename" -f dayssp -s "$stateid" --coloring 3 --caretype PTC --limit ${limits[1]} --render "$output_prefix/${stateid}_PTC_${coloring}.mp4" --dropyearly --lag $lag --ppf 7 &

    python src/main2.py -i "$filename2" -f dayssp -s "$stateid2" --coloring 3 --caretype PCC --limit ${limits2[0]} --render "$output_prefix2/${stateid2}_PCC_${coloring}.mp4" --dropyearly --lag $lag --ppf 7 &
    python src/main2.py -i "$filename2" -f dayssp -s "$stateid2" --coloring 3 --caretype PKC --limit ${limits2[0]} --render "$output_prefix2/${stateid2}_PKC_${coloring}.mp4" --dropyearly --lag $lag --ppf 7 &
    python src/main2.py -i "$filename2" -f dayssp -s "$stateid2" --coloring 3 --caretype PFC --limit ${limits2[0]} --render "$output_prefix2/${stateid2}_PFC_${coloring}.mp4" --dropyearly --lag $lag --ppf 7 &
    python src/main2.py -i "$filename2" -f dayssp -s "$stateid2" --coloring 3 --caretype POT --limit ${limits2[0]} --render "$output_prefix2/${stateid2}_POT_${coloring}.mp4" --dropyearly --lag $lag --ppf 7 &
    python src/main2.py -i "$filename2" -f dayssp -s "$stateid2" --coloring 3 --caretype PTC --limit ${limits2[1]} --render "$output_prefix2/${stateid2}_PTC_${coloring}.mp4" --dropyearly --lag $lag --ppf 7 &


    wait
done < src/wave3_states.txt

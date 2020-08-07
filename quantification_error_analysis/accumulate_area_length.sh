file=$1
temp=(`echo ${file[i]}| cut -d '.' -f 1`)
python accumulate_area_length.py --input $file --output ${temp}_accu.txt

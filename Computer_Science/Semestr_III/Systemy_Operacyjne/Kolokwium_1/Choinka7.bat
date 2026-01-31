odstep=$1
poziomy=$2
tmp_odstep=$odstep
for((i=1;i<=$2;i++)); do
    for ((j=0;j<odstep;j++)); do
        echo -n " "
    done

    for((j=0;j<2*i+1;j++)); do
        if [ $((i%5)) -eq 3] && [ $j -eq 0 ]; then
            echo -n "|"
        elif [ $((i%5)) -eq 3] && [ $j -eq $((2*i)) ]; then
            echo -n "|"
        else
            echo -n "$3"
        fi    
    done
    odstep=$((tmp_odstep-1))
    echo
done

for((i=0;i<2;i++)); do
    for((j=0;j<tmp_odstep;j++)); do
        echo -n " "
    done

    echo "$3"
done
temp_odstep=$2
odstep=$2
for ((p=1;p<=$3;p++)); do
        odstep=temp_odstep
        for ((i=0;i<p;i++)); do

                #rysujemy spacje
                for ((j=0;j<odstep;j++)); do
                        echo -n " "
                done

                #rysujemy znaki
                for((j=0;j<2*i+1;j++)); do
                        echo -n "$1"
                done
                odstep=$((odstep-1))
                echo
        done
done

#rysujemy pien choinki
for((i=0;i<2;i++)); do
        for((j=0;j<temp_odstep;j++)); do
                echo -n " "
        done

        echo "$1"
done


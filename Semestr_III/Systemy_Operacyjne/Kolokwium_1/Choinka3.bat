temp_odstep=20
for ((p=2;p<=$1+1;p++)); do
        odstep=temp_odstep
        for ((i=0;i<p;i++)); do

                #rysujemy spacje
                for ((j=0;j<odstep-i;j++)); do
                        echo -n " "
                done

                #rysujemy znaki
                for((j=0;j<2*i+1;j++)); do
                        echo -n "$2 "
                done
                odstep=$((odstep-1))
                echo
        done
done

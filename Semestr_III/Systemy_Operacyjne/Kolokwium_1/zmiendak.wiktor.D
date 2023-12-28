if [ "$#" -eq 0 ]; then
	echo -n "Bledna ilosc parametrow"
	echo
	exit 7
elif [ "$#" -gt 2 ]; then
	echo -n "Bledna ilosc parametrow"
	echo
	exit 7
fi

while true
do
    echo -n "1. awk"
    echo
    echo -n "2. rysowanie"
    echo
    echo -n "3. koniec"
    echo
    read wybor
    if [ $wybor -eq 1 ]; then
	numer_kol1=$1
	numer_kol2=$2
	echo -n "Wczytaj tekst"
	echo
	read tekst
	echo -n "Wczytaj plik dane"
	echo
	read dane
	suma=0
	echo -n "Suma: $suma"
	echo
    elif [ $wybor -eq 2 ]; then
	if [ $(($1%2)) -eq 0 ]; then
		echo -n "Pierwszy parametr musi byc nieparzysty"
		echo
		exit 7
	fi
        echo -n "Podaj znak"
	echo
	read znak
	odstep=$1
	for ((i=1;i<=$1;i=i+2)); do
		for ((z=0;z<i;z++)); do
			for ((j=0;j<=$odstep;j++)); do
				echo -n " "
			done
			for ((k=0;k<i;k++)); do
				echo -n "$znak"
			done
			echo
		done
		((odstep--))
	done
    elif [ $wybor -eq 3 ]; then
        exit 7
    else
        echo -n "bledne dane"
	echo
    fi
done

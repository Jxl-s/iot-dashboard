declare -A devices

while IFS= read -r line; do    
    first_word=$(echo "$line" | awk '{print $1}')
    third_word=$(echo "$line" | awk '{print $3}')
    fourth_word=$(echo "$line" | awk '{print $4}')
    fifth_word=$(echo "$line" | awk '{print $5}')

    if [[ $first_word == *"NEW"* ]]; then
        devices["$third_word"]=-999
    fi

    if [[ $first_word == *"DEL"* ]]; then
        unset devices["$third_word"]
    fi

    if [[ $first_word == *"CHG"* && $fourth_word == "RSSI:" ]]; then
        devices["$third_word"]=$fifth_word
    fi

    echo "" > bl.out
    
    for mac in "${!devices[@]}"; do
        echo -e "$mac ${devices[$mac]}" >> bl.out
    done

done < <(bluetoothctl scan on)
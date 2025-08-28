#!bin/bash

DEST="$HOME/Code/ghibli/color_picker/img/thewindrises"

i=1

while true; do
  num=$(printf "%03d" $i)
  url="https://www.ghibli.jp/gallery/kazetachinu${num}.jpg"
  
  http_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")

  if["http_code" -ne 200]; then
    echo "Stopping. Received ${http_code} from ${url}."
    break
  else
    output="$DEST/thewindrises${num}.jpg"
    echo "Downloading from ${url}"
    curl -o "$output" "$url"
  fi

  i=$((i+1))
done


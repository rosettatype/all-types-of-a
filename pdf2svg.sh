cd assets/letters
for f in *.pdf;
do 
    if [ -f "$f" ]; then 
        pdf2svg "$f" "${f//pdf/svg}"
    fi
done
cd ../..
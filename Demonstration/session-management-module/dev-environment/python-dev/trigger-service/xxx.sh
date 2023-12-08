image_ids=$(awk '{if(NR>1) print $3}' input.txt)

# Deleting each image by ID
for image_id in $image_ids; do
    docker image rm $image_id
     
done

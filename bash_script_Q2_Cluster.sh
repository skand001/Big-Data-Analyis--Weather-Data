#!/bin/bash

# Define the range of k values to test
start_k=2
end_k=10

# Define the directory paths to your Mahout vectors and output
input_dir="docs-vectors/tfidf-vectors"
output_dir="docs-kmeans-clusters"
canopy_centroids="docs-vectors/docs-canopy-centroids"

# Choose your distance measure
distance_measure="org.apache.mahout.common.distance.CosineDistanceMeasure"

# Loop through the range of k values
for ((k=start_k; k<=end_k; k++)); do
    echo "Running K-means with k=$k"
    
    # Define output subdirectory for the current k
    output_subdir="${output_dir}-cosine-k$k"
    
    # Run the Mahout kmeans command
    mahout kmeans \
        -i $input_dir \
        -c $canopy_centroids \
        -o $output_subdir \
        -dm $distance_measure \
        -cl \
        -cd 0.1 \
        -ow \
        -x 20 \
        -k $k
    
    # Evaluate the clusters and capture the evaluation metrics
    mahout clusterdump \
        -i ${output_subdir}/clusters-*-final \
        -o ${output_subdir}/clusterdump.txt \
        -of TEXT \
        -b 100 \
        -p ${output_subdir}/clusteredPoints \
        -d $input_dir/dictionary.file-* \
        -dt sequencefile \
        -n 20 --evaluate
    
    # Extract the relevant metrics from the clusterdump output
    inter_cluster_density=$(grep "Inter-Cluster Density" ${output_subdir}/clusterdump.txt | cut -d ':' -f2)
    intra_cluster_density=$(grep "Intra-Cluster Density" ${output_subdir}/clusterdump.txt | cut -d ':' -f2)
    
    # Append the metrics to a file for later analysis
    echo "$k $inter_cluster_density $intra_cluster_density" >> kmeans_evaluation.txt

done


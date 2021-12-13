#!/bin/bash
# Function: run potree convert in docker and generate html for potree web view
# Usage:
#     # porun.sh /home/oceanx/test.las
#     Parameter: input the point cloud path, e.g. "/home/oceanx/test.las"
#     Authority: chmod +x porun.sh 

# 1) sudo docker run -it potreetransform /bin/bash
# 2) Input: ${path}${filename}, 例如: {/home/a/b/c/}{test.las}
# sudo docker run -it -v ${path}:/usr/src/app/data/ -v /home/oceanx/Documents/oceanx-pcloud/html:/usr/src/app/dataview/ potreetransform /usr/src/app/run.sh ${filename}



# var=/home/pointcloud/3Sdata.las
var=$1

# Judge whether input string is empty 
if [ -z "$var" ];then
echo "Please input the point cloud data path for conversion."
exit
fi

echo "The point cloud data for conversion: ${var}."

path=${var%/*}    # /home/oceanx
file=${var##*/}   # test.las
basename=${file%%.*}  # test
suffix=${file##*.}    # las

# echo $path
# echo $file
# echo $basename
# echo $suffix


input="./data/$file"
output="./dataview/${basename}"

/usr/src/app/PotreeConverter ${input} -o ${output}


################################
# Generate html
################################

# genrate html file
ppc_path="./${basename}/metadata.json" 
html_path="./dataview/${basename}.html"
python3 ./genhtml.py --ppc-path $ppc_path --save-path $html_path

echo "Finished data conversion and html generation!"
echo "The original point cloud data is at ${var}."
echo "The converted point cloud data (Potree) is at ${ppc_path}."
echo "The html used for web view is at ${html_path}."




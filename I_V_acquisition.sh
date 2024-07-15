#!/bin/sh

acquired_data_file="acquired_data.txt"
data_path="./data/"
#
#FBK tile one
tile_produser="FBK"
tile_ID="01"
#
#
out_log_file="$data_path$tile_produser"_"TILE$tile_ID".log
#mkdir -p $data_path

function printHelp {
    echo " --> ERROR in input arguments"
    echo " [0] -d : (IV measurements)"
    echo " [1]    : CHID in format (00 .. 63)"
    echo " [0] -t : test"
    echo " [0] -h : print help"
}

if [ $# -eq 0 ];
then    
    printHelp
else
    if [ "$1" = "-d" ]; then
        if [ $# -eq 2 ]; then
            CHID=$2
	    data_time_start=$(date '+%d.%m.%Y-%H:%M:%S')
	    echo "data_time_start     $data_time_start" | tee -a $out_log_file
	    echo "data_path           $data_path" | tee -a $out_log_file
	    echo "tile_produser       $tile_produser" | tee -a $out_log_file
	    echo "tile_ID             $tile_ID" | tee -a $out_log_file
	    echo "CHID                $CHID" | tee -a $out_log_file
	    echo "out_log_file        $out_log_file" | tee -a $out_log_file
	    out_data_file_name=$data_path$tile_produser"_"TILE"$tile_ID"_"CH"$CHID'.txt'
	    echo "out_data_file_name  $out_data_file_name" | tee -a $out_log_file	    
	    #time python I_V_acquisition.py  | tee -a $out_log_file
	    #mv acquired_data.txt $out_data_file_name  | tee -a $out_log_file
	    data_time_end=$(date '+%d.%m.%Y-%H:%M:%S')
	    echo "data_time_end       $data_time_end" | tee -a $out_log_file
	    echo " " | tee -a $out_log_file
	    echo " " | tee -a $out_log_file
	    echo " " | tee -a $out_log_file
	else
            printHelp
        fi
       elif [ "$1" = "-t" ]; then
	time python I_V_acquisition.py
    elif [ "$1" = "-h" ]; then
        printHelp
    else
        printHelp
    fi
fi

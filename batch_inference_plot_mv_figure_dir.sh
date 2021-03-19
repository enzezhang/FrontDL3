
#need to modify the data path first

para_file=para.ini
para_py=./script/parameters.py
working_path=$(python2 ${para_py} -p ${para_file} working_root)
data_path=$(python2 ${para_py} -p ${para_file} data_path)

list=Glacier_ID_list.txt
network=$1

if [  $network ];then
	echo "ok"
else
	echo "please input the network"
	exit 1
fi
cat $list | while read GID
do
	ID=${GID#*GID}
	GID2=GID_${ID}
	echo "bash batch_inference.sh $data_path/${GID}  $data_path/${GID}/polygon/${GID2}_cutting_polygon.gmt $network"
	echo "bash batch_plot.sh $data_path/${GID} $network"
	echo "bash batch_mv_figure_dir.sh $data_path/${GID} $network"
done








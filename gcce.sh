shellFolder="/home/ayoub/ayoub/commands/shell/c_compiler/"

if [ "$1" == "" ];then
    echo "messing argument of files names"
    exit
fi

targetPath=`pwd`
pythonOut=`python3 ${shellFolder}makeHeaders.py $1 $targetPath `
files=`echo "$pythonOut" | grep -v "\->"`

if gcc main.c $files; then
    if [ "$2" != "-c" ];then
        ./a.out
    fi
fi
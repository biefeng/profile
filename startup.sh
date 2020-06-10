source /home/root/program/miniconda2/bin/activate blog_mini

cd /home/root/program/Blog_mini

nohup gunicorn -b 0.0.0.0:80 -p logs/pid  manage:app  > logs/log.out 2>&1 & 

if [ $? = "0" ];then
 echo "blog_mini starts successfully,the pid is: $!"
fi

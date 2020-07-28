source /home/root/program/miniconda2/bin/activate blog_mini

cd /home/root/program/profile

nohup gunicorn -b 0.0.0.0:8888 --access-logfile=logs/access.out  --access-logformat='{"remote_ip":"%(h)s","request_id":"%({X-Request-Id}i)s","response_code":"%(s)s","request_method":"%(m)s","request_path":"%(U)s","request_querystring":"%(q)s","request_timetaken":"%(D)s","response_length":"%(B)s"}' -p logs/pid  manage:app  > logs/log.out 2>&1 & 

if [ $? = "0" ];then
 echo "blog_mini starts successfully,the pid is: $!"
fi

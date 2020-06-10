#/bin/bash

if [ -e $(pwd)/logs/pid  ];then
  p=$(cat $(pwd)/logs/pid)
  kill 9 $p
  if [ $? = '0' ];then
    echo 'blog_mini stoped'
  fi 
else 
  echo "blog_mini has not been started!"
fi

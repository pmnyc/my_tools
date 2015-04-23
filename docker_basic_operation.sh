echo 'assign random container name' 
x=random_container_name 
echo 'create a docker through a bash command script' 
sudo docker run --name $x pengma/aws_ubuntu:v5 /bin/sh -c 'mkdir ~/image; cd ~/image; echo 1 > test.txt;' 
echo 'copy containers test.txt file into the container_output folder under host current path'
sudo docker cp $x:/root/image/test.txt $(pwd)/container_output

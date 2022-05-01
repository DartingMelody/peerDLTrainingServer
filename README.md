# peerDLTrainingServer
* attach to nfsserver follow https://www.tecmint.com/install-nfs-server-on-ubuntu/ , https://www.howtoforge.com/tutorial/how-to-configure-a-nfs-server-and-mount-nfs-shares-on-ubuntu-18.04/ make mount directory to file_store
* pip install flask
* run python database_gen.py -> This will create database and tables. 
* run python dispatcher.py -> This will dispatch jobs to resources
* run python app.py -> server for resource management,client interact to this. 

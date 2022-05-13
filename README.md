# peerDLTrainingServer
* attach to nfsserver follow https://www.tecmint.com/install-nfs-server-on-ubuntu/ , https://www.howtoforge.com/tutorial/how-to-configure-a-nfs-server-and-mount-nfs-shares-on-ubuntu-18.04/ make mount directory to file_store
* ```pip install flask```
* run ```python database_gen.py``` -> This will create database and tables. 
* run ```python credit_allocator.py ``` -> This will allocate credits to users.
* run ```python dispatcher.py``` -> This will dispatch jobs to resources
* For accessing flask server by public follow this https://www.socketxp.com/iot/how-to-access-python-flask-app-from-internet/ Basically you need to create an account here, get the token and connect socketxp with port 5000. 
* run ```python app.py``` -> server for resource management,client interact with this. 

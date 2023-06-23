import os 
import subprocess

<<<<<<< HEAD
hostname ="192.168.178.101"
=======
hostname ="192.168.178.100"
>>>>>>> main
#response = os.system("ping -c 1 " + hostname)
#response = os.system("ping -c 1 -w 2 " + hostname + " > /dev/null 2>&1")
#subprocess.run(["ping ", "-c ","1 ",hostname])
#response = subprocess.run(["ping ",hostname])
response = os.system("ping " + hostname)

#Ceck the response

if response == 0:
    response = os.system("ping " + hostname)
    print(f"{hostname} is up")
else:
    print(f"{hostname} is down")
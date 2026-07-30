import psutil
from system_utils import system_info
cpu = psutil.cpu_percent(interval=1)
cpu_time= psutil.cpu_times()

print(dir(psutil))
print(cpu_time)
print(psutil.cpu_count())
print(psutil.cpu_percent.__doc__)
if (cpu>50):
    print ("cpu is overloaded", cpu)
elif (cpu>40 and  cpu < 50):
    print("alert")
else:
    print("cpu is normal")    


for i in range(5):
    print(psutil.cpu_percent(interval=1))


threshold= float(input("Enter the threshold: "))
for i in range(5):
    if psutil.cpu_percent(interval=1)> threshold:
        print ("cpu is unhealthy")    
    else:
        print("cpu is healthy")    


system_info()     
The currunt regex based filter can take
```
 من time حضر localtime

 activities = {8: 'نوم',
               17: 'عمل',
               22: 'راحة' }

 time_now = localtime()
 hour = time_now.tm_hour

 لكل activity_time في sorted(activities.keys()):
     اذا hour < activity_time:
         اطبع (activities[activity_time])
         break
 اخيرا:
     اطبع ('Unknown, AFK أو sleeping!')
```
and turn it to this
``` python
from time import localtime

activities = {8: 'نوم',
              17: 'عمل',
              22: 'راحة' }

time_now = localtime()
hour = time_now.tm_hour

for activity_time in sorted(activities.keys()):
    if hour < activity_time:
        print (activities[activity_time])
        break
else:
    print ('Unknown, AFK or sleeping!')
```

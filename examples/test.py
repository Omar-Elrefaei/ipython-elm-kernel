 من time حضر localtime



 activities = {8: 'Sleeping',

               22: 'Resting' }



 time_now = localtime()

 hour = time_now.tm_hour



 لكل activity_time في sorted(activities.keys()):

     اذا hour < activity_time:

         اطبع (activities[activity_time])

         break

 اخيرا:

     اطبع ('Unknown, AFK أو sleeping!')

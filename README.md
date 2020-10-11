# HomeWebServer
 Small server for the home LAN.

 Currently only containing the LegacyPWM and an appointment reminder (Termine).
 Things that may be added:
 - Photo/Video Viewer
 - New PWM
 - ...
 
 Using Celery for distributed tasks, with rabbitmq running as broker.
 (While I'm aware that it is a bit overkill for the current project size, I chose to set it up for easier upscaling later on.)


I'm additionally aware, that the css is (at least) partly redundant and therefore a bit overkill, as I initially intended to design each app's look different - which didn't happen.
The css file will therefore be reduced, once I'm done with everything else.. or feel like it.

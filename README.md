# HomeWebServer
 Small server for the home LAN.

 Currently containing:
 - LegacyPWM
 - appointment reminder (Termine)
 - audiobooksDB

 Things that may be added:
 - Photo/Video Viewer
 - New PWM
 - ...


Served by Apache2 on Ubuntu Server.
Using Celery for distributed tasks, with rabbitmq running as broker.
(While I'm aware that it is a bit overkill for the current project size, I chose to set it up for easier upscaling later on.)

Additionally I'm aware, that the css is (at least) partly redundant and therefore a bit overkill, as I initially intended to design each app's look different - which didn't happen.
The css file will therefore be reduced, once I'm done with everything else.. or feel like it.

# HomeWebServer
 Small server for the home LAN.

 Currently only containing the LegacyPWM and an appointment reminder (Termine).
 Things that may be added:
 - Photo/Video Viewer
 - New PWM
 - ...
 
 Using Celery for distributed tasks, with rabbitmq running as broker.
 (While I'm aware that it is a bit overkill for the current project size, I chose to set it up for easier upscaling later on.)

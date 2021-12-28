This is a weather app and it has few functionalities:
<ol>
  <li>
    It automatically pulls data from weather API and stores it in the database.
  </li>
  <li>
    It automatically sends emails with the weather forecast for the current day
  </li>
  <li>
    It has an API which could show the weather forecast or to subscribe an email.
  </li>
</ol>
  
In order to set the project you should install the requirements.txt file as usual.
<ul>
  <li>
    For the API part I am using this one https://stormglass.io/, where you can register an get an API key for up to 10 free requests per day.
  </li>
  <li>
    For the email part I am using gmail as provider. Refer to gmail documentation on how to enable less secure apps access.
  </li>
  <li>
    For the scheduled task I am using Celery beat with rabbitMQ. Celery can be used with other services as well, which is described in the documentation.
    I will share the commands that I use to schedule and execute the tasks from Celery, as its documentation is a bit messy.
    Start a worker that would receive and execute tasks: "celery -A weather worker --loglevel=info --concurrency 1 -P solo"
    Start the Celery beat process: "celery -A weather beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler"
  </li>
</ul>

You need to set these environment variables:<br/>
EMAIL_HOST_USER<br/>
EMAIL_HOST<br/>
EMAIL_HOST_PASSWORD<br/>
SECRET_KEY<br/>
WEATHER_API_KEY<br/>

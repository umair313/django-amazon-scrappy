# Project Boilerplate
## install docker
https://docs.docker.com/engine/install/ubuntu/
## install make
https://www.gnu.org/software/make/

### Environment Setup

- Copy ENV file `cp config/env/.env.example .env`
- Update env variables

Run the command to build and run the application
- `make dev.build` : build containers
- `make dev.up` : start containers in attached mode

### create superuser

make dev.dcshell
```bash
python manage.py createsuperuser
```

login to admin
open `localhost:8001/admin`

### Add new Periodic Task

open `http://localhost:8001/admin/django_celery_beat/periodictask/`
- click on ADD Periodic Task
- set name
- from task drop down select `app.products.tasks.run_scrapper` 
- Under schedule set Crontab Schedule
  - minute: 0
  - Hour(s): 0,6,12,18
  - Days of the week: *
  - Days of the Month: *
  - Month of the year: *
  - Cron Timezone: UTC
 - save it.


you can also run the task by selecting it.

after running the task open http://localhost:8001/products/products/

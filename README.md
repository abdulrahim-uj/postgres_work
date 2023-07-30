# postgres_work
## database backup and restore

### TAKE BACKUP FROM DATABASE
    Apps: [accounts, tasklists]
    MODELS: [
        accounts: {User, Userprofile},
        tasklists: {Task}
    ]
#### 1. WHOLE DATABASE
    python manage.py dumpdata > whole_db.json

#### 2. SPECIFIC APP
    python manage.py dumpdata accounts > accounts.json

#### 3. SPECIFIC TABLE
    python manage.py dumpdata accounts.user > accounts_user.json
    python manage.py dumpdata accounts.userprofile > accounts_userprofile.json
    python manage.py dumpdata tasklists.task > tasklists_task.json

#### 4. EXCLUDE
    python manage.py dumpdata --exclude auth.permission > whole_db_x_perm.json

#### 5. USING INDENTATION
    python manage.py dumpdata accounts.user --indent 4 > accounts_user.json

#### 6. OUTPUT FORMAT
    python manage.py dumpdata accounts.user --indent 4 --format xml > accounts_user.xml
    python manage.py dumpdata accounts.user --indent 4 --format json > accounts_user.json

#### 7. FOR TAKE A BACKUP FOR FRESH PROJECT
    python manage.py dumpdata --exclude auth.permission --exclude contenttypes > whole_db_fresh.json

#### 8. LOAD DATA TO DATABASE
    python manage.py loaddata whole_db_fresh.json


## for schedule periodic backups
    pip install django-dbbackup

    python manage.py dbbackup       # for backup, create a bin file inside backups folder

    pip install django-apscheduler

    makemigrations & migrate    [django_apscheduler_djangojob, django_apscheduler_djangojobexecution]

## create a scheduler and backup functions
    from django.core.management import call_command
    from apscheduler.schedulers.background import BackgroundScheduler
    from django_apscheduler.jobstores import DjangoJobStore, register_events
    
    def my_db_backup_jobs():
        try:
            call_command('dbbackup')
        except Exception as e:
            print("SOMETHING WENT WRONG: : : ", e)

    
    def start_scheduler():
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        # day_of_week="mon", hour="00", minute="00"
        scheduler.add_job(my_db_backup_jobs, 'interval', minutes=10, jobstore="default",
                          id="minutes_10_db_backup", replace_existing=True)
        register_events(scheduler=scheduler)
        scheduler.start()

## set this into apps.py file
    class BasicsConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'app_name'
    
        def ready(self):
            from .functions import start_scheduler
            start_scheduler()

### not works in windows
    pip install django-crontab
    python manage.py crontab add    # for add
    python manage.py crontab show    # for show cron jobs
    python manage.py crontab remove  # for remove

from django.core.management import call_command
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events


def get_auto_id(model):
    auto_id = 1
    latest_auto_id = model.objects.all().order_by("-created_at")[:1]
    if latest_auto_id:
        for auto in latest_auto_id:
            auto_id = auto.auto_id + 1
    return auto_id


def generate_form_errors(args, formset=False):
    message = ''
    if not formset:
        for field in args:
            if field.errors:
                message += field.errors + "|"
        for err in args.non_field_errors():
            message += str(err) + "|"

    elif formset:
        for form in args:
            for field in form:
                if field.errors:
                    message += field.errors + "|"
            for err in form.non_field_errors():
                message += str(err) + "|"
    return message[:-1]


def my_db_backup_jobs():
    try:
        call_command('dbbackup')
    except Exception as e:
        print("SOMETHING WENT WRONG: : : ", e)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(my_db_backup_jobs, 'interval', minutes=1, jobstore="default",
                      id="minutes_db_backup", replace_existing=True)
    register_events(scheduler=scheduler)
    scheduler.start()

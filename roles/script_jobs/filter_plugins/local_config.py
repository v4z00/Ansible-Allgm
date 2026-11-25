"""Do not deploy controller notification credentials to autonomous job hosts."""
CHANNEL_KEYS = ('EMAIL', 'MAIL_TO', 'MAIL_FROM', 'BOT_TOKEN', 'TELEGRAM_BOT_TOKEN', 'TELEGRAM_TOKEN', 'CHAT_ID', 'TELEGRAM_CHAT_ID')


def local_job_config(values):
    if not isinstance(values, dict):
        raise ValueError('Job configuration must be an object')
    result = dict(values)
    # Empty compatibility fields keep old shell bodies with `set -u` usable.
    # Explicit flags also protect direct program calls outside the managed runner.
    result.update({key: '' for key in CHANNEL_KEYS})
    result.update(ENABLE_EMAIL_NOTIFICATION=False, ENABLE_TELEGRAM_NOTIFICATION=False)
    return result


class FilterModule:
    def filters(self):
        return {'script_jobs_local_config': local_job_config}

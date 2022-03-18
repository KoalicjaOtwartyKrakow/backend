import functools

import sentry_sdk


# https://github.com/getsentry/sentry-python/issues/1078#issuecomment-879149355
def sentry(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            sentry_sdk.flush()
            raise e

    return wrapper

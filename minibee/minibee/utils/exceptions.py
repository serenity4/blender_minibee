from ... import log


def add_msg_to_exception(ex, msg):
    old_msg = ex.args[0]
    new_msg = '\n'.join((old_msg, stradd))
    ex.args = (new_msg,)
    return ex


def log_and_raise_error(msg, exception_type):
    log.logger.error(msg)
    raise exception_type(msg)


def add_and_raise(msg, exception):
    exception = add_to_exception(ex, msg)
    raise exception

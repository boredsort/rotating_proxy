import logging


logger = logging.getLogger(__name__)

def attribute(func):
    def wrapper(*args, **kwargs):
        try:
            func_name = func.__name__
            logger.debug(f'Execute {func_name}')
            value = func(*args, **kwargs)

            if not value:
                value = 'NOT_FOUND'
                if 'port' in func_name:
                    return 0 

            if not isinstance(value, str):
                value = str(value)

            if value.strip() == '':
                value = 'NOT_FOUND'

        except Exception as e:
            logging.Logger(e)
            value = 'Extraction Failed'

        return value


    return wrapper

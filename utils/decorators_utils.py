# -----------BASE DECORATOR---------------
# def decorator(func):
#     def wrapped_func(func, *args, **kwargs):
#         DO SOMETHING
#         func(*args, **kwargs)
#         DO SOMETHING
#
#     return wrapped_func

# -----------ClASS DECORATOR---------------

# class decorator(object):
#     def __init__(self, name):
#         self.name = name
#
#     def __call__(self, func):
#
#         def wrapped_func(*args, **kwargs):
#           DO SOMETHING
#           func(*args, **kwargs)
#           DO SOMETHING
#
#         return wrapped_func
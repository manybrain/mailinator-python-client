print("Hello world")


# Import localsettings if any
try:
    from localsettings import *
except ImportError:
    pass

print("API_TOKEN ", API_TOKEN)
# Entry point for the application
from . import app   # For application discovery by the 'Flask' command
from . import views     # For import side-effects of setting up routes
from . import services  # For import logic and database operation
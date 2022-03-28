class AppError(Exception):
    def __init__(self, message=None, status=400):
        self.message = message
        self.status = status

    def __str__(self):
        return f"App error ({self.status}): {self.message}"

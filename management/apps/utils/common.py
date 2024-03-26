class Common:
    def __init__(self) -> None:
        pass

    def format_time(self, time_obj):
        # Format time as 6:52:29 PM
        return time_obj.strftime('%I:%M:%S %p')
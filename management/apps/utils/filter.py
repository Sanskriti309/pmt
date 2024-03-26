class GlobalFilter:

    def __init__(self):
        pass

    def check_access(self, request):
        if not request.user.is_authenticated:
            return {
                "isEmployee": False,
                "isStudent": False,
                "isManager": False,
                "isAdmin": False,
                "isMarketing":False
            }

        group_names = {group.name for group in request.user.groups.all()}

        return {
            "isEmployee": self.is_in_group(group_names, "Employee"),
            "isStudent": self.is_in_group(group_names, "Students"),
            "isManager": self.is_in_group(group_names, "Manager"),
            "isAdmin": self.is_in_group(group_names, "Admin"),
            "isMarketing": self.is_in_group(group_names, "Marketing")
        }

    def check_access_filter(self, request, access_level):
        data = self.check_access(request)
        is_any = any(data.get(permission, False) for permission in access_level)
        return is_any

    def is_in_group(self, group_names, group_name):
        return group_name in group_names

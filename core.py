# Context
class Context(object):
    def __init__(self, project, shot, task):
        self.project = project
        self.shot = shot
        self.task = task

    def isvalid(self) -> bool:
        """
        Check if the context is valid

        :return: <type 'bool'>
        """

        for item in [self.project, self.shot, self.task]:
            if not item:
                return False

            if not isinstance(item, str) or not item.isalpha():
                return False

        return True


if __name__ == '__main__':
    pass

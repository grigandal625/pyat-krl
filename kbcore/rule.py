class BaseRule:

    def check(self, **kwargs) -> bool:
        pass

    def fire(self, **kwargs):
        pass
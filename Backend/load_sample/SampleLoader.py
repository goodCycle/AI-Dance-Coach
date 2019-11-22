

class SampleLoader:

    def __call__(self, *args, **kwargs):
        return self.list_difference(*args, **kwargs)
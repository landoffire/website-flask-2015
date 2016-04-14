class Nav(object):
    registry = []

    def __init__(self, title, ref=None, url=None, external=False):
        self.title = title
        self.ref = ref if ref is not None else title.lower()
        self.url = url if url is not None else '/' + self.ref
        self.external = external

        self.registry.append(self)

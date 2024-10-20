class Unique(object):
    def __init__(self, items, **kwargs):
        self.items = iter(items)
        self.seen = set()
        self.ignore_case = kwargs.get('ignore_case', False)

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            item = next(self.items)

            comp_item = item.lower() if self.ignore_case and isinstance(item, str) else item

            if comp_item not in self.seen:
                self.seen.add(comp_item)
                return item

if __name__ == "__main__":
    data = [1, 1, 2, 2, 3, 3, 4, 4, 'a', 'A', 'b', 'B', 'a', 'A']
    print(list(Unique(data)))
    print(list(Unique(data, ignore_case=True)))
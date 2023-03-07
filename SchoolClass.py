

class SchoolClass:
    def __init__(self, name: str, taken: bool, offered: list[bool], pre_reqs: list[str]) -> None:
        self.quaters = ['Fall', 'Winter', 'Spring']
        self.name = name
        self.taken = taken
        self.offered = {self.quaters[i]: offered[i]
                        for i in range(len(self.quaters))}
        self.pre_reqs = set(pre_reqs)
        self.post_classes = set()
        self.chain_len: int = 0
        self.chain = []

    def get_taken(self) -> bool:
        return self.taken

    def get_pre_reqs(self) -> set[str]:
        return self.pre_reqs

    def get_post_classes(self) -> set[str]:
        return self.post_classes

    def get_chain_len(self) -> int:
        return self.chain_len

    def set_chain_len(self, length: int) -> None:
        self.chain_len = length

    def add_post_class(self, sch_class: str) -> None:
        self.post_classes.add(sch_class)

    def remove_pre_req(self, class_taken: set[str]) -> None:
        self.pre_reqs = self.pre_reqs.difference(class_taken)

    def __str__(self):
        return str([self.name, self.taken, self.offered, list(self.pre_reqs)])

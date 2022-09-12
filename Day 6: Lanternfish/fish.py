from dataclasses import dataclass

@dataclass
class Fish:
    timer: int = 9

    def progress(self, group: list) -> None:
        if not self.timer:
            self.new_fish(group)
            self.timer = 7
        self.timer -= 1

    @staticmethod
    def new_fish(group: list) -> None:
        group.append(Fish())


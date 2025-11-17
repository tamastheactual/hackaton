from dataclasses import dataclass

@dataclass(frozen=True)
class Car:
    manufacturer: str
    model: str
    age: int
    owners: list[str] = []

MG = Car('SAIC Motor', 'MG6', 15, ["Albert Deed", "Florian"])
MG.age += 1
print(MG)

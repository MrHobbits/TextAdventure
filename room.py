import json
# holds all the blocks info


def get_blocks():
    locations = []
    with open("game.json", "r") as f:
        jsontext = f.read()
        d = json.loads(jsontext)
        blocks = (d["block"])
    for x in blocks:
        locations.append(Block(**x))
    return locations 


class Block():
    def __init__(self, ident="", name="A room", 
            description="an empty room", 
            neighbours={}, items={},
            hasEnemy=False, enemy=None):
        self.ident=ident
        self.name=name
        self.description=description
        self.neighbours = neighbours
        self.items = items
        self.hasEnemy = hasEnemy
        self.enemy = enemy

    def _neighbour(self, direction):
        if direction in self.neighbours:
            return self.neighbours[direction]
        else:
            return None

    def _item(self, item):
        if item in self.items:
            return self.items[item]
        else:
            return None

    def removeItem(self, item):
        # remove the itemm from the import dictionary
        self.items.pop(item, None)

    def returnItems(self):
        # return a list of items in the room
        return list(self.items.keys())

    def _enemy(self):
        return self.enemy

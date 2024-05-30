import playerFile


class Power: # TEST
    def __init__(self):
        pass

    def event_listener(self, ev, player, list_of_enemies):
        if ev.type == playerFile.ON_ATTACK_PLAYED:
            player.add_armor(2, player)




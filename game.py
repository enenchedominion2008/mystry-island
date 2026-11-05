
CONNECTIONS = {
    "beach":      ["jungle"],
    "jungle":     ["beach", "cave"],
    "cave":       ["jungle", "old bridge"],
    "old bridge": ["cave", "lighthouse"],
    "lighthouse": ["old bridge"],
}

MAX_ENERGY = 5


def new_game(name):
    return {
        "name": name.strip().capitalize() or "Explorer",
        "location": "beach",
        "energy": MAX_ENERGY,
        "inventory": [],          
        "game_over": False,
        "won": False,
    }


def available_destinations(player):
    """Return the list of place names the player may move to."""
    return list(CONNECTIONS.get(player["location"], []))


def can_cross_bridge(player):
    return player["location"] == "cave" and "rope" in player["inventory"]


def can_light_beacon(player):
    """True if at lighthouse with lantern. (Test T7.)"""
    return player["location"] == "lighthouse" and "lantern" in player["inventory"]


def collect_item(player, item):
    """Add item to inventory once. Returns True if collected now."""
    if item in player["inventory"]:
        return False
    player["inventory"].append(item)
    return True


def move(player, destination):

    if player["game_over"]:
        return False, "The game is over. Replay to try again."
    if destination not in CONNECTIONS.get(player["location"], []):
        return False, f"You cannot go to {destination} from here."
    if destination == "lighthouse" and "rope" not in player["inventory"]:
        return False, "The bridge is broken — you need rope to cross. (No energy lost.)"

    player["location"] = destination
    player["energy"] -= 1

    if player["energy"] <= 0:
        player["energy"] = 0
        player["game_over"] = True
        player["won"] = False
        return True, f"You reach {destination} but collapse from exhaustion. GAME OVER."

    return True, f"You travel to {destination}. Energy left: {player['energy']}."


def light_beacon(player):
 
    if player["game_over"]:
        return False, "The game is over."
    if not can_light_beacon(player):
        return False, "You cannot light the beacon here (or you lack the lantern)."
    player["won"] = True
    player["game_over"] = True
    return True, f" {player['name']} lights the beacon! The rescue boat sees you. YOU WIN!"


def is_win(player):
    return player.get("won", False)


def is_loss(player):
    return player.get("game_over", False) and not player.get("won", False)
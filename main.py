from game import (new_game, available_destinations, move,
                  light_beacon, collect_item, is_win, is_loss)


def show_intro():
    print("=" * 60)
    print("  MYSTERY ISLAND — The Lost Lighthouse")
    print("=" * 60)
    print("You wake on a beach after a storm. The lighthouse is dark.")
    print("Find rope and a lantern, cross the old bridge, light the beacon.")
    print("Energy starts at 5. Invalid choices never cost energy.\n")


def show_status(player):
    print(f"\n-- {player['name']} --")
    print(f"Location : {player['location']}")
    print(f"Energy   : {player['energy']}")
    print(f"Inventory: {player['inventory'] or 'empty'}")
    print(f"Exits    : {', '.join(available_destinations(player)) or 'none'}")
    print("Actions  : (1) look  (2) move  (3) light beacon  (4) quit")


def look(player):
    loc = player["location"]
    if loc == "beach":
        print("Waves crash. A rusted lantern lies half-buried in the sand.")
        if collect_item(player, "lantern"):
            print(">>> You picked up the lantern. <<<")
    elif loc == "jungle":
        print("Vines everywhere. A coil of rope hangs from a branch.")
        if collect_item(player, "rope"):
            print(">>> You picked up the rope. <<<")
    elif loc == "cave":
        print("Damp stone. The old bridge creaks to the north.")
    elif loc == "old bridge":
        print("Rope planks sway. The lighthouse looms ahead.")
    elif loc == "lighthouse":
        print("A dark beacon waits for a flame. Use action 3 to light it.")


def choose_move(player):
    dests = available_destinations(player)
    if not dests:
        print("No exits from here.")
        return
    print("Where to?")
    for i, d in enumerate(dests, start=1):
        print(f"  ({i}) {d}")
    raw = input("choose >> ").strip().lower()
    if not raw.isdigit() or not (1 <= int(raw) <= len(dests)):
        print("Invalid choice — staying put.")
        return
    ok, msg = move(player, dests[int(raw) - 1])
    print(msg)


def play_once():
    show_intro()
    name = input("YOUR NAME: ")
    player = new_game(name)
    while not player["game_over"]:
        show_status(player)
        raw = input("choose >> ").strip().lower()
        if raw in ("4", "q", "quit", "exit"):
            print("You quit. The island keeps its secrets.")
            return
        elif raw == "1":
            look(player)
        elif raw == "2":
            choose_move(player)
        elif raw == "3":
            ok, msg = light_beacon(player)
            print(msg)
        else:
            print("Unknown option — try 1, 2, 3 or 4. (No energy lost.)")

    if is_win(player):
        print(f"\n {player['name']}, you escaped Mystery Island!")
    else:
        print(f"\n {player['name']}, you ran out of energy. The island wins this round.")


def main():
    while True:
        play_once()
        again = input("\nPlay again? (y/n) >> ").strip().lower()
        if again not in ("y", "yes"):
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
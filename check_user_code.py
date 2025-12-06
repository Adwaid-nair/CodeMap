import radon.complexity as radon_cc
import radon.visitors as radon_visitors

code = """
import random
import time

# Map layout
rooms = {
    "Base": ["Lab", "Hangar"],
    "Lab": ["Base", "Armory"],
    "Hangar": ["Base", "Wasteland"],
    "Armory": ["Lab"],
    "Wasteland": ["Hangar", "Alien Nest"],
    "Alien Nest": []
}

# Items and enemies
items = {
    "Lab": "Medkit",
    "Armory": "Laser Gun",
    "Wasteland": "Shield",
}

enemies = {
    "Wasteland": "Alien Scout",
    "Alien Nest": "Alien Queen"
}

# Player state
player_room = "Base"
inventory = []
health = 100

def slow_print(text):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(0.01)
    print()

def show_status():
    print("\\n----------------------------")
    print(f"Location: {player_room}")
    print(f"Health: {health}")
    print(f"Inventory: {inventory}")
    print("Paths:", rooms[player_room])
    print("----------------------------\\n")

def battle(enemy):
    global health
    slow_print(f"A wild {enemy} appears!")
    while True:
        action = input("Fight or Run? ").lower()
        if action == "fight":
            if "Laser Gun" in inventory:
                slow_print("You blast the enemy!")
                return True
            else:
                dmg = random.randint(10, 30)
                health -= dmg
                slow_print(f"You punch it! You lose {dmg} HP.")
                if health <= 0:
                    slow_print("You died! Game Over.")
                    exit()
                if random.random() < 0.3:
                    slow_print("You managed to defeat it!")
                    return True
        elif action == "run":
            slow_print("You escaped safely!")
            return False

def collect_item():
    if player_room in items:
        item = items[player_room]
        slow_print(f"You found a {item}!")
        inventory.append(item)
        del items[player_room]

# Game intro
slow_print("Welcome to the Space Adventure!")
slow_print("Retrieve the alien egg from the Alien Nest and survive!\\n")

# Main game loop
while True:
    show_status()

    if player_room == "Alien Nest":
        if "Laser Gun" not in inventory:
            slow_print("You entered the Alien Nest unarmed...")
        if battle("Alien Queen"):
            slow_print("You collected the Alien Egg! YOU WIN!")
            break

    if player_room in enemies:
        battle(enemies[player_room])

    collect_item()

    move = input("Where do you want to go? ").strip()
    if move in rooms[player_room]:
        player_room = move
    else:
        slow_print("You can't go there!")

slow_print("Thanks for playing!")
"""

print(f"Analyzing code length: {len(code)}")

try:
    cv = radon_visitors.ComplexityVisitor.from_code(code)
    print("Function Complexities:")
    for f in cv.functions:
        print(f"  {f.name}: {f.complexity}")
    
    total_complexity = sum([f.complexity for f in cv.functions]) + cv.complexity
    print(f"\nTotal File Complexity (sum + top-level): {total_complexity}")

    print(f"Is > 10? {total_complexity > 10}")

except Exception as e:
    print(f"Error: {e}")

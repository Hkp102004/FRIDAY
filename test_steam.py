from skills.steam import _game_library, _find_game

print("All games:")
for name in sorted(_game_library.keys()):
    print(f"  {name}")

print("\nSearching for 'spider':")
name, gid = _find_game("spider")
print(f"  Found: {name} ({gid})")


print("\nSearching for 'spider-man remastered':")
name, gid = _find_game("spider-man remastered")
print(f"  Found: {name} ({gid})")

print("\nSearching for 'marvel spider man remastered':")
name, gid = _find_game("marvel spider man remastered")
print(f"  Found: {name} ({gid})")

print("\nSearching for 'spider man 2':")
name, gid = _find_game("spider man 2")
print(f"  Found: {name} ({gid})")
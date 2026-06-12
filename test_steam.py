from skills.steam import _game_library, _find_game

print("All games:")
for name in sorted(_game_library.keys()):
    print(f"  {name}")

print("\nDEBUG scoring for 'spider-man remastered':")
query = "spider-man remastered"
query_words = query.split()
print(f"Query words: {query_words}")
for name, gid in _game_library.items():
    score = sum(1 for word in query_words if word in name)
    print(f"  '{name}' → score: {score}")
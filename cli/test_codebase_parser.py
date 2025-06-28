from scripts.codebase_parser import parse_codebase

root_path = "E:/Git/Self/BlinkMart-Server"

results = parse_codebase(root_path)

for file, data in results.items():
    print(f"\nFile: {file}")
    print(f"Language: {data['language']}")
    for feature, items in data['features'].items():
        # print(f"  {feature}: {len(items)} items")
        print(f"  {feature}: {items}")

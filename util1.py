import json

def extract_coordinates(input_path: str, output_path: str):
    # Load the original JSON
    with open(input_path, 'r', encoding='utf-8') as f:
        scenes = json.load(f)
    
    # Build the new list
    coords_list = []
    for key, info in scenes.items():
        title = str(info.get("scene_name")) + " " + str(info.get("title"))
        coor_str = info.get("coor", "")
        try:
            lat_str, lon_str = coor_str.split(",")
            latitude = float(lat_str.strip())
            longitude = float(lon_str.strip())
        except ValueError:
            # Skip entries with malformed or missing coor
            print(f"Warning: skipping '{key}' with invalid coor: {coor_str!r}")
            continue
        
        coords_list.append({
            "title": title,
            "latitude": latitude,
            "longitude": longitude
        })
    
    # Write out the new JSON array
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(coords_list, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(coords_list)} coordinate entries to {output_path!r}")

if __name__ == "__main__":
    # Replace these with your actual filenames
    extract_coordinates("scenes.json", "coords_only.json")

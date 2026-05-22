import os
import re

scratch_dir = r"d:\Materials\Skills\Github\ITI-Notes\scratch"
group_files = [f"group_{c}.html" for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g']]

for g_file in group_files:
    path = os.path.join(scratch_dir, g_file)
    print(f"\n--- FILE: {g_file} ---")
    if not os.path.exists(path):
        print("Does not exist!")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex to find section open tags with ids and their h2 titles
    sections = re.findall(r'<section\s+id="([^"]+)"[^>]*>.*?<h2[^>]*>(.*?)</h2>', content, re.DOTALL)
    for idx, (sid, h2) in enumerate(sections):
        h2_clean = re.sub(r'<[^>]+>', '', h2).strip()
        print(f"Section {idx+1}: ID='{sid}', Title='{h2_clean}'")

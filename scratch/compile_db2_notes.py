import os
import re
import sys

# Define absolute paths
workspace_dir = r"d:\Materials\Skills\Github\ITI-Notes"
notes_file = os.path.join(workspace_dir, "Notes", "db2-notes.html")
scratch_dir = os.path.join(workspace_dir, "scratch")

def extract_section_by_id(content, section_id):
    # Find the start tag: <section id="section_id" ...>
    pattern = rf'<section\s+[^>]*id="{section_id}"[^>]*>'
    match = re.search(pattern, content)
    if not match:
        return None
    start_pos = match.start()
    
    # Trace nested tags to find matching </section>
    pos = match.end()
    nested_count = 1
    while nested_count > 0 and pos < len(content):
        next_open = content.find('<section', pos)
        next_close = content.find('</section>', pos)
        
        if next_close == -1:
            break
            
        if next_open != -1 and next_open < next_close:
            nested_count += 1
            pos = next_open + len('<section')
        else:
            nested_count -= 1
            pos = next_close + len('</section>')
            
    if nested_count == 0:
        return content[start_pos:pos]
    else:
        # Fallback
        close_pos = content.find('</section>', match.end())
        if close_pos != -1:
            return content[start_pos:close_pos + len('</section>')]
        return None

def compile_notes():
    print("Reading target notes file...")
    with open(notes_file, 'r', encoding='utf-8') as f:
        notes_content = f.read()

    # Define groups and their sections
    groups = {
        'group_a.html': ['topic14', 'topic15', 'topic16', 'topic17', 'topic18'],
        'group_b.html': ['topic19', 'topic20', 'topic21', 'topic22', 'topic23'],
        'group_c.html': ['topic24', 'topic25', 'topic26', 'topic27'],
        'group_d.html': ['topic28', 'topic29', 'topic30', 'topic31'],
        'group_e.html': ['group-e-overview', 'topic-32', 'topic-33', 'topic-34', 'topic-35', 'topic-36'],
        'group_f.html': ['introduction', 'topic37', 'topic38', 'topic39', 'topic40', 'topic41', 'topic42'],
        'group_g.html': ['introduction', 'topic43', 'topic44', 'topic45', 'topic46', 'topic47', 'topic48'],
    }

    compiled_blocks = []

    for g_file, section_ids in groups.items():
        g_path = os.path.join(scratch_dir, g_file)
        print(f"\nProcessing {g_file}...")
        if not os.path.exists(g_path):
            print(f"ERROR: {g_file} not found!")
            sys.exit(1)
            
        with open(g_path, 'r', encoding='utf-8') as f:
            g_content = f.read()

        for sid in section_ids:
            sec_html = extract_section_by_id(g_content, sid)
            if not sec_html:
                print(f"ERROR: Section with ID '{sid}' not found in {g_file}!")
                sys.exit(1)
                
            # Perform adjustments based on file and ID rules
            if g_file == 'group_e.html':
                # Normalize dashed IDs to solid IDs in Group E
                # Replace id="topic-32" with id="topic32", href="#topic-32" with href="#topic32", etc.
                sec_html = re.sub(r'id="topic-(\d+)"', r'id="topic\1"', sec_html)
                sec_html = re.sub(r'href="#topic-(\d+)"', r'href="#topic\1"', sec_html)
                # Keep group-e-overview as is
                print(f"  Extracted and normalized section: {sid}")
            elif g_file == 'group_f.html' and sid == 'introduction':
                # Rename introduction in Group F to lifecycle-intro
                sec_html = sec_html.replace('id="introduction"', 'id="lifecycle-intro"')
                # Also fix the inner header icon class to be stylish
                print(f"  Extracted introduction -> lifecycle-intro")
            elif g_file == 'group_g.html' and sid == 'introduction':
                # Rename introduction in Group G to advanced-topics-intro
                sec_html = sec_html.replace('id="introduction"', 'id="advanced-topics-intro"')
                print(f"  Extracted introduction -> advanced-topics-intro")
            else:
                print(f"  Extracted section: {sid}")
                
            compiled_blocks.append(sec_html)

    # Combine blocks with comments
    combined_content_to_inject = "\n\n          ".join(compiled_blocks)

    # 1. Inject content at split point
    split_marker = "<!-- Section 6: Best Practices & Performance Tips -->"
    if split_marker not in notes_content:
        print(f"ERROR: Split marker '{split_marker}' not found in target notes file!")
        sys.exit(1)

    parts = notes_content.split(split_marker)
    first_part = parts[0]
    second_part = parts[1]

    # Combine first part + injected blocks + split marker + second part
    # We want to insert a separator comment before the new sections
    separator_comment = "\n          <!-- ============================================ -->\n          <!-- ADDITIONAL ITI STUDY NOTE TOPICS (14 TO 48)   -->\n          <!-- ============================================ -->\n          "
    notes_content_new = first_part + separator_comment + combined_content_to_inject + "\n\n          " + split_marker + second_part

    # 2. Generate and update sidebar navigation
    print("\nUpdating sidebar navigation...")
    
    old_sidebar_pattern = r'<li>\s*<a href="#db2-joins"><i class="fas fa-link"></i> Types of JOINS in DB2</a>.*?</li>'
    # Let's search exactly what is in lines 59 to 68 of db2-notes.html
    # We can match from `<a href="#db2-joins">` to the closing `</li>` corresponding to it.
    
    new_sidebar_html = """<li>
            <a href="#db2-joins"><i class="fas fa-link"></i> Types of JOINS in DB2</a>
            <ul>
              <li><a href="#join-concepts">Logical vs. Physical Joins</a></li>
              <li><a href="#join-syntax">Join Command Syntax</a></li>
              <li><a href="#join-lab">DBA Join Lab</a></li>
              <li><a href="#join-tuning">Join Heuristics &amp; Indexing</a></li>
              <li><a href="#join-summary">Join Summary Table</a></li>
            </ul>
          </li>
          <li>
            <a href="#topic14"><i class="fas fa-server"></i> Maintaining DB2 Data &amp; Server Admin (Topics 14-18)</a>
            <ul>
              <li><a href="#topic14">Topic 14: Storage Architecture</a></li>
              <li><a href="#topic15">Topic 15: Transaction Logging</a></li>
              <li><a href="#topic16">Topic 16: Lifecycle Management</a></li>
              <li><a href="#topic17">Topic 17: DML &amp; Transactions</a></li>
              <li><a href="#topic18">Topic 18: Concurrency &amp; Escalation</a></li>
            </ul>
          </li>
          <li>
            <a href="#topic19"><i class="fas fa-shield-alt"></i> Objects &amp; Database Security (Topics 19-23)</a>
            <ul>
              <li><a href="#topic19">Topic 19: Database Objects</a></li>
              <li><a href="#topic20">Topic 20: Connection Security &amp; Auth</a></li>
              <li><a href="#topic21">Topic 21: SECADM vs. DBADM</a></li>
              <li><a href="#topic22">Topic 22: Privileges &amp; RBAC</a></li>
              <li><a href="#topic23">Topic 23: Auditing &amp; Intro to RCAC</a></li>
            </ul>
          </li>
          <li>
            <a href="#topic24"><i class="fas fa-history"></i> Backup &amp; Recovery Operations (Topics 24-27)</a>
            <ul>
              <li><a href="#topic24">Topic 24: Backup &amp; Recovery Intro</a></li>
              <li><a href="#topic25">Topic 25: Transactional Logging</a></li>
              <li><a href="#topic26">Topic 26: Restore &amp; Reconstruction</a></li>
              <li><a href="#topic27">Topic 27: Rollforward &amp; PITR</a></li>
            </ul>
          </li>
          <li>
            <a href="#topic28"><i class="fas fa-lock"></i> Concurrency &amp; Locking Admin (Topics 28-31)</a>
            <ul>
              <li><a href="#topic28">Topic 28: Concurrency &amp; Isolation</a></li>
              <li><a href="#topic29">Topic 29: Locking &amp; Advanced Modes</a></li>
              <li><a href="#topic30">Topic 30: Lock Admin &amp; Tuning</a></li>
              <li><a href="#topic31">Topic 31: Locking Diagnostics</a></li>
            </ul>
          </li>
          <li>
            <a href="#group-e-overview"><i class="fas fa-rocket"></i> High-Performance Utilities &amp; HADR (Topics 32-36)</a>
            <ul>
              <li><a href="#group-e-overview">Group E Overview</a></li>
              <li><a href="#topic32">Topic 32: EXPORT &amp; IMPORT</a></li>
              <li><a href="#topic33">Topic 33: LOAD Utility</a></li>
              <li><a href="#topic34">Topic 34: Fundamentals Exam Review</a></li>
              <li><a href="#topic35">Topic 35: HADR Sync Modes</a></li>
              <li><a href="#topic36">Topic 36: HADR Implementation</a></li>
            </ul>
          </li>
          <li>
            <a href="#lifecycle-intro"><i class="fas fa-redo"></i> Enterprise Upgrade Roadmap (Topics 37-42)</a>
            <ul>
              <li><a href="#lifecycle-intro">Group F Overview</a></li>
              <li><a href="#topic37">Topic 37: Upgrade Roadmap</a></li>
              <li><a href="#topic38">Topic 38: OS Prep &amp; Server Tuning</a></li>
              <li><a href="#topic39">Topic 39: Silent Install &amp; Response File</a></li>
              <li><a href="#topic40">Topic 40: db2ckupgrade Utility</a></li>
              <li><a href="#topic41">Topic 41: db2iupgrade Utility</a></li>
              <li><a href="#topic42">Topic 42: db2updv115 Utility</a></li>
            </ul>
          </li>
          <li>
            <a href="#advanced-topics-intro"><i class="fas fa-gem"></i> Advanced Administration Topics (Topics 43-48)</a>
            <ul>
              <li><a href="#advanced-topics-intro">Group G Overview</a></li>
              <li><a href="#topic43">Topic 43: GUI Tools &amp; Interfaces</a></li>
              <li><a href="#topic44">Topic 44: Deep Table Compression</a></li>
              <li><a href="#topic45">Topic 45: Row &amp; Column Security (RCAC)</a></li>
              <li><a href="#topic46">Topic 46: Storage Groups</a></li>
              <li><a href="#topic47">Topic 47: Temporal Tables</a></li>
              <li><a href="#topic48">Topic 48: Columnar Storage &amp; BLU</a></li>
            </ul>
          </li>"""

    # We find the exact block from `<a href="#db2-joins">` to its parent `<li>` wrapper and replace it
    # The parent li wrapper starts with `<li>\s*<a href="#db2-joins">` and ends after the corresponding closed ul and li.
    # Let's inspect the target file lines:
    # 59:           <li>
    # 60:             <a href="#db2-joins"><i class="fas fa-link"></i> Types of JOINS in DB2</a>
    # ...
    # 68:           </li>
    
    target_pattern = r'<li>\s*<a href="#db2-joins">.*?</a>\s*<ul>.*?</ul>\s*</li>'
    
    # We replace with our new sidebar items
    notes_content_new, count = re.subn(target_pattern, new_sidebar_html, notes_content_new, flags=re.DOTALL)
    
    if count == 0:
        print("ERROR: Failed to replace sidebar block using regex!")
        # Let's try matching a wider or more generic block if the previous regex failed
        sys.exit(1)
    else:
        print(f"Sidebar updated successfully (replaced {count} block).")

    print(f"Writing updated content to {notes_file}...")
    with open(notes_file, 'w', encoding='utf-8') as f:
        f.write(notes_content_new)

    print("SUCCESS: Notes compiled and merged successfully!")

if __name__ == '__main__':
    compile_notes()

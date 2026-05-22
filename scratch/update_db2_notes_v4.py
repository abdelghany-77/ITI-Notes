import re

file_path = r'd:\Materials\Skills\Github\ITI-Notes\Notes\db2-notes.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update sidebar
old_nav_pattern = re.compile(
    r'(<!-- Follow-up topics will be injected here in later batches -->)',
    re.DOTALL
)
new_nav = """<li><a href="#topic16">Topic 16: Instances</a></li>
              <li><a href="#topic17">Topic 17: Databases</a></li>
              <li><a href="#topic18">Topic 18: Storage</a></li>
              <!-- Follow-up topics will be injected here in later batches -->"""
content = old_nav_pattern.sub(new_nav, content)


old_content_pattern = re.compile(
    r'(</section>\s*\n\s*<!-- Section 6: Best Practices & Performance Tips -->)',
    re.DOTALL
)

topic_16_17_18 = """
          </section>

          <section id="topic16" class="section">
            <h2 class="section-title"><i class="fas fa-server"></i> Topic 16: DB2 Server - Administering and Working with Instances</h2>
            <div class="subsection" id="t16-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                In DB2, the <strong>Instance</strong> is the heartbeat of the database engine—a dedicated memory environment and background process block on the host OS. A single physical server can host multiple, discrete DB2 instances (each mapping to a unique system user, like <code>db2inst1</code>, <code>db2inst2</code>). This provides absolute logical, memory, and security isolation. The <code>db2sysc</code> core process and its Engine Dispatchable Units (EDUs) operate at the Instance level.
              </p>
            </div>
            
            <div class="subsection" id="t16-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">Instance Administration Shell Commands</div>
                <pre><code><span class="comment"># Create a new local instance (executed as root/sudo) using a fenced user</span>
/opt/ibm/db2/V11.5/instance/db2icrt -u db2fenc2 db2inst2

<span class="comment"># Update Instance level configuration (DBM CFG) - requires instance restart</span>
db2 "UPDATE DBM CFG USING SVCENAME 50000"
db2 "UPDATE DBM CFG USING MAX_CONNECTIONS 1500"

<span class="comment"># List all active instances on the server</span>
db2ilist

<span class="comment"># Drop an instance (must be stopped first)</span>
/opt/ibm/db2/V11.5/instance/db2idrop db2inst2</code></pre>
              </div>
            </div>

            <div class="subsection" id="t16-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: The Multi-Tenant Server</h3>
              <p><strong>Scenario:</strong> You must host both the European HR system and the North American Warehouse on a single huge Linux box. Because European GDPR laws dictate complete segregation, you build a multi-instance topology.</p>
              <div class="code-example">
                <div class="code-language">Lab Execution</div>
                <pre><code><span class="comment"># 1. As root, provision the OS accounts required for European DB</span>
useradd -m -g db2iadm euinst1
useradd -m -g db2fadm eufenc1

<span class="comment"># 2. Spawn the isolated DB2 Engine</span>
/opt/ibm/db2/V11.5/instance/db2icrt -u eufenc1 euinst1

<span class="comment"># 3. Log in to the new engine space</span>
su - euinst1
db2start

<span class="comment"># 4. Modify memory so it does not cannibalize the North American DB instance</span>
db2 "UPDATE DBM CFG USING INSTANCE_MEMORY 500000" <span class="comment"># Bound explicitly</span></code></pre>
              </div>
            </div>

            <div class="subsection" id="t16-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="disadvantages-box font-code">
                <h4><i class="fas fa-bug"></i> Error SQL1032N</h4>
                <p><strong>Error Message:</strong> No start database manager command was issued.</p>
                <p><strong>Cause:</strong> Attempting to run a <code>db2 create database</code> or <code>update dbm cfg</code> without starting the engine via <code>db2start</code>.</p>
              </div>
            </div>
            
            <div class="subsection" id="t16-summary">
              <h3 class="subsection-title">5. Summary Table</h3>
              <table class="table">
                <thead><tr><th>Command</th><th>Purpose</th><th>OS Level vs CLP Level</th></tr></thead>
                <tbody>
                  <tr><td><code>db2icrt</code></td><td>Provision a new DB2 Instance environment</td><td>Root OS Level (Shell)</td></tr>
                  <tr><td><code>db2start</code> / <code>db2stop</code></td><td>Wake / Shutdown the background DBM processes</td><td>Instance Owner Level (CLP)</td></tr>
                  <tr><td><code>UPDATE DBM CFG</code></td><td>Modify universal constraints across all attached databases</td><td>Instance Owner Level (CLP)</td></tr>
                </tbody>
              </table>
            </div>
          </section>

          <section id="topic17" class="section">
            <h2 class="section-title"><i class="fas fa-database"></i> Topic 17: DB2 Server - Administering and Working with Databases</h2>
            <div class="subsection" id="t17-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                A DB2 <strong>Database</strong> is a relational containment boundary housing its own table data, local catalog dictionaries, and transaction logs. When you connect to a database and allocate it (via <code>ACTIVATE DB</code>), DB2 allocates a massive chunk of RAM called the <strong>Database Global Memory</strong>. This holds the Buffer Pools, Lock List, and Log Buffers. It isolates workloads perfectly: dropping one database does not compromise the tablespaces of another database in the same instance.
              </p>
            </div>
            
            <div class="subsection" id="t17-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">Database Lifecycle Commands</div>
                <pre><code><span class="comment">-- Create a database setting it to use high-capacity 32KB pages</span>
CREATE DATABASE ANALYTIC ON '/dbdata/data' DBPATH ON '/dbdata/ctrl' PAGESIZE 32768;

<span class="comment">-- ACTIVATE the database memory structure explicitly without connecting clients</span>
ACTIVATE DATABASE ANALYTIC;

<span class="comment">-- DEACTIVATE local memory when finished to save system resources</span>
DEACTIVATE DATABASE ANALYTIC;

<span class="comment">-- Terminate all active sessions connected to the database</span>
FORCE APPLICATION ALL;

<span class="comment">-- Drop the entire physical database</span>
DROP DATABASE ANALYTIC;</code></pre>
              </div>
            </div>

            <div class="subsection" id="t17-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: The Maintenance Window</h3>
              <p><strong>Scenario:</strong> You must perform extreme high-velocity structural changes on the <code>PAYROLL</code> database over the weekend without client applications blocking your locks.</p>
              <div class="code-example">
                <div class="code-language">Offline DBA Operations</div>
                <pre><code><span class="comment"># 1. Sever all ongoing application connections forcefully</span>
db2 "FORCE APPLICATION ALL"

<span class="comment"># 2. Deactivate the memory to cleanly flush the dirty pages</span>
db2 "DEACTIVATE DATABASE PAYROLL"

<span class="comment"># 3. Enter restricted access mode so web servers cannot reconnect</span>
db2 "QUIESCE DATABASE PAYROLL IMMEDIATE"

<span class="comment"># 4. Connect locally, perform the massive alter table jobs</span>
db2 "CONNECT TO PAYROLL"
db2 -tvf massive_upgrade_script.sql

<span class="comment"># 5. Lift the quarantine and restore public access</span>
db2 "UNQUIESCE DATABASE PAYROLL"</code></pre>
              </div>
            </div>

            <div class="subsection" id="t17-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="advantages-box font-code">
                <h4><i class="fas fa-check-circle"></i> Best Practices for First Connects</h4>
                <p>Always issue an <code>ACTIVATE DB</code> during server startup routines. If you rely on the first user connection to auto-activate the database, that first user suffers an enormous timeout penalty as DB2 allocates memory, parses catalogs, and provisions buffers.</p>
              </div>
            </div>
          </section>

          <section id="topic18" class="section">
            <h2 class="section-title"><i class="fas fa-microchip"></i> Topic 18: DB2 Server - Managing Database Storage</h2>
            <div class="subsection" id="t18-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>DB2 manages physical disk space via <strong>Storage Groups</strong> and <strong>Tablespaces</strong>. Modern DB2 exclusively relies on <em>Automatic Storage</em>, where DBAs designate mount points (`/db2/data1`, `/db2/data2`), and DB2 dynamically stripes container files uniformly across these mounts, preventing hot-spotting on a single physical disk array. Storage management involves extending disks, adding new paths to storage groups, and rebalancing data across the new arrays.</p>
            </div>
            
            <div class="subsection" id="t18-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">DB2 CLP - Storage Commands</div>
                <pre><code><span class="comment">-- View available automatic storage paths for a database</span>
db2 "SELECT * FROM SYSIBMADM.SNAPSTORAGE_PATHS"

<span class="comment">-- Expand the database onto a new SAN LUN Mount target</span>
ALTER DATABASE WORKDB ADD STORAGE ON '/san/lun03'

<span class="comment">-- Re-stripe and balance existing data to utilize the new mount</span>
ALTER TABLESPACE USERSPACE1 REBALANCE;

<span class="comment">-- Recapture freed OS disk space after dropping millions of rows</span>
ALTER TABLESPACE USERSPACE1 REDUCE MAX;</code></pre>
              </div>
            </div>
"""

content = old_content_pattern.sub(topic_16_17_18 + r'\1', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS BATCH 2")
import re

file_path = r'd:\Materials\Skills\Github\ITI-Notes\Notes\db2-notes.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update sidebar
old_nav_pattern = re.compile(
    r'(<!-- Follow-up topics will be injected here in later batches -->)',
    re.DOTALL
)
new_nav = """<li><a href="#topic32">Topic 32: Data Movement (EXPORT/IMPORT/LOAD)</a></li>
              <li><a href="#topic33">Topic 33: Certification Prep Fundamentals</a></li>
              <li><a href="#topic34">Topic 34: DB2 Case Studies</a></li>
              <li><a href="#topic35">Topic 35: Learning Resources</a></li>
              <li><a href="#topic36">Topic 36: Bonus - HADR</a></li>
              <!-- Follow-up topics will be injected here in later batches -->"""
content = old_nav_pattern.sub(new_nav, content)


old_content_pattern = re.compile(
    r'(</section>\s*\n\s*<!-- Section 6: Best Practices & Performance Tips -->)',
    re.DOTALL
)

topic_32_to_36_chunk = """
          </section>

          <section id="topic32" class="section">
            <h2 class="section-title"><i class="fas fa-truck-loading"></i> Topic 32: Data Movement Utilities (EXPORT, IMPORT, LOAD)</h2>
            <div class="subsection" id="t32-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                As a DBA, moving massive amounts of data is a daily task. DB2 provides three distinct utilities. <strong>EXPORT</strong> extracts data from a table into a flat file (DEL, IXF). To push data back in, you choose between <strong>IMPORT</strong> or <strong>LOAD</strong>. 
                <br><br>
                <em>IMPORT</em> is a standard SQL application. It performs standard <code>INSERT</code> statements, writes to the transaction logs, fires triggers, and respects constraint validations. It is safe but extremely slow for massive volumes. 
                <br>
                <em>LOAD</em> is a physical database engine utility. It bypasses the SQL engine entirely, formatting data blocks in memory and writing them directly to the tablespace pages physically on disk. It is incredibly fast, but skips triggers and often leaves the table in a "Backup Pending" state because it bypasses the transaction log.
              </p>
            </div>
            
            <div class="subsection" id="t32-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">DB2 Data Movement Utilities</div>
                <pre><code><span class="comment">-- EXPORT: Dump a massive table into a comma-delimited (DEL) file</span>
db2 "EXPORT TO employees.del OF DEL SELECT * FROM HR.EMPLOYEES"

<span class="comment">-- IMPORT: Carefully ingest the data (Fires constraints and writes to active log)</span>
db2 "IMPORT FROM employees.del OF DEL INSERT_UPDATE INTO HR.EMPLOYEES"

<span class="comment">-- LOAD: Force physical ingestion (10x faster). Warning: Bypasses logs!</span>
db2 "LOAD FROM employees.del OF DEL REPLACE INTO HR.EMPLOYEES NONRECOVERABLE"</code></pre>
              </div>
            </div>

            <div class="subsection" id="t32-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: The "Log Full" Migration</h3>
              <p><strong>Scenario:</strong> You are tasked with migrating 50 million records from an old archive table. Using <code>IMPORT</code> crashes the system mid-way with SQL0964C (Transaction Log Full).</p>
              <div class="code-example">
                <div class="code-language">LOAD Utility Migration</div>
                <pre><code><span class="comment"># 1. Use LOAD to totally bypass the SQL engine and transaction logs.</span>
<span class="comment"># 'COPY NO' puts the table in Backup Pending State after the load finishes to protect you.</span>
db2 "LOAD FROM archive.del OF DEL INSERT INTO FIN.ARCHIVE COPY NO"

<span class="comment"># 2. Extract the table from Backup Pending so users can query it</span>
db2 "BACKUP DATABASE PRODDB TABLESPACE (ARCHIVE_TBS) ONLINE"

<span class="comment"># 3. Inform the Query Optimizer about the 50 million new physical rows</span>
db2 "RUNSTATS ON TABLE FIN.ARCHIVE AND INDEXES ALL"</code></pre>
              </div>
            </div>

            <div class="subsection" id="t32-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="disadvantages-box font-code">
                <h4><i class="fas fa-bug"></i> Error SQL0668N Reason Code 3</h4>
                <p><strong>Error Message:</strong> Operation not allowed for reason code "3" on table.</p>
                <p><strong>Cause:</strong> The table is stuck in <code>LOAD PENDING</code> state. This happens if a LOAD crashes halfway through due to a power outage or bad data file.</p>
                <p><strong>Fix:</strong> You must explicitly tell the engine to kill the corrupted load attempt: <br>
                <code>db2 "LOAD FROM /dev/null OF DEL TERMINATE INTO FIN.ARCHIVE"</code></p>
              </div>
            </div>

            <div class="subsection" id="t32-summary">
              <h3 class="subsection-title">5. Summary Table</h3>
              <table class="table">
                <thead><tr><th>Feature</th><th>IMPORT</th><th>LOAD</th></tr></thead>
                <tbody>
                  <tr><td><strong>Engine Path</strong></td><td>SQL Statements (Inserts)</td><td>Direct Physical Page Formatting</td></tr>
                  <tr><td><strong>Logging</strong></td><td>Fully logged in Transaction Logs</td><td>Minimal (or NONE if NONRECOVERABLE)</td></tr>
                  <tr><td><strong>Triggers Fired?</strong></td><td>Yes</td><td>No (Bypassed)</td></tr>
                  <tr><td><strong>Speed</strong></td><td>Slow (Bottlenecks on Logs)</td><td>Extremely Fast (I/O Maxed)</td></tr>
                </tbody>
              </table>
            </div>
          </section>

          <section id="topic33" class="section">
            <h2 class="section-title"><i class="fas fa-graduation-cap"></i> Topic 33: DB2 Family Fundamentals - Preparing for Certification</h2>
            <div class="subsection" id="t33-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                The IBM DB2 Fundamentals Certification validates universal knowledge across the DB2 Family (LUW, z/OS, iSeries). The exam doesn't just ask about SQL syntax; it demands deep comprehension of DB2's isolated architecture. You must intrinsically understand how the Query Compiler processes data, the difference between DDL and DML, DB2's hierarchical security model, and how Isolation Levels dynamically affect locking mechanisms.
              </p>
            </div>
            
            <div class="subsection" id="t33-summary">
              <h3 class="subsection-title">5. Summary Table: Exam Focus Areas</h3>
              <table class="table">
                <thead><tr><th>Exam Domain</th><th>Core Concepts to Memorize</th></tr></thead>
                <tbody>
                  <tr><td><strong>Planning & Architecture</strong></td><td>Instances vs Databases, Catalog definitions (SYSIBM), Client-server connection mechanisms.</td></tr>
                  <tr><td><strong>Data Concurrency</strong></td><td>Memorize the 4 Isolation Levels (UR, CS, RS, RR) and the 3 phenomena they block.</td></tr>
                  <tr><td><strong>Security</strong></td><td>Know exactly who grants DBADM, exactly what SECADM does, and OS-dependent Authentication.</td></tr>
                </tbody>
              </table>
            </div>
          </section>

          <section id="topic34" class="section">
            <h2 class="section-title"><i class="fas fa-briefcase"></i> Topic 34: DB2 Case Studies</h2>
            <div class="subsection" id="t34-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                Theory must translate to architectural decisions. In a high-stakes DB2 enterprise environment, multiple subsystems (Locking, Logging, Disk I/O, OS Security) interact simultaneously. A failure in one subsystem often cascades. True DBA mastery involves recognizing the ripple effects across the architecture.
              </p>
            </div>

            <div class="subsection" id="t34-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: The E-Commerce Black Friday Crash</h3>
              <p><strong>Scenario:</strong> It is Black Friday. Traffic spikes 500%. Suddenly, the entire web platform stalls. Transactions are timing out. The active logs fill up. Disk I/O is at 100%.</p>
              <div class="code-example">
                <div class="code-language">The Cascade Analysis</div>
                <pre><code><span class="comment"># Step 1: Check Lock Manager - Finding massive table locks</span>
db2 "SELECT * FROM SYSIBMADM.LOCKWAITS" 
<span class="comment">-- Finding: Lock Escalation occurred! 1000 users are waiting on 1 mass lock.</span>

<span class="comment"># Step 2: Identify the root cause of escalation in the Application</span>
db2 "SELECT STMT_TEXT ... FROM SYSIBMADM.SNAPSTMT"
<span class="comment">-- Finding: A marketing module issued "UPDATE Inventory SET Price = Price * 0.5" (No WHERE Clause)</span>

<span class="comment"># Step 3: Why did logs fill? </span>
<span class="comment">-- That singular UPDATE modified 10 million rows in ONE transaction block,</span>
<span class="comment">-- saturating the Active Transaction Log before a COMMIT could be issued.</span>

<span class="comment"># FIX: Force the marketing application. Increase MAXLOCKS dynamically. </span>
<span class="comment"># Force the devs to batch updates in 100,000 row chunks with COMMITs.</span></code></pre>
              </div>
            </div>
          </section>

          <section id="topic35" class="section">
            <h2 class="section-title"><i class="fas fa-book-open"></i> Topic 35: Learning Resources for DB2</h2>
            <div class="subsection" id="t35-concept">
              <p>
                Mastering IBM DB2 requires utilizing IBM's immense library of technical resources. 
                <ul>
                  <li><strong>IBM Knowledge Center:</strong> The gold standard for explicit CLP syntax, system catalog definitions, and exact error code explanations.</li>
                  <li><strong>IBM Redbooks:</strong> Deep, architectural whitepapers that explain "Why" and "How" large-scale implementations operate (e.g., HADR setups, DPF clustering).</li>
                  <li><strong>developerWorks:</strong> Practical forums and step-by-step DBA guides.</li>
                </ul>
              </p>
            </div>
          </section>

          <section id="topic36" class="section">
            <h2 class="section-title"><i class="fas fa-network-wired"></i> Topic 36: Bonus - High Availability and Disaster Recovery (HADR)</h2>
            <div class="subsection" id="t36-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                <strong>DB2 HADR</strong> is a database replication feature providing a high-availability solution. DB2 essentially utilizes "Log Shipping" at the engine level. 
                <br><br>
                You configure a <em>Primary</em> database and a <em>Standby</em> database on separate Linux servers. Whenever a user executes a transaction on the Primary, DB2 writes to the local transaction log as usual, but simultaneously transmits that log buffer over a TCP/IP connection to the Standby server. The Standby server receives the log buffer and independently runs a continuous <code>ROLLFORWARD</code>, replaying the data natively. If the Primary data center burns down, you issue a <code>TAKEOVER</code> command on the Standby, making it the new Primary within seconds.
              </p>
            </div>
            
            <div class="subsection" id="t36-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">HADR Implementation</div>
                <pre><code><span class="comment">-- On the Standby Server (Start it FIRST to receive logs)</span>
db2 "START HADR ON DATABASE PRODDB AS STANDBY"

<span class="comment">-- On the Primary Server (Start it SECOND to send logs)</span>
db2 "START HADR ON DATABASE PRODDB AS PRIMARY"

<span class="comment">-- Check the real-time replication status, looking for state 'PEER'</span>
db2pd -db PRODDB -hadr

<span class="comment">-- Administrative Failover (Taking the Standby and making it Primary during a disaster)</span>
db2 "TAKEOVER HADR ON DATABASE PRODDB"</code></pre>
              </div>
            </div>

            <div class="subsection" id="t36-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: The Automatic Failover</h3>
              <p><strong>Scenario:</strong> You want the failover to be fully automatic if the primary node loses power. You don't want to wake up at 3 AM to type the TAKEOVER command.</p>
              <div class="definition-box">
                <h4><i class="fas fa-eye"></i> IBM Tivoli System Automation (TSA)</h4>
                <p>DBAs integrate DB2 HADR with <strong>TSAMP (Tivoli SA MP)</strong>. TSA is a robotic cluster manager installed at the OS level. It sends physical "heartbeat" pings between the two Linux servers over the network. If the Primary server drops dead, TSA automatically detects the dropped heartbeat, executes the DB2 <code>TAKEOVER</code> command on the standby node, and remaps the network Virtual IP (VIP) to the new server before any users even realize there was an outage.</p>
              </div>
            </div>

            <div class="subsection" id="t36-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="disadvantages-box font-code">
                <h4><i class="fas fa-bug"></i> The Split-Brain Scenario</h4>
                <p><strong>Issue:</strong> The network cable connecting the Primary and Standby fails, but both servers remain online. TSA thinks the Primary died and promotes the Standby. Now you have TWO Primary databases accepting web transactions simultaneously. Data is permanently disjointed.</p>
                <p><strong>Fix:</strong> Network Tiebreakers. Always integrate a completely independent third server (or pingable router disk) into the TSA quorum. In a network partition, the DB2 server that can successfully ping the Tiebreaker is crowned the true Primary. The other isolated server forcefully shuts itself down.</p>
              </div>
            </div>
"""

content = old_content_pattern.sub(topic_32_to_36_chunk + r'\1', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS BATCH 6")
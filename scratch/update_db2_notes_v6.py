import re

file_path = r'd:\Materials\Skills\Github\ITI-Notes\Notes\db2-notes.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update sidebar
old_nav_pattern = re.compile(
    r'(<!-- Follow-up topics will be injected here in later batches -->)',
    re.DOTALL
)
new_nav = """<li><a href="#topic24">Topic 24: Backup & Recovery Intro</a></li>
              <li><a href="#topic25">Topic 25: Transactional Logging</a></li>
              <li><a href="#topic26">Topic 26: Backup Operations</a></li>
              <li><a href="#topic27">Topic 27: Recovery Operations</a></li>
              <!-- Follow-up topics will be injected here in later batches -->"""
content = old_nav_pattern.sub(new_nav, content)


old_content_pattern = re.compile(
    r'(</section>\s*\n\s*<!-- Section 6: Best Practices & Performance Tips -->)',
    re.DOTALL
)

topic_24_to_27_chunk = """
          </section>

          <section id="topic24" class="section">
            <h2 class="section-title"><i class="fas fa-life-ring"></i> Topic 24: DB2 Backup & Recovery - Introduction</h2>
            <div class="subsection" id="t24-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                In an enterprise DB2 environment, data preservation relies on two conceptual pillars: <strong>Crash Recovery</strong> and <strong>Disaster Recovery</strong>. Crash recovery is automatic: if the server power plug is pulled, DB2 reads the Transaction Logs upon restart and brings the database back to a consistent state (undoing partial transactions, redoing committed ones missed by the disk). Disaster recovery is manual: when a SAN disk melts or data is mistakenly wiped, the DBA must rebuild the database from <strong>Backup Images</strong> and roll forward using archived logs.
              </p>
            </div>

            <div class="subsection" id="t24-syntax">
              <h3 class="subsection-title">2. Full Syntax & Definitions</h3>
              <div class="code-example">
                <div class="code-language">DB2 - Key Concepts</div>
                <pre><code><span class="comment">-- Offline Backup (Cold)</span>
<span class="comment">-- The database is completely disconnected. No users allowed. Consistent image.</span>

<span class="comment">-- Online Backup (Hot)</span>
<span class="comment">-- The database is active and users are performing DML inserts. </span>
<span class="comment">-- Requires Archive Logging to be enabled to catch shifts during the backup process.</span>

<span class="comment">-- Rollforward</span>
<span class="comment">-- Applying subsequent transactions from the log files to a restored backup image </span>
<span class="comment">-- to bring it to a specific point-in-time (PIT).</span></code></pre>
              </div>
            </div>

            <div class="subsection" id="t24-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: The Strategy Map</h3>
              <p><strong>Scenario:</strong> You are drafting the SLA (Service Level Agreement) for the new E-Commerce DB2 environment. You must define RTO and RPO metrics for management before setting up scripts.</p>
              <div class="definition-box">
                <h4><i class="fas fa-eye"></i> RPO vs RTO in DB2 terms</h4>
                <ul>
                  <li><strong>Recovery Point Objective (RPO):</strong> How much data can you lose? We configure LOGARCHMETH1 (Archive Logging) to a separate NFS mount to achieve zero RPO to the last transaction.</li>
                  <li><strong>Recovery Time Objective (RTO):</strong> How long to restore? If 10 hours is unacceptable, DBAs will employ incremental backups or disk-level snapshots.</li>
                </ul>
              </div>
            </div>
          </section>

          <section id="topic25" class="section">
            <h2 class="section-title"><i class="fas fa-list-alt"></i> Topic 25: DB2 Backup and Recovery - Transactional Logging</h2>
            <div class="subsection" id="t25-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                DB2 supports two logging models: <strong>Circular Logging</strong> (default) and <strong>Archive Logging</strong>. In <em>Circular Logging</em>, DB2 continually overrides old log files once transactions commit. This means no online backups, and if the DB crashes you can only restore an old offline backup (losing all work since). In <em>Archive Logging</em>, once a log fills up, DB2 copies it to a safe archive location (Tape, TSM, NFS) before overwriting the active space. Archive Logging enables 24/7 online backups and Point-In-Time (PIT) recovery via a Rollforward.
              </p>
            </div>
            
            <div class="subsection" id="t25-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">Transforming to Archive Logging</div>
                <pre><code><span class="comment"># 1. By default, DB2 Databases are Circular (LOGARCHMETH1 is OFF)</span>
db2 get db cfg for MAINDB | grep -i LOGARCH

<span class="comment"># 2. Update to Archive pointing to a different disk mount</span>
db2 "UPDATE DB CFG FOR MAINDB USING LOGARCHMETH1 DISK:/mnt/nas/db2_archives"

<span class="comment"># 3. Upon updating this parameter, the DB goes into 'Backup Pending' State</span>
<span class="comment"># You must take an offline backup immediately to establish a new base line.</span>
db2 "BACKUP DB MAINDB TO /mnt/nas/backups"</code></pre>
              </div>
            </div>

            <div class="subsection" id="t25-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: Tracking Active Logs</h3>
              <p><strong>Scenario:</strong> You get an alert: Active disk space is at 95%. Transactions are going to freeze, triggering SQL0964C on production.</p>
              <div class="code-example">
                <div class="code-language">Diagnosing Log Bottlenecks</div>
                <pre><code><span class="comment"># Check the active log pathway for log utilization</span>
db2 "SELECT TOTAL_LOG_AVAILABLE, TOTAL_LOG_USED FROM TABLE(SYSPROC.MON_GET_TRANSACTION_LOG(-1))"

<span class="comment"># If an old log isn't being archived because of a hung program holding the Oldest Commit:</span>
db2 "SELECT AGENT_ID FROM SYSIBMADM.SNAPAPPL WHERE APPL_STATUS = 'UOW WAITING'"</code></pre>
              </div>
            </div>

            <div class="subsection" id="t25-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="disadvantages-box font-code">
                <h4><i class="fas fa-bug"></i> Active Log Spanning</h4>
                <p>Ensure that active logs and archived logs are on physically separate storage controllers. If the SAN disk hosting the active logs physically fries, but the archived logs and the database tables are intact on other nodes, DBAs can still perform database recovery.</p>
              </div>
            </div>
          </section>

          <section id="topic26" class="section">
            <h2 class="section-title"><i class="fas fa-hdd"></i> Topic 26: DB2 Backup and Recovery - Backup Operations</h2>
            <div class="subsection" id="t26-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                Taking <strong>Backups</strong> produces monolithic, structured, proprietary image files spanning the entire database or targeted tablespaces. Enterprise backups run ONLINE to avoid downtime. When executing an ONLINE backup, DB2 internally copies data pages as they exist, while simultaneously tracking DML modifications taking place during the backup window (putting them in the active log). An online backup image is physically "dirty" and unusable until a rollforward applies those missing logs. DB2 supports Full, Incremental, and Delta backup types to save space.
              </p>
            </div>
            
            <div class="subsection" id="t26-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">DB2 CLP - Taking Backups</div>
                <pre><code><span class="comment">-- Standard Offline Backup (Database must be deactivated)</span>
db2 "BACKUP DATABASE HRDB TO /backups/full COMPRESS"

<span class="comment">-- Online Backup (Users are connected and working)</span>
db2 "BACKUP DATABASE HRDB ONLINE TO /backups/online INCLUDE LOGS COMPRESS"

<span class="comment">-- Check the internal History File to see previous backup stamps and LSNs</span>
db2 "LIST HISTORY BACKUP ALL FOR HRDB"

<span class="comment">-- Tablespace-level backup (Useful for multi-terabyte databases where fulls are slow)</span>
db2 "BACKUP DATABASE HRDB TABLESPACE (USERSPACE1) ONLINE TO /backups/tbsp"</code></pre>
              </div>
            </div>

            <div class="subsection" id="t26-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: INCLUDE LOGS directive</h3>
              <p><strong>Scenario:</strong> You need to ship yesterday's production backup to the QA team for a testing refresh. They don't have access to the production archive log mount.</p>
              <div class="code-example">
                <div class="code-language">Executing self-contained backups</div>
                <pre><code><span class="comment"># By adding INCLUDE LOGS, DB2 packages the active logs actively changing </span>
<span class="comment"># during the exact timeframe of the backup directly INSIDE the monolithic backup image.</span>
db2 "BACKUP DATABASE HRDB ONLINE TO /exports INCLUDE LOGS"

<span class="comment"># You now have a single file (e.g. HRDB.0.inst1.DBPART000.20231015143000.001)</span>
<span class="comment"># You can SCP this single file to QA safely.</span></code></pre>
              </div>
            </div>
            
            <div class="subsection" id="t26-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="advantages-box font-code">
                <h4><i class="fas fa-check-circle"></i> Utilizing Utility Heap (UTIL_HEAP_SZ)</h4>
                <p>Backup operations do not share memory with standard query executions. They pull RAM from the <code>UTIL_HEAP_SZ</code>. If a backup is running disastrously slowly across a 2TB database, increasing the Utility Heap allows DB2 to allocate more concurrent thread buffers to reading the storage pages.</p>
              </div>
            </div>
          </section>

          <section id="topic27" class="section">
            <h2 class="section-title"><i class="fas fa-undo-alt"></i> Topic 27: DB2 Backup and Recovery - Recovery Operations</h2>
            <div class="subsection" id="t27-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                <strong>Recovery</strong> is a two-phased operation: <strong>RESTORE</strong> followed by <strong>ROLLFORWARD</strong>. 
                Running <code>RESTORE</code> unpacks the binary image file over the empty tablespace containers. However, if it was an ONLINE backup, the database remains in 'Rollforward Pending' status. You must then run <code>ROLLFORWARD</code>, which forces DB2 to hunt down the archived log files, replay the transactions missing during the backup, and bring the state to the "End of Logs" or a specific "Point In Time".
              </p>
            </div>
            
            <div class="subsection" id="t27-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">DB2 CLP - Recovery Sequence</div>
                <pre><code><span class="comment">-- Phase 1: Unpack the image using the exact timestamp format (YYYYMMDDHHMMSS)</span>
db2 "RESTORE DATABASE HRDB FROM /backups TAKEN AT 20231015143000"

<span class="comment">-- Phase 2: Rollforward to the absolute end of the available archive logs, and STOP</span>
<span class="comment">-- The 'AND STOP' command removes the 'Rollforward Pending' lock, exposing the DB to clients</span>
db2 "ROLLFORWARD DATABASE HRDB TO END OF LOGS AND STOP"

<span class="comment">-- (Alternative) Restore to a Point In Time (Whoops, the Junior DBA dropped a table at 2PM!)</span>
db2 "ROLLFORWARD DATABASE HRDB TO 2023-10-15-13.59.59.000000 AND STOP"</code></pre>
              </div>
            </div>

            <div class="subsection" id="t27-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: The "Oops" Scenario</h3>
              <p><strong>Scenario:</strong> At 10:15 AM, an application developer accidentally truncates the <code>ORDERS</code> table. An online backup was taken at 02:00 AM.</p>
              <div class="code-example">
                <div class="code-language">Executing PIT Recovery</div>
                <pre><code><span class="comment"># 1. Nuke the ruined active database by restoring yesterday's clean structural image</span>
db2 "RESTORE DATABASE OSDB FROM /backups/online TAKEN AT 20231014020000"

<span class="comment"># 2. Tell the engine to play back all the logs from 2AM, right up to 10:14 AM and HALT</span>
db2 "ROLLFORWARD DATABASE OSDB TO 2023-10-14-10.14.59.000000 USING LOCAL TIME AND STOP"

<span class="comment"># Result: 8 hours of legitimate orders are saved, but the truncation command is skipped.</span></code></pre>
              </div>
            </div>

            <div class="subsection" id="t27-summary">
              <h3 class="subsection-title">5. Summary Table</h3>
              <table class="table">
                <thead><tr><th>Utility Phase</th><th>DB Status After Command</th><th>Developer Action</th></tr></thead>
                <tbody>
                  <tr><td><code>RESTORE DB</code></td><td>Rollforward Pending</td><td>Developer cannot connect (SQL1117N). DB is locked in transit.</td></tr>
                  <tr><td><code>ROLLFORWARD ... TO END OF LOGS</code></td><td>Still Rollforward Pending</td><td>Logs are injected but the DB remains sealed awaiting final confirmation.</td></tr>
                  <tr><td><code>ROLLFORWARD ... AND STOP</code></td><td>Normal / Active</td><td>DB is opened for connections; logical point-in-time branch completes.</td></tr>
                </tbody>
              </table>
            </div>
"""

content = old_content_pattern.sub(topic_24_to_27_chunk + r'\1', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS BATCH 4")
import re

file_path = r'd:\Materials\Skills\Github\ITI-Notes\Notes\db2-notes.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update sidebar
old_nav_pattern = re.compile(
    r'(<li>\s*<a href="#topic14">.*?)(<li>\s*<a href="#cheat-sheet">)',
    re.DOTALL
)
new_nav = """<li>
            <a href="#roadmap"><i class="fas fa-server"></i> DB2 Course Roadmap (Topics 14-48)</a>
            <ul>
              <li><a href="#topic14">Topic 14: Maintaining Data - DML</a></li>
              <li><a href="#topic15">Topic 15: Detective Game (Troubleshooting)</a></li>
              <li><a href="#topic16">Topic 16: Administering Instances (Pending)</a></li>
              <!-- Follow-up topics will be injected here in later batches -->
            </ul>
          </li>
          """
content = old_nav_pattern.sub(new_nav + r'\2', content)

# 2. Update the main content body
# Replaces everything between the additional topics comment and Section 6
old_content_pattern = re.compile(
    r'(<!-- ADDITIONAL ITI STUDY NOTE TOPICS \(14 TO 48\)\s*-->).*?(<!-- Section 6: Best Practices & Performance Tips -->)',
    re.DOTALL
)

topic_14_15 = """
          <section id="topic14" class="section">
            <h2 class="section-title"><i class="fas fa-database"></i> Topic 14: Maintaining DB2 Data - DML Statements</h2>

            <div class="subsection" id="t14-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                <strong>Data Manipulation Language (DML)</strong> instructions form the core toolkit for interacting with DB2 data. In IBM DB2, DML operations (SELECT, INSERT, UPDATE, DELETE, MERGE) are deeply integrated with the engine's <strong>Transactional Logging</strong> and <strong>Locking Manager</strong>. 
                Whenever a DML query modifies data, DB2 does not instantly write the change to the physical tablespace disk. Instead, the change happens in the <em>Buffer Pool</em> (RAM) while the transaction details are recorded securely to the <em>Active Transaction Log</em>. This multi-tier architectural approach ensures extreme performance through delayed I/O and absolute ACID (Atomicity, Consistency, Isolation, Durability) compliance in enterprise recovery scenarios.
              </p>
              <div class="concept-grid">
                <div class="concept-card">
                  <h5><i class="fas fa-bolt"></i> Buffered Writes</h5>
                  <p>Updates are written to memory (buffer pool dirty pages). Background page cleaners asynchronously push these down to disk, avoiding I/O bottleneck during peak inserts.</p>
                </div>
                <div class="concept-card">
                  <h5><i class="fas fa-shield-alt"></i> Write-Ahead Logging (WAL)</h5>
                  <p>DB2 guarantees that the log records reflecting a DML change are physically safely written to disk <em>before</em> the modified dirty data page is written to the tablespace.</p>
                </div>
              </div>
            </div>

            <div class="subsection" id="t14-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <p>The DB2 Command Line Processor offers rich extensions to ANSI SQL for robust manipulation.</p>
              <div class="code-example">
                <div class="code-language">DB2 CLP - DML Command Syntax</div>
                <pre><code><span class="comment">-- Bulk Insert utilizing NEXT VALUE for Identity Columns</span>
INSERT INTO HR.Employees (EmpID, Name, Dept, Salary) 
VALUES (NEXT VALUE FOR HR.EmpSeq, 'Youssef Ahmed', 'IT', 95000.00);

<span class="comment">-- Sub-select Insert (Copies large swathes of data)</span>
INSERT INTO HR.EmployeeArchive (EmpID, Name, EndDate)
SELECT EmpID, Name, CURRENT DATE FROM HR.Employees WHERE Status = 'Terminated';

<span class="comment">-- Positioned Update using a Cursor (Advanced DBA usage)</span>
UPDATE HR.Employees SET Salary = Salary * 1.05 WHERE CURRENT OF EmployeeCursor;

<span class="comment">-- UPSERT / MERGE Statement (Inserts if new, Updates if existing - High Performance)</span>
MERGE INTO HR.Inventory AS target
USING (VALUES ('Laptop', 50)) AS source (Product, Quantity)
ON target.Product = source.Product
WHEN MATCHED THEN
  UPDATE SET target.Quantity = target.Quantity + source.Quantity
WHEN NOT MATCHED THEN
  INSERT (Product, Quantity) VALUES (source.Product, source.Quantity);</code></pre>
              </div>
            </div>

            <div class="subsection" id="t14-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: Telecom Bulk Operations</h3>
              <p><strong>Scenario:</strong> You are the DBA at a Telecom. Every night, millions of call detail records (CDRs) are loaded. We need to implement a massive batch update of subscriber states using `MERGE` and handle high-volume inserts without crashing logs.</p>
              <div class="code-example">
                <div class="code-language">CLP Setup & Operations</div>
                <pre><code><span class="comment"># 1. Set the CLI prompt</span>
db2 "CONNECT TO BILLING"

<span class="comment"># 2. Turn off autocommit to control the transaction scope manually</span>
db2 +c "UPDATE Subscribers SET Status = 'SUSPENDED' WHERE BillDue > 90"

<span class="comment"># 3. Create a massive temporary table block and insert offline data</span>
db2 +c "DECLARE GLOBAL TEMPORARY TABLE SESSION.TempCDR 
        (CallID INT, Duration INT) 
        ON COMMIT PRESERVE ROWS NOT LOGGED"

<span class="comment"># 4. Perform the massive commit to finalize the transaction and free the active log</span>
db2 "COMMIT"</code></pre>
              </div>
              <div class="definition-box">
                <h4><i class="fas fa-eye"></i> Behind the Scenes</h4>
                <p>By defining the temporary table as <code>NOT LOGGED</code> and manipulating the commit boundary, we prevented DB2 from dumping terabytes of temporary transaction logs into the recovery chain for a volatile staging table, saving both Disk I/O and CPU context switches.</p>
              </div>
            </div>

            <div class="subsection" id="t14-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="disadvantages-box font-code">
                <h4><i class="fas fa-bug"></i> Error SQL0964C</h4>
                <p><strong>Error Message:</strong> The transaction log for the database is full.</p>
                <p><strong>Cause:</strong> A single DML statement (like a massive DELETE) has exhausted all primary and secondary active logs without issuing a COMMIT.</p>
                <p><strong>Fix:</strong> Commit more frequently (batch your operations), or increase the database configuration parameters: 
                <code>db2 "UPDATE DB CFG FOR BILLING USING LOGPRIMARY 50 LOGSECOND 100"</code></p>
              </div>
            </div>

            <div class="subsection" id="t14-summary">
              <h3 class="subsection-title">5. Summary Table</h3>
              <table class="table">
                <thead><tr><th>DML Command</th><th>DB2-Specific Execution Characteristics</th><th>DBA Pro-Tip</th></tr></thead>
                <tbody>
                  <tr><td><code>MERGE</code></td><td>Executes dual-logic (insert/update) in a single tablespace pass, saving heavily on logical physical reads.</td><td>Always use over programmatic IF/ELSE loops in external application code.</td></tr>
                  <tr><td><code>INSERT (NOT LOGGED)</code></td><td>Skips heavy transactional log writes (using alternative LOB mechanisms or temp tables).</td><td>Essential for ETL jobs. Data is unrecoverable if transaction rolls back.</td></tr>
                  <tr><td><code>COMMIT</code> / <code>ROLLBACK</code></td><td>Releases row/table locks allowing high concurrency and writes final state to WAL.</td><td>Never let batch updates run boundlessly; always cap batches at 100k-500k rows.</td></tr>
                </tbody>
              </table>
            </div>
          </section>

          <section id="topic15" class="section">
            <h2 class="section-title"><i class="fas fa-search"></i> Topic 15: Let's Play - DB2 Detective Game! (Troubleshooting)</h2>
            <div class="subsection" id="t15-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                The <strong>DB2 Diagnostic Architecture</strong> utilizes the <code>db2diag.log</code> and the internal <em>First Failure Data Capture (FFDC)</em> mechanism to track engine state anomalies. Whenever the engine hits a snag—whether it is a lock escalation, a tablespace container out of space, or a fractured network packet—DB2 writes timestamped, extremely verbose diagnostic traces to these central logs. Troubleshooting is a game of finding the right PID/EDU token, cross-referencing the SQL CODE, and resolving the underlying architecture barrier.
              </p>
            </div>
            
            <div class="subsection" id="t15-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Diagnostics</h3>
              <div class="code-example">
                <div class="code-language">DB2 CLP - Diagnostic Tools</div>
                <pre><code><span class="comment">-- Find where the diagnostic log is currently kept</span>
db2 get dbm cfg | grep -i DIAGPATH

<span class="comment">-- Actively tail the DB2 diagnostic log (Linux) for real-time error tracking</span>
tail -f ~/sqllib/db2dump/db2diag.log

<span class="comment">-- Look up the meaning of an SQL error code</span>
db2 "? SQL0911N"

<span class="comment">-- Extract severe error records from the db2diag.log for yesterday</span>
db2diag -g level=Severe -H 1d</code></pre>
              </div>
            </div>

            <div class="subsection" id="t15-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: The Detective Scenario</h3>
              <p><strong>Scenario:</strong> You receive an urgent call from the Call Center floor. Application terminals are freezing with "Database Deadlock" timeouts. It's time to play detective.</p>
              <div class="code-example">
                <div class="code-language">The DB2 Detective Protocol</div>
                <pre><code><span class="comment"># Phase 1: Identify if it is Locking</span>
db2 "SELECT * FROM SYSIBMADM.SNAPLOCKWAIT" 
<span class="comment"># -> This shows Agent X is waiting on Agent Y</span>

<span class="comment"># Phase 2: Probe what Agent Y is doing</span>
db2 "SELECT * FROM SYSIBMADM.SNAPAPPL_INFO WHERE AGENT_ID = 'Y'"
<span class="comment"># -> This yields the connection IP (is it a rogue reporting job?)</span>

<span class="comment"># Phase 3: Gather the exact SQL Agent Y is holding open</span>
db2 "SELECT STMT_TEXT FROM SYSIBMADM.SNAPSTMT WHERE AGENT_ID = 'Y'"
<span class="comment"># -> Discover Agent Y executed a massive UPDATE without a COMMIT.</span>

<span class="comment"># Phase 4: Resolution (If authorized/rogue connection)</span>
db2 "FORCE APPLICATION ('Y')"</code></pre>
              </div>
            </div>

            <div class="subsection" id="t15-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="advantages-box font-code">
                <h4><i class="fas fa-check-circle"></i> Best Practices for the db2diag.log</h4>
                <p>Never let the <code>db2diag.log</code> grow indefinitely. A 50 GB log file is impossible to parse mathematically. Rotate it periodically:</p>
                <div class="code-example">
                  <pre><code>db2diag -A   <span class="comment"># Archives db2diag.log with a timestamp suffix</span></code></pre>
                </div>
              </div>
            </div>

            <div class="subsection" id="t15-summary">
              <h3 class="subsection-title">5. Summary Table</h3>
              <table class="table">
                <thead><tr><th>Tool / Utility</th><th>Function</th><th>Detective Usage</th></tr></thead>
                <tbody>
                  <tr><td><code>db2diag</code></td><td>Parses diagnostic logs</td><td>Filtering out info blocks to find 'Error' or 'Severe' failures related to crash instances.</td></tr>
                  <tr><td><code>db2 "? SQLXXX"</code></td><td>Error Catalog</td><td>Instant translation of a cryptic numerical error into human root-cause explanation.</td></tr>
                  <tr><td><code>FORCE APPLICATION</code></td><td>Connection Termination</td><td>The nuclear option when an application has frozen the system via lock escalation.</td></tr>
                </tbody>
              </table>
            </div>
          </section>
"""

content = old_content_pattern.sub(r'\1\n' + topic_14_15 + r'\n          \2', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS V3")
import re

file_path = r'd:\Materials\Skills\Github\ITI-Notes\Notes\db2-notes.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update sidebar
old_nav_pattern = re.compile(
    r'(<!-- Follow-up topics will be injected here in later batches -->)',
    re.DOTALL
)
new_nav = """<li><a href="#topic28">Topic 28: Data Concurrency Intro</a></li>
              <li><a href="#topic29">Topic 29: Concurrency Phenomena</a></li>
              <li><a href="#topic30">Topic 30: Isolation Levels</a></li>
              <li><a href="#topic31">Topic 31: More on Locking</a></li>
              <!-- Follow-up topics will be injected here in later batches -->"""
content = old_nav_pattern.sub(new_nav, content)


old_content_pattern = re.compile(
    r'(</section>\s*\n\s*<!-- Section 6: Best Practices & Performance Tips -->)',
    re.DOTALL
)

topic_28_to_31_chunk = """
          </section>

          <section id="topic28" class="section">
            <h2 class="section-title"><i class="fas fa-users-cog"></i> Topic 28: DB2 Server - Data Concurrency - Introduction</h2>
            <div class="subsection" id="t28-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                <strong>Data Concurrency</strong> ensures that thousands of users can simultaneously access the same database objects (Tables/Rows) while strictly preserving transactional integrity. DB2 enforces concurrency through its internal <strong>Lock Manager</strong>. This subsystem issues structural "Locks" in RAM against objects. If User A is updating a row (holding an 'X' Exclusive lock), User B's read request requesting an 'S' (Share) lock will natively queue and wait. This prevents data corruption at the cost of processing speed.
              </p>
            </div>
          </section>

          <section id="topic29" class="section">
            <h2 class="section-title"><i class="fas fa-ghost"></i> Topic 29: DB2 Server - Data Concurrency - Phenomena in Concurrent Access</h2>
            <div class="subsection" id="t29-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                Without proper locking governance, massive concurrency leads to mathematically anomalous logic errors. The relational database standard defines three critical corruption "Phenomena" that occur when overlapping transactions read/write the same data unconditionally.
              </p>
            </div>
            
            <div class="subsection" id="t29-syntax">
              <h3 class="subsection-title">2. Definitions of Phenomena</h3>
              <div class="definition-box">
                <h4><i class="fas fa-eye"></i> 1. Dirty Read</h4>
                <p>User A updates a row, but hasn't committed. User B reads this uncommitted row. User A rolls back. User B has captured data that technically never existed in the database.</p>
                
                <h4><i class="fas fa-exchange-alt"></i> 2. Non-Repeatable Read</h4>
                <p>User A reads a row. User B updates that same row and commits. User A reads the row again and the value has magically changed within the same transaction.</p>
                
                <h4><i class="fas fa-magic"></i> 3. Phantom Read</h4>
                <p>User A reads a range of records (e.g. <code>WHERE Salary > 50k</code>) getting 10 rows. User B inserts a new row matching that condition and commits. User A repeats the query and suddenly gets 11 rows.</p>
              </div>
            </div>
          </section>

          <section id="topic30" class="section">
            <h2 class="section-title"><i class="fas fa-layer-group"></i> Topic 30: DB2 Server - Data Concurrency - Isolation Levels</h2>
            <div class="subsection" id="t30-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                <strong>Isolation Levels</strong> dictate how fiercely the Lock Manager protects a transaction's scope against the three Phenomena. Higher isolation guarantees absolute mathematical purity but restricts concurrency (other users pile up waiting). Lower isolation ignores rules, granting instant speeds but risking dirty reads. DB2 sets <strong>CS (Cursor Stability)</strong> as the global default.
              </p>
            </div>
            
            <div class="subsection" id="t30-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">DB2 CLP - Setting Isolation</div>
                <pre><code><span class="comment">-- Setting it dynamically for the current session terminal</span>
db2 "CHANGE ISOLATION TO UR"

<span class="comment">-- Passing the clause at the end of a physical SQL query</span>
db2 "SELECT * FROM HR.Employees WITH UR"

<span class="comment">-- Binding a stored procedure using strict isolation</span>
db2 "BIND logic.bnd ISOLATION RR"</code></pre>
              </div>
            </div>

            <div class="subsection" id="t30-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: The "WITH UR" Reporting Hack</h3>
              <p><strong>Scenario:</strong> The financial reporting app is locking up the web store during its 9AM run. The report takes 10 minutes to sum all invoices, casting 'S' (Share) locks on rows that the webstore needs to update.</p>
              <div class="code-example">
                <div class="code-language">UR Optimization</div>
                <pre><code><span class="comment">-- Developer Modifies the report query:</span>
SELECT SUM(Amount) FROM FIN.Invoices WHERE Status = 'PAID' WITH UR;

<span class="comment">-- Under Uncommitted Read:</span>
<span class="comment">-- 1. DB2 does NOT cast 'S' locks on the rows.</span>
<span class="comment">-- 2. Web Store 'X' (exclusive) locks are permitted to update concurrently.</span>
<span class="comment">-- 3. The report risks a "Dirty Read" (might pull an invoice that isn't committed yet).</span>
<span class="comment">-- 4. Result: Web store is saved. A +/- 0.5% margin of error on a 10 million record report is a valid business trade-off for zero downtime.</span></code></pre>
              </div>
            </div>

            <div class="subsection" id="t30-summary">
              <h3 class="subsection-title">5. Summary Table</h3>
              <table class="table">
                <thead><tr><th>DB2 Isolation Level</th><th>Dirty Read</th><th>Non-Repeatable Read</th><th>Phantom Read</th><th>Concurrency</th></tr></thead>
                <tbody>
                  <tr><td><strong>Uncommitted Read (UR)</strong></td><td>Possible</td><td>Possible</td><td>Possible</td><td>MAXIMUM (Fastest)</td></tr>
                  <tr><td><strong>Cursor Stability (CS)</strong> <em>*Default*</em></td><td>Prevented</td><td>Possible</td><td>Possible</td><td>HIGH</td></tr>
                  <tr><td><strong>Read Stability (RS)</strong></td><td>Prevented</td><td>Prevented</td><td>Possible</td><td>LOW</td></tr>
                  <tr><td><strong>Repeatable Read (RR)</strong></td><td>Prevented</td><td>Prevented</td><td>Prevented</td><td>MINIMUM (Slowest)</td></tr>
                </tbody>
              </table>
            </div>
          </section>

          <section id="topic31" class="section">
            <h2 class="section-title"><i class="fas fa-lock"></i> Topic 31: DB2 Server - Data Concurrency - More on Locking</h2>
            <div class="subsection" id="t31-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                As transactions proceed, the Lock Manager memory block (governed by <code>LOCKLIST</code>) fills up. If a user runs <code>UPDATE TABLE ...</code> without a WHERE clause, they require millions of Row-level 'X' locks. When the <code>LOCKLIST</code> threshold (governed by <code>MAXLOCKS</code>) is breached, DB2 executes <strong>Lock Escalation</strong> automatically. It swaps 1,000,000 row locks for 1 giant Table lock to save memory. This instantly paralyzes all other users requiring access to that table, creating massive application bottlenecks.
              </p>
            </div>
            
            <div class="subsection" id="t31-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">Controlling Locking Memory</div>
                <pre><code><span class="comment">-- Allow DB2 automatic memory manager (STMM) to tune locklist (Dynamic)</span>
db2 "UPDATE DB CFG FOR HRDB USING LOCKLIST AUTOMATIC"

<span class="comment">-- explicitly force DB2 to wait 30 seconds before failing a lock request, rather than default indefinitely</span>
db2 "UPDATE DB CFG FOR HRDB USING LOCKTIMEOUT 30"</code></pre>
              </div>
            </div>

            <div class="subsection" id="t31-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="disadvantages-box font-code">
                <h4><i class="fas fa-bug"></i> Deadlocks (SQL0911N RC 2)</h4>
                <p><strong>Cause:</strong> Transaction A holds Lock 1 and wants Lock 2. Transaction B holds Lock 2 and wants Lock 1. Neither can proceed. This is a mathematical stalemate.</p>
                <p><strong>Resolution:</strong> DB2's background "Deadlock Detector" wakes up every 10 seconds (DLCHKTIME), spots the circular wait, chooses the transaction with the least work done as the "Victim", and forcefully ROLLS IT BACK to free the survivor.</p>
                <p><strong>DBA Fix:</strong> This is NOT a DBA configuration error. It is an application logic design flaw. Developers must rewrite their code to always lock objects in a standardized sequential order, or use DB2 Event Monitors to trace deadlock history and identify poorly written stored procedures.</p>
              </div>
            </div>
"""

content = old_content_pattern.sub(topic_28_to_31_chunk + r'\1', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS BATCH 5")
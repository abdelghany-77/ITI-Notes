import re

file_path = r'd:\Materials\Skills\Github\ITI-Notes\Notes\db2-notes.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_nav_pattern = re.compile(
    r'(<!-- Follow-up topics will be injected here in later batches -->)',
    re.DOTALL
)

new_nav = """<li><a href="#topic42">Topic 42: BLU Acceleration (Columnar DB)</a></li>
              <li><a href="#topic43">Topic 43: Adaptive Compression</a></li>
              <li><a href="#topic44">Topic 44: DB2 Workload Manager (WLM)</a></li>
              <li><a href="#topic45">Topic 45: DB2 pureScale vs DPF</a></li>
              <li><a href="#topic46">Topic 46: Advanced Security (RCAC & Roles)</a></li>
              <li><a href="#topic47">Topic 47: DB2 Audit Facility</a></li>
              <li><a href="#topic48">Topic 48: The Daily DBA Checklist (Conclusion)</a></li>
              <!-- Follow-up topics will be injected here in later batches -->"""
content = old_nav_pattern.sub(new_nav, content)

old_content_pattern = re.compile(
    r'(</section>\s*\n\s*<!-- Section 6: Best Practices & Performance Tips -->)',
    re.DOTALL
)

chunk = """
          </section>

          <section id="topic42" class="section">
            <h2 class="section-title"><i class="fas fa-microchip"></i> Topic 42: BLU Acceleration (Columnar Database)</h2>
            <div class="subsection" id="t42-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                Introduced in DB2 10.5, <strong>BLU Acceleration</strong> fundamentally changes how DB2 stores data. Traditional tables are "Row-Oriented" (great for OLTP/inserts). BLU tables are "Column-Oriented". By storing data continuously by column, analytical workloads (OLAP) that only need a subset of columns don't have to load irrelevant data into memory. BLU includes "Actionable Compression" and SIMD processing (Single Instruction Multiple Data), allowing the CPU to evaluate predicates directly against compressed data in the CPU cache without decompressing it first.
              </p>
            </div>
            
            <div class="subsection" id="t42-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">BLU Acceleration Table Creation</div>
                <pre><code><span class="comment">-- Setting the database configuration to default to exact BLU table creation</span>
db2 update db cfg for PRODDB using DFT_TABLE_ORG COLUMN 

<span class="comment">-- Create a table specifically overriding the default (ORGANIZE BY COLUMN)</span>
db2 "CREATE TABLE SALES_ANALYTICS (
    REGION VARCHAR(50), 
    REVENUE DECIMAL(15,2)
) ORGANIZE BY COLUMN"</code></pre>
              </div>
            </div>

            <div class="subsection" id="t42-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: The OLAP Query Speedup</h3>
              <p><strong>Scenario:</strong> Generating an end-of-year Revenue Report across 5 billion rows takes 45 minutes on a standard Row table because it performs a massive Table Scan pulling all 50 columns into memory.</p>
              <div class="definition-box">
                <h4><i class="fas fa-tachometer-alt"></i> The BLU Approach</h4>
                <p>By migrating the table to <code>ORGANIZE BY COLUMN</code>, DB2 only reads the `REGION` and `REVENUE` data pages from disk. Because the data is highly compressed (column data is highly repetitive), it fits entirely in the CPU L3 Cache. The report drops from 45 minutes down to 3 seconds with zero manual indexes created.</p>
              </div>
            </div>

            <div class="subsection" id="t42-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="disadvantages-box font-code">
                <h4><i class="fas fa-exclamation-triangle"></i> BLU Limitations (The "Not For Everything" Rule)</h4>
                <p><strong>Issue:</strong> Developers try to convert highly active OLTP websites (e-commerce carts) to BLU.</p>
                <p><strong>Fix:</strong> Columnar tables are terrible at high-concurrency single-row `INSERT`, `UPDATE`, and `DELETE` operations. Row-level locks in a columnar structure cause massive locking contention. Only use BLU for Data Warehouses and Data Marts.</p>
              </div>
            </div>
          </section>

          <section id="topic43" class="section">
            <h2 class="section-title"><i class="fas fa-compress-arrows-alt"></i> Topic 43: DB2 Adaptive Compression</h2>
            <div class="subsection" id="t43-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                DB2 offers advanced storage optimization mechanisms. Classic row compression uses a static dictionary built at table level. <strong>Adaptive Compression</strong> combines classic table-level dictionary compression with page-level compression. As data changes dynamically over time, DB2 builds temporary dictionaries strictly for individual data pages, ensuring optimal compression without requiring DBAs to constantly reorganize or rebuild the table dictionaries.
              </p>
            </div>
          </section>

          <section id="topic44" class="section">
            <h2 class="section-title"><i class="fas fa-server"></i> Topic 44: DB2 Workload Manager (WLM)</h2>
            <div class="subsection" id="t44-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                In an enterprise, competing applications connect to the same DB2 engine. A massive BI report might consume 95% of the CPU, starving the sub-second OLTP web application. <strong>DB2 Workload Manager (WLM)</strong> acts as a strict traffic cop. It allows the DBA to categorize inbound connections into "Service Classes" and assign rigid CPU, Memory, and locking thresholds to them.
              </p>
            </div>
            
            <div class="subsection" id="t44-syntax">
              <h3 class="subsection-title">2. Full Syntax: WLM Constraints</h3>
              <div class="code-example">
                <div class="code-language">WLM Setup</div>
                <pre><code><span class="comment">-- Create a Service Class for the Web Application (High Priority)</span>
db2 "CREATE SERVICE CLASS WebAppServiceClass PRIORITY HIGH"

<span class="comment">-- Create a Service Class for batch reporting (Low Priority, max 1 hour duration)</span>
db2 "CREATE SERVICE CLASS BatchReporting PRIORITY LOW"
db2 "CREATE THRESHOLD MaxReportTime FOR SERVICE CLASS BatchReporting ACTIVITIES 
     ENFORCEMENT DATABASE WHEN ESTIMATEDSQLCOST &gt; 100000 
     STOP EXECUTION"</code></pre>
              </div>
            </div>
          </section>

          <section id="topic45" class="section">
            <h2 class="section-title"><i class="fas fa-network-wired"></i> Topic 45: DB2 pureScale vs DPF</h2>
            <div class="subsection" id="t45-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                For extreme scalability, DB2 offers two clustering architectures:
                <br><br>
                <strong>DPF (Database Partitioning Feature):</strong> A "Shared-Nothing" architecture. Data is physically hashed and split across multiple DB2 servers (nodes). Queries are processed in parallel across all nodes. Incredible for Data Warehousing.
                <br>
                <strong>pureScale:</strong> A "Shared-Disk" architecture. Multiple DB2 servers (members) connect to a centralized SAN via high-speed RDMA networks. A centralized "Cluster Caching Facility (CF)" ensures all servers see consistent data. Incredible for high-availability OLTP (Mainframe-style clustering on Linux).
              </p>
            </div>
          </section>
          
          <section id="topic46" class="section">
            <h2 class="section-title"><i class="fas fa-user-shield"></i> Topic 46: Advanced Security (Roles & RCAC)</h2>
            <div class="subsection" id="t46-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                Beyond standard GRANT/REVOKE, enterprise security demands granular control. 
                <br><strong>Roles:</strong> DBAs can package multiple table privileges into a "Role" and assign that role to a group, severely minimizing catalog bloat.
                <br><strong>Row and Column Access Control (RCAC):</strong> Sometimes DBADM users (or even developers) shouldn't be able to see personal data (e.g., SSN, Salaries) inside a table they are meant to query. RCAC dynamically masks columns or restrict rows natively in the database engine based on the user's login, completely bypassing application logic.
              </p>
            </div>
          </section>

          <section id="topic47" class="section">
            <h2 class="section-title"><i class="fas fa-receipt"></i> Topic 47: DB2 Audit Facility</h2>
            <div class="subsection" id="t47-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                To comply with PCI-DSS or HIPAA, DBAs must prove exactly who executed what code. The <strong>DB2 Audit Facility (db2audit)</strong> acts strictly at the engine level. It acts separately from standard transaction logs, dumping binary audit records of all authentication events, DDL executions, and SECADM changes that cannot be bypassed.
              </p>
            </div>
          </section>

          <section id="topic48" class="section">
            <h2 class="section-title"><i class="fas fa-clipboard-check"></i> Topic 48: Conclusion - The Daily DBA Checklist</h2>
            <div class="subsection" id="t48-summary">
              <h3 class="subsection-title">5. Summary Table: Real-World DBA Lifecycle</h3>
              <table class="table">
                <thead><tr><th>Timeframe</th><th>Duties and Responsibilities</th></tr></thead>
                <tbody>
                  <tr><td><strong>Daily</strong></td><td>Check `db2diag.log` for FATAL/SEVERE warnings. Verify Backup Success (`db2 list history`). Ensure Transaction log disks have &gt;30% free space.</td></tr>
                  <tr><td><strong>Weekly</strong></td><td>Run `REORGCHK` and schedule `REORG` on fragmented tables. Regenerate `RUNSTATS` on heavy-mutation tables.</td></tr>
                  <tr><td><strong>Monthly</strong></td><td>Review WLM and Lock Timeout occurrences. Verify OS kernel/CPU metrics metrics baseline. Capacity Plan Disk limits.</td></tr>
                  <tr><td><strong>Quarterly</strong></td><td>Disaster Recovery testing. Shut down Primary HADR and perform full TAKEOVER to verify RTO/RPO SLA compliance. Apply DB2 FixPacks.</td></tr>
                </tbody>
              </table>
              <p>
                <br>
                <em>This concludes the comprehensive DB2 ITI Lab & Theory Guide.</em>
              </p>
            </div>
          </section>
"""

content = old_content_pattern.sub(chunk + r'\1', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS FINAL BATCH")
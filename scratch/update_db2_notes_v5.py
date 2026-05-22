import re

file_path = r'd:\Materials\Skills\Github\ITI-Notes\Notes\db2-notes.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update sidebar
old_nav_pattern = re.compile(
    r'(<!-- Follow-up topics will be injected here in later batches -->)',
    re.DOTALL
)
new_nav = """<li><a href="#topic19">Topic 19: Database Objects</a></li>
              <li><a href="#topic20">Topic 20: Security - Authentication</a></li>
              <li><a href="#topic21">Topic 21: Security - Authorization</a></li>
              <li><a href="#topic22">Topic 22: Security - Privileges</a></li>
              <li><a href="#topic23">Topic 23: Security - Misc</a></li>
              <!-- Follow-up topics will be injected here in later batches -->"""
content = old_nav_pattern.sub(new_nav, content)


old_content_pattern = re.compile(
    r'(</section>\s*\n\s*<!-- Section 6: Best Practices & Performance Tips -->)',
    re.DOTALL
)

topic_19_to_23_chunk = """
          </section>

          <section id="topic19" class="section">
            <h2 class="section-title"><i class="fas fa-cubes"></i> Topic 19: DB2 Server - Administering and Working with Database Objects</h2>
            <div class="subsection" id="t19-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                In DB2, maintaining <strong>Database Objects</strong> (Schemas, Tables, Indexes, Views, Aliases/Synonyms, Triggers) involves ensuring structural integrity and optimizing their accessibility. As applications evolve, so must the schema. DB2 maintains an exhaustive internal dictionary called the <strong>System Catalog</strong> (residing in schema <code>SYSIBM</code>) where all metadata about every object is strictly documented. Querying this catalog is essential for any object administration task.
              </p>
            </div>
            
            <div class="subsection" id="t19-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">DDL and Catalog Inspection</div>
                <pre><code><span class="comment">-- Inspect all custom schemas</span>
SELECT SCHEMANAME, OWNER FROM SYSCAT.SCHEMATA WHERE OWNERTYPE = 'U';

<span class="comment">-- Dynamically alter a table column length without dropping data</span>
ALTER TABLE HR.Employees ALTER COLUMN Email SET DATA TYPE VARCHAR(150);

<span class="comment">-- After a massive structural ALTER, the table may enter a "REORG PENDING" state</span>
REORG TABLE HR.Employees;

<span class="comment">-- Update the system catalogs with fresh statistical data about the object for the Optimizer</span>
RUNSTATS ON TABLE HR.Employees WITH DISTRIBUTION AND DETAILED INDEXES ALL;</code></pre>
              </div>
            </div>

            <div class="subsection" id="t19-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: The Maintenance Pending Trap</h3>
              <p><strong>Scenario:</strong> You altered a table adding a massive VARCHAR column. Application developers complain they receive SQL0668N indicating the table is inaccessible.</p>
              <div class="code-example">
                <div class="code-language">Resolution Protocol</div>
                <pre><code><span class="comment"># 1. Identify which tables are trapped in the REORG PENDING state</span>
db2 "SELECT TABSCHEMA, TABNAME FROM SYSIBMADM.ADMINTABINFO WHERE REORG_PENDING = 'Y'"

<span class="comment"># 2. Perform the reorganization to rebuild the pages on disk</span>
db2 "REORG TABLE HR.Employees"

<span class="comment"># 3. Always chase a REORG with a RUNSTATS</span>
db2 "RUNSTATS ON TABLE HR.Employees"</code></pre>
              </div>
            </div>

            <div class="subsection" id="t19-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="disadvantages-box font-code">
                <h4><i class="fas fa-bug"></i> Error SQL0668N</h4>
                <p><strong>Error Message:</strong> Operation not allowed for reason code "7" on table "XX".</p>
                <p><strong>Cause:</strong> Attempting to query a table that has had its physical structure altered but has not yet been reorganized.</p>
                <p><strong>Fix:</strong> Run <code>REORG TABLE XX</code>.</p>
              </div>
            </div>

            <div class="subsection" id="t19-summary">
              <h3 class="subsection-title">5. Summary Table</h3>
              <table class="table">
                <thead><tr><th>Utility</th><th>Purpose</th><th>When to run?</th></tr></thead>
                <tbody>
                  <tr><td><code>REORG</code></td><td>Rebuilds table pages, eliminating fragmentation and reclaiming disk space.</td><td>After large DELETE operations or ALTER TABLE modifications.</td></tr>
                  <tr><td><code>RUNSTATS</code></td><td>Updates catalog metadata (row counts, distributions) for the Query Optimizer.</td><td>After bulk loads, mass updates, or when query plans degrade.</td></tr>
                </tbody>
              </table>
            </div>
          </section>

          <section id="topic20" class="section">
            <h2 class="section-title"><i class="fas fa-passport"></i> Topic 20: DB2 Security - Authentication</h2>
            <div class="subsection" id="t20-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                <strong>Authentication</strong> determines ("Who are you?"). Unlike Oracle or SQL Server, DB2 (on Linux/Unix) <em>does not maintain its own password file</em> by default. It inherently delegates identity validation to the underlying <strong>Operating System (PAM/LDAP/Active Directory)</strong>. When a user executes <code>CONNECT TO HRDB USER alice USING passwd</code>, DB2 passes "alice" and "passwd" to the Linux kernel or LDAP server. If the OS approves, DB2 allows the connection.
              </p>
            </div>
            
            <div class="subsection" id="t20-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">Authentication DBM Configurations</div>
                <pre><code><span class="comment"># Check the current authentication mechanism at the Instance Level</span>
db2 get dbm cfg | grep -i AUTHENTICATION

<span class="comment"># Force Authentication at the SERVER level (Client sends plaintext/hashed password to Server OS)</span>
db2 "UPDATE DBM CFG USING AUTHENTICATION SERVER"

<span class="comment"># Force Client Authentication (Trusts the client OS to authenticate - insecure for WAN)</span>
db2 "UPDATE DBM CFG USING AUTHENTICATION CLIENT"

<span class="comment"># Employ encrypted passwords over the network</span>
db2 "UPDATE DBM CFG USING AUTHENTICATION SERVER_ENCRYPT"</code></pre>
              </div>
            </div>

            <div class="subsection" id="t20-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: The "Bad Password" Test</h3>
              <p><strong>Scenario:</strong> You need to create a new DBA account that has DB2 access but cannot log in via SSH interactively to the Linux server.</p>
              <div class="code-example">
                <div class="code-language">Creating an App-Only OS User</div>
                <pre><code><span class="comment#"># 1. Create native OS user with no shell access</span>
useradd -m -s /sbin/nologin appdb_user
passwd appdb_user

<span class="comment"># 2. Attempt remote DB2 connection</span>
db2 "CONNECT TO HRDB USER appdb_user USING new_password"
<span class="comment"># Result: Success! The OS validated the password via PAM, but blocks SSH.</span></code></pre>
              </div>
            </div>

            <div class="subsection" id="t20-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="advantages-box font-code">
                <h4><i class="fas fa-check-circle"></i> Best Practices</h4>
                <p>Never leave DB2 authentication set to <code>CLIENT</code> except in highly secured, isolated Intranets. Any user on a remote Windows PC named "Administrator" could connect and claim high privileges. Always use <code>SERVER_ENCRYPT</code> to prevent wire packet sniffing.</p>
              </div>
            </div>
          </section>

          <section id="topic21" class="section">
            <h2 class="section-title"><i class="fas fa-user-shield"></i> Topic 21: DB2 Security - Authorization</h2>
            <div class="subsection" id="t21-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                <strong>Authorization</strong> determines ("What are you allowed to do once connected?"). DB2 handles authorization through hierarchical <strong>Authorities</strong> (spanning entire instances or databases) and <strong>Privileges</strong> (granular access to specific objects). The major Authorities are <code>SYSADM</code> (Sysadmin - OS Level), <code>DBADM</code> (Database Admin), <code>SECADM</code> (Security Admin - specifically splits security off from DBADM), and <code>DATAACCESS</code>.
              </p>
            </div>
            
            <div class="subsection" id="t21-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">Managing DB2 Authorities</div>
                <pre><code><span class="comment">-- Which OS group actually holds the ultimate SYSADM power?</span>
db2 get dbm cfg | grep -i SYSADM_GROUP

<span class="comment">-- (Requires SECADM or SYSADM) Grant DBADM to a user over a specific database</span>
db2 "GRANT DBADM ON DATABASE TO USER alice"

<span class="comment">-- Grant Security Administration power (they can grant access to others)</span>
db2 "GRANT SECADM ON DATABASE TO USER bob"

<span class="comment">-- Determine what authorities you currently possess on the active connection</span>
db2 "SELECT * FROM TABLE(SYSPROC.AUTH_LIST_AUTHORITIES_FOR_AUTHID('ALICE', 'U'))"</code></pre>
              </div>
            </div>

            <div class="subsection" id="t21-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: Separation of Duties</h3>
              <p><strong>Scenario:</strong> According to Sarbanes-Oxley (SOX) compliance, the person who manages database architecture (DBADM) cannot be the same person who manages user access (SECADM), to prevent a DBA from granting themselves access to payroll data.</p>
              <div class="code-example">
                <div class="code-language">SOX Implementation</div>
                <pre><code><span class="comment"># 1. As the ultimate instance owner, delegate permissions</span>
db2 "GRANT SECADM ON DATABASE TO USER security_officer"
db2 "GRANT DBADM WITHOUT DATAACCESS ON DATABASE TO USER architect"

<span class="comment"># Result: 'architect' can build tables, drop tables, and run REORGs.</span>
<span class="comment"># But 'architect' CANNOT run SELECT * FROM Payroll_Table.</span></code></pre>
              </div>
            </div>

            <div class="subsection" id="t21-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="disadvantages-box font-code">
                <h4><i class="fas fa-bug"></i> Error SQL1092N</h4>
                <p><strong>Error Message:</strong> The user does not have the authority to perform the requested command.</p>
                <p><strong>Cause:</strong> Attempting to run a <code>db2 backup db</code> without having SYSADM, DBADM, or SYSCTRL authority.</p>
              </div>
            </div>
          </section>
          
          <section id="topic22" class="section">
            <h2 class="section-title"><i class="fas fa-key"></i> Topic 22: DB2 Security - Privileges</h2>
            <div class="subsection" id="t22-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                While Authorities grant broad sweeping power, <strong>Privileges</strong> are surgical. They grant actions (SELECT, INSERT, UPDATE, DELETE, EXECUTE) on specific database objects (Tables, Views, Procedures, Packages). Privileges can be granted to individual <code>USERS</code> or OS-level <code>GROUPS</code>, or DB2-internal <code>ROLES</code>.
              </p>
            </div>
            
            <div class="subsection" id="t22-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">Grant and Revoke Privileges</div>
                <pre><code><span class="comment">-- Grant read access to the developers group</span>
GRANT SELECT ON TABLE HR.Employees TO GROUP DevGroup;

<span class="comment">-- Grant execution capability on a stored procedure</span>
GRANT EXECUTE ON PROCEDURE Calc_Taxes TO USER charlie;

<span class="comment">-- Utilize DB2 Roles (Internal DB2 groups that don't require OS administration)</span>
CREATE ROLE DataAnalyst;
GRANT SELECT ON HR.Sales TO ROLE DataAnalyst;
GRANT ROLE DataAnalyst TO USER reporter_dan;

<span class="comment">-- Revoke privilege</span>
REVOKE INSERT ON HR.Employees FROM USER alice;</code></pre>
              </div>
            </div>

            <div class="subsection" id="t22-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: The View Shield</h3>
              <p><strong>Scenario:</strong> You have an HR table with salaries. Managers need to see Employee Names and Departments, but NOT Salary. You must restrict access effectively.</p>
              <div class="code-example">
                <div class="code-language">View Abstraction Security</div>
                <pre><code><span class="comment">-- 1. Revoke absolute access from the base table</span>
REVOKE SELECT ON TABLE HR.Employees FROM PUBLIC;

<span class="comment">-- 2. Create the abstraction view (Developer needs DBADM or explicit rights to base table to create this)</span>
CREATE VIEW HR.V_Directory AS 
  SELECT EmpID, Name, Dept FROM HR.Employees;

<span class="comment">-- 3. Grant access ONLY to the view</span>
GRANT SELECT ON VIEW HR.V_Directory TO GROUP Managers;</code></pre>
              </div>
            </div>

            <div class="subsection" id="t22-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="advantages-box font-code">
                <h4><i class="fas fa-check-circle"></i> DB2 Roles vs OS Groups</h4>
                <p>Always rely on DB2 <code>ROLES</code> instead of OS <code>GROUPS</code> when possible. OS Groups require Linux Sysadmins to add/remove members, slowing down ticket resolution. DB2 Roles can be entirely managed internally via <code>GRANT ROLE...</code> by the SECADM.</p>
              </div>
            </div>
          </section>
          
          <section id="topic23" class="section">
            <h2 class="section-title"><i class="fas fa-shield-alt"></i> Topic 23: DB2 Security - Miscellaneous (RCAC, LBAC, Audit)</h2>
            <div class="subsection" id="t23-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                Beyond baseline permissions, DB2 introduced highly advanced compliance security models. <strong>Row and Column Access Control (RCAC)</strong> dictates that even if you have SELECT access to a table, a dynamic policy evaluates your user token and filters/masks the returning rows or masks data (e.g., masking credit cards). <strong>Audit Facility</strong> asynchronously intercepts critical events (failed logins, DDL drops) and writes them to encrypted audit buffers.
              </p>
            </div>
            
            <div class="subsection" id="t23-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">RCAC Masking Implementation</div>
                <pre><code><span class="comment">-- Create a mask on the Salary column so only HR users see real data, everyone else sees 0</span>
CREATE MASK mask_salary ON HR.Employees
  FOR COLUMN Salary RETURN 
    CASE WHEN VERIFY_GROUP_FOR_USER(SESSION_USER, 'HR_GRP') = 1 
         THEN Salary
         ELSE 0.00
    END
  ENABLE;

<span class="comment">-- Enforce RCAC on the table</span>
ALTER TABLE HR.Employees ACTIVATE COLUMN ACCESS CONTROL;</code></pre>
              </div>
            </div>

            <div class="subsection" id="t23-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: SECADM Audit Trace</h3>
              <p><strong>Scenario:</strong> Complying with PCI-DSS, you must log every single query executed against the Credit Card vault without relying on application logs and without hurting throughput.</p>
              <div class="code-example">
                <div class="code-language">Audit Facility Setup</div>
                <pre><code><span class="comment">-- Executed connected as SECADM</span>
<span class="comment">-- 1. Create the Audit Policy</span>
CREATE AUDIT POLICY TrackVAULT CATEGORIES EXECUTE STATUS BOTH ERROR TYPE NORMAL;

<span class="comment">-- 2. Bind the policy strictly to the target table</span>
AUDIT TABLE FIN.CreditCards USING POLICY TrackVAULT;

<span class="comment">-- The db2audit utility process will spool binary logs. The SECADM periodically extracts them to tables.</span>
db2audit extract file /tmp/audit_out.del from files /home/db2inst1/sqllib/security/auditdata</code></pre>
              </div>
            </div>

            <div class="subsection" id="t23-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="advantages-box font-code">
                <h4><i class="fas fa-check-circle"></i> Audit Performance</h3>
                <p>Never set <code>AUDIT DATABASE USING POLICY... CATEGORIES ALL STATUS BOTH</code>. Because of IBM's asynchronous audit buffer, DB2 acts extremely fast, but auditing "ALL" traffic will exhaust your IO subsystem dumping out gigabytes of trace data daily.</p>
              </div>
            </div>
"""

content = old_content_pattern.sub(topic_19_to_23_chunk + r'\1', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS BATCH 3")
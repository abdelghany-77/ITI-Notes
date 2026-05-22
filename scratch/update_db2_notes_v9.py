import re

file_path = r'd:\Materials\Skills\Github\ITI-Notes\Notes\db2-notes.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_nav_pattern = re.compile(
    r'(<!-- Follow-up topics will be injected here in later batches -->)',
    re.DOTALL
)

new_nav = """<li><a href="#topic37">Topic 37: DB2 Upgrade Roadmap (v10 to v11)</a></li>
              <li><a href="#topic38">Topic 38: Preparing the Environment for DB2</a></li>
              <li><a href="#topic39">Topic 39: Linux Basics for DB2 DBAs</a></li>
              <li><a href="#topic40">Topic 40: DB2 10.1 Installation on Linux</a></li>
              <li><a href="#topic41">Topic 41: Post-Installation & Data Studio Setup</a></li>
              <!-- Follow-up topics will be injected here in later batches -->"""
content = old_nav_pattern.sub(new_nav, content)

old_content_pattern = re.compile(
    r'(</section>\s*\n\s*<!-- Section 6: Best Practices & Performance Tips -->)',
    re.DOTALL
)

chunk = """
          </section>

          <section id="topic37" class="section">
            <h2 class="section-title"><i class="fas fa-level-up-alt"></i> Topic 37: DB2 Upgrade Roadmap (v10 to v11)</h2>
            <div class="subsection" id="t37-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                Upgrading IBM DB2 from version 10.x to 11.x is a major architectural shift. It introduces native BLU Acceleration (Columnar structures) and deeper advanced compression natively. An upgrade isn't simply replacing binaries; it requires migrating system catalogs, managing deprecated features, and often recompiling bound packages.
              </p>
            </div>
            
            <div class="subsection" id="t37-syntax">
              <h3 class="subsection-title">2. Full Syntax & CLP Commands</h3>
              <div class="code-example">
                <div class="code-language">DB2 Upgrade Fundamentals</div>
                <pre><code><span class="comment">-- Run db2ckupgrade BEFORE upgrading to verify database readiness</span>
db2ckupgrade -e -l db2ckupgrade.log -u &lt;username&gt; -p &lt;password&gt; -d PRODDB

<span class="comment">-- Upgrade the DB2 Instance (Run as root)</span>
/opt/ibm/db2/V11.1/instance/db2iupgrade db2inst1

<span class="comment">-- Upgrade the Database (Run as the instance owner)</span>
db2 UPGRADE DATABASE PRODDB</code></pre>
              </div>
            </div>

            <div class="subsection" id="t37-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: Rebinding Packages</h3>
              <p><strong>Scenario:</strong> After successfully running <code>UPGRADE DATABASE</code>, your applications are receiving SQL0805N (Package not found or invalid). The SQL optimizer in V11 has changed, invalidating the V10 bound access plans.</p>
              <div class="code-example">
                <div class="code-language">Post-Upgrade Rebind</div>
                <pre><code><span class="comment"># Rebind all packages in the database to optimize for the new V11 Engine</span>
db2rbind PRODDB -l rebind_V11.log all</code></pre>
              </div>
            </div>

            <div class="subsection" id="t37-summary">
              <h3 class="subsection-title">5. Summary Table: Upgrade Considerations</h3>
              <table class="table">
                <thead><tr><th>Phase</th><th>Key Action</th></tr></thead>
                <tbody>
                  <tr><td><strong>Pre-Upgrade</strong></td><td>Backup databases, run db2ckupgrade, check OS kernel compatibility.</td></tr>
                  <tr><td><strong>Installation</strong></td><td>Install new DB2 V11 binaries in a new directory (Side-by-side).</td></tr>
                  <tr><td><strong>Instance Upgrade</strong></td><td>db2iupgrade migrates the instance metadata to the V11 path.</td></tr>
                  <tr><td><strong>Post-Upgrade</strong></td><td>db2rbind for packages, test applications, backup immediately.</td></tr>
                </tbody>
              </table>
            </div>
          </section>

          <section id="topic38" class="section">
            <h2 class="section-title"><i class="fas fa-server"></i> Topic 38: Preparing the Environment for DB2</h2>
            <div class="subsection" id="t38-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                DB2 is deeply intertwined with the underlying Linux/UNIX operating system. The DB2 engine requires strict Memory (RAM) kernel parameters (IPC, SHMMNI, SHMALL) and file descriptor limits to be configured in the OS BEFORE installation. If DB2 cannot allocate its initial Shared Memory segments during <code>db2start</code>, the instance will crash on launch.
              </p>
            </div>
          </section>

          <section id="topic39" class="section">
            <h2 class="section-title"><i class="fab fa-linux"></i> Topic 39: Linux Basics for DB2 DBAs</h2>
            <div class="subsection" id="t39-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                A DB2 DBA is inherently a Junior Linux Admin. Managing disk mounts, checking memory utilization, understanding the <code>root</code> versus <code>db2inst1</code> user isolation, and managing DB2 daemon background processes requires constant use of standard Linux bash utilities.
              </p>
            </div>
            
            <div class="subsection" id="t39-syntax">
              <h3 class="subsection-title">2. Full Syntax: The DBA's Linux Toolkit</h3>
              <div class="code-example">
                <div class="code-language">Critical Linux Commands</div>
                <pre><code><span class="comment"># Check if the DB2 core daemon is running in memory</span>
ps -ef | grep db2sysc

<span class="comment"># Check Linux RAM usage to ensure DB2 bufferpools aren't causing paging/swapping</span>
free -m

<span class="comment"># Verify disk space (Are the transaction logs going to fill the disk?)</span>
df -h

<span class="comment"># View the end of the DB2 diagnostic log (db2diag.log) in real-time</span>
tail -f ~/sqllib/db2dump/db2diag.log</code></pre>
              </div>
            </div>
          </section>

          <section id="topic40" class="section">
            <h2 class="section-title"><i class="fas fa-hdd"></i> Topic 40: DB2 10.1 Installation on Linux</h2>
            <div class="subsection" id="t40-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                Installing DB2 involves essentially unpacking binaries as <code>root</code> into <code>/opt/ibm/db2/V10.1</code>, checking license compliance, and generating the DB2 Instance and Fenced users. IBM provides the <code>db2setup</code> GUI (Java-based) or the silent configuration method via a response file for automated enterprise rollouts.
              </p>
            </div>

             <div class="subsection" id="t40-lab">
              <h3 class="subsection-title">3. Industry-Standard Practical Lab: Silent Installation</h3>
              <p><strong>Scenario:</strong> You need to install DB2 identically across 50 Linux VMs for a DPF (Partitioned) cluster. A GUI installer is impractical.</p>
              <div class="code-example">
                <div class="code-language">Silent Install</div>
                <pre><code><span class="comment"># Step 1: Create a Response File (db2server.rsp) defining the install path and users</span>
<span class="comment"># PROD=DB2_ENTERPRISE_SERVER_EDITION</span>
<span class="comment"># FILE=/opt/ibm/db2/V10.1</span>
<span class="comment"># INSTANCE=db2inst1</span>

<span class="comment"># Step 2: Run the silent installation as ROOT</span>
./db2setup -r /tmp/db2server.rsp -l /tmp/db2install.log</code></pre>
              </div>
            </div>
          </section>

          <section id="topic41" class="section">
            <h2 class="section-title"><i class="fas fa-tools"></i> Topic 41: Post-Installation & IBM Data Studio</h2>
            <div class="subsection" id="t41-concept">
              <h3 class="subsection-title">1. High-Level Concept & Architecture</h3>
              <p>
                Once the <code>db2sysc</code> daemon is running, administrators switch to client tools. <strong>IBM Data Studio</strong> is an Eclipse-based IDE that replaces the older DB2 Control Center. It connects via JDBC (Port 50000). While the CLP is required for low-level OS configuration and scripting, IBM Data Studio is superior for reading Visual Explain plans, managing SQL stored procedures, and generating DDL for massive schemas.
              </p>
            </div>
            
            <div class="subsection" id="t41-troubleshoot">
              <h3 class="subsection-title">4. DBA Best Practices & Troubleshooting</h3>
              <div class="definition-box">
                <h4><i class="fas fa-eye"></i> JDBC Firewall Troubleshooting</h4>
                <p><strong>Issue:</strong> You installed DB2, but Data Studio cannot connect. Error: <code>java.net.ConnectException</code>.</p>
                <p><strong>Cause:</strong> 1) The DB2 instance is not listening on TCP/IP. 2) The Linux Firewall is blocking port 50000.</p>
                <p><strong>Fix:</strong> <br>
                1. Set the registry: <code>db2set DB2COMM=tcpip</code><br>
                2. Check the port config: <code>db2 get dbm cfg | grep SVCENAME</code></p>
              </div>
            </div>
"""

content = old_content_pattern.sub(chunk + r'\1', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS BATCH 7")
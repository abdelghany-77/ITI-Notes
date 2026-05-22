// ========================================
// ITI Notes Hub - Main JavaScript
// Unified functionality for all pages
// ========================================

// Initialize everything when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  initializeDarkMode();
  initializeReadingProgress();
  initializeBackToTop();
  initializeCodeCopy();
  initializeSidebar();
  initializeKeyboardShortcuts();
  initializeSearch();
  observeAnimations();
  initializeScrollHandler();
});

// ========================================
// Throttled Scroll Handler
// ========================================
let scrollTicking = false;
const scrollCallbacks = [];

function registerScrollCallback(fn) {
  scrollCallbacks.push(fn);
}

function initializeScrollHandler() {
  window.addEventListener("scroll", () => {
    if (!scrollTicking) {
      requestAnimationFrame(() => {
        const scrollY = window.scrollY;
        const scrollHeight = document.documentElement.scrollHeight;
        const clientHeight = document.documentElement.clientHeight;
        scrollCallbacks.forEach((fn) => fn(scrollY, scrollHeight, clientHeight));
        scrollTicking = false;
      });
      scrollTicking = true;
    }
  });
}

// ========================================
// Dark Mode Manager
// ========================================
function initializeDarkMode() {
  const savedTheme = localStorage.getItem("theme") || "light";

  if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
  }

  let toggleBtn = document.querySelector(".dark-mode-toggle");
  if (!toggleBtn) {
    toggleBtn = document.createElement("button");
    toggleBtn.className = "dark-mode-toggle";
    toggleBtn.setAttribute("aria-label", "Toggle Dark Mode");
    toggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
    document.body.appendChild(toggleBtn);
  }

  const updateIcon = () => {
    const isDark = document.body.classList.contains("dark-mode");
    const icon = toggleBtn.querySelector("i");
    if (icon) {
      icon.className = isDark ? "fas fa-sun" : "fas fa-moon";
    }
  };

  updateIcon();

  toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    const isDark = document.body.classList.contains("dark-mode");
    localStorage.setItem("theme", isDark ? "dark" : "light");
    updateIcon();
  });
}

// ========================================
// Reading Progress Bar
// ========================================
function initializeReadingProgress() {
  let progressBar = document.querySelector(".reading-progress");
  if (!progressBar) {
    progressBar = document.createElement("div");
    progressBar.className = "reading-progress";
    document.body.appendChild(progressBar);
  }

  registerScrollCallback((scrollY, scrollHeight, clientHeight) => {
    const height = scrollHeight - clientHeight;
    if (height > 0) {
      const scrolled = (scrollY / height) * 100;
      progressBar.style.width = scrolled + "%";
    }
  });
}

// ========================================
// Back to Top Button
// ========================================
function initializeBackToTop() {
  let backToTopBtn = document.querySelector(".back-to-top");
  if (!backToTopBtn) {
    backToTopBtn = document.createElement("button");
    backToTopBtn.className = "back-to-top";
    backToTopBtn.setAttribute("aria-label", "Back to Top");
    backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    document.body.appendChild(backToTopBtn);
  }

  registerScrollCallback((scrollY) => {
    if (scrollY > 300) {
      backToTopBtn.classList.add("visible");
    } else {
      backToTopBtn.classList.remove("visible");
    }
  });

  backToTopBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

// ========================================
// Code Copy Functionality
// ========================================
function initializeCodeCopy() {
  const preBlocks = document.querySelectorAll("pre");

  preBlocks.forEach((pre) => {
    // Skip if already has a copy button or is inside .node-command
    if (pre.querySelector(".code-copy-btn") || pre.closest(".node-command")) {
      return;
    }

    const copyBtn = document.createElement("button");
    copyBtn.className = "code-copy-btn";
    copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';

    copyBtn.addEventListener("click", async (e) => {
      e.stopPropagation();
      const codeEl = pre.querySelector("code");
      const textToCopy = codeEl ? codeEl.textContent : pre.textContent;

      try {
        await navigator.clipboard.writeText(textToCopy);
        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        copyBtn.classList.add("copied");

        setTimeout(() => {
          copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
          copyBtn.classList.remove("copied");
        }, 2000);
      } catch (err) {
        // Fallback for non-HTTPS contexts
        try {
          const textarea = document.createElement("textarea");
          textarea.value = textToCopy;
          textarea.style.position = "fixed";
          textarea.style.opacity = "0";
          document.body.appendChild(textarea);
          textarea.select();
          document.execCommand("copy");
          document.body.removeChild(textarea);

          copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
          copyBtn.classList.add("copied");
          setTimeout(() => {
            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
            copyBtn.classList.remove("copied");
          }, 2000);
        } catch (fallbackErr) {
          copyBtn.innerHTML = '<i class="fas fa-times"></i> Failed';
          setTimeout(() => {
            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
          }, 2000);
        }
      }
    });

    pre.style.position = "relative";
    pre.appendChild(copyBtn);
  });
}

// ========================================
// Sidebar / TOC Navigation
// ========================================
function initializeSidebar() {
  // Support both sidebar types
  const sidebar =
    document.querySelector(".sidebar") ||
    document.querySelector(".toc-container");

  if (!sidebar) return;

  // Find or create toggle button
  let toggleBtn =
    document.querySelector(".sidebar-toggle") ||
    document.querySelector(".toggle-btn") ||
    document.querySelector(".toc-toggle");

  if (!toggleBtn) {
    toggleBtn = document.createElement("button");
    toggleBtn.className = "sidebar-toggle";
    toggleBtn.setAttribute("aria-label", "Toggle Navigation");
    toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
    document.body.appendChild(toggleBtn);
  }

  // Remove existing inline onclick to prevent double-toggling
  toggleBtn.removeAttribute("onclick");

  // Find or create overlay backdrop
  let overlay =
    document.querySelector(".sidebar-overlay") ||
    document.querySelector(".overlay") ||
    document.querySelector(".toc-backdrop");

  if (!overlay) {
    overlay = document.createElement("div");
    overlay.className = "sidebar-overlay";
    document.body.appendChild(overlay);
  }

  const openSidebar = () => {
    sidebar.classList.add("active");
    overlay.classList.add("active");
    const icon = toggleBtn.querySelector("i");
    if (icon) icon.className = "fas fa-times";
    toggleBtn.setAttribute("aria-expanded", "true");
  };

  const closeSidebar = () => {
    sidebar.classList.remove("active");
    overlay.classList.remove("active");
    const icon = toggleBtn.querySelector("i");
    if (icon) icon.className = "fas fa-bars";
    toggleBtn.setAttribute("aria-expanded", "false");
  };

  // Attach click handler — remove existing inline onclick first
  const newToggle = toggleBtn.cloneNode(true);
  toggleBtn.parentNode.replaceChild(newToggle, toggleBtn);
  toggleBtn = newToggle;

  toggleBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    if (sidebar.classList.contains("active")) {
      closeSidebar();
    } else {
      openSidebar();
    }
  });

  // Close on overlay click
  overlay.addEventListener("click", closeSidebar);

  // Close on sidebar link click (mobile)
  sidebar.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", () => {
      if (window.innerWidth <= 768) {
        closeSidebar();
      }
    });
  });

  // Expose globally for inline onclick handlers that may still exist
  window.toggleSidebar = () => {
    if (sidebar.classList.contains("active")) {
      closeSidebar();
    } else {
      openSidebar();
    }
  };
  window.closeSidebar = closeSidebar;
  window.toggleTOC = window.toggleSidebar;
  window.closeTOC = closeSidebar;

  // Scroll-spy for sidebar active link highlighting
  const navLinks = sidebar.querySelectorAll('a[href^="#"]');
  if (navLinks.length > 0) {
    const sectionSelectors = [
      "section[id]",
      ".session[id]",
      ".lesson[id]",
      ".content-section[id]",
      "[id].section",
      ".subsection[id]",
    ];
    const sections = document.querySelectorAll(sectionSelectors.join(", "));

    if (sections.length > 0) {
      registerScrollCallback((scrollY) => {
        let current = "";

        sections.forEach((section) => {
          const sectionTop = section.offsetTop;
          if (scrollY >= sectionTop - 120) {
            current = section.getAttribute("id");
          }
        });

        navLinks.forEach((link) => {
          link.classList.remove("active");
          if (link.getAttribute("href") === `#${current}`) {
            link.classList.add("active");
          }
        });
      });
    }
  }
}

// ========================================
// Keyboard Shortcuts
// ========================================
function initializeKeyboardShortcuts() {
  document.addEventListener("keydown", (e) => {
    // Ctrl/Cmd + D: Toggle dark mode
    if ((e.ctrlKey || e.metaKey) && e.key === "d") {
      e.preventDefault();
      const toggleBtn = document.querySelector(".dark-mode-toggle");
      if (toggleBtn) toggleBtn.click();
    }

    // Ctrl/Cmd + K: Focus search
    if ((e.ctrlKey || e.metaKey) && e.key === "k") {
      e.preventDefault();
      const searchInput = document.querySelector(".search-input");
      if (searchInput) searchInput.focus();
    }

    // Escape: Close sidebar
    if (e.key === "Escape") {
      const sidebar =
        document.querySelector(".sidebar.active") ||
        document.querySelector(".toc-container.active");
      if (sidebar) {
        sidebar.classList.remove("active");
        const overlay =
          document.querySelector(".sidebar-overlay.active") ||
          document.querySelector(".overlay.active") ||
          document.querySelector(".toc-backdrop.active");
        if (overlay) overlay.classList.remove("active");

        const toggleBtn =
          document.querySelector(".sidebar-toggle") ||
          document.querySelector(".toggle-btn") ||
          document.querySelector(".toc-toggle");
        if (toggleBtn) {
          const icon = toggleBtn.querySelector("i");
          if (icon) icon.className = "fas fa-bars";
        }
      }
    }

    // Ctrl/Cmd + Up: Scroll to top
    if ((e.ctrlKey || e.metaKey) && e.key === "ArrowUp") {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  });
}

// ========================================
// Search Functionality
// ========================================
function initializeSearch() {
  const searchInput = document.querySelector(".search-input");
  const searchableItems = document.querySelectorAll(
    ".course-card, .searchable-item"
  );

  if (!searchInput || searchableItems.length === 0) return;

  let debounceTimer;

  searchInput.addEventListener("input", (e) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const searchTerm = e.target.value.toLowerCase().trim();

      searchableItems.forEach((item) => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(searchTerm) ? "" : "none";
      });
    }, 200);
  });
}

// ========================================
// Scroll Animations (Course Cards)
// ========================================
function observeAnimations() {
  const animatedElements = document.querySelectorAll(".course-card");
  if (animatedElements.length === 0) return;

  // Track DOM order for stagger
  const elementOrder = new Map();
  animatedElements.forEach((el, i) => {
    elementOrder.set(el, i);
    el.style.opacity = "0";
    el.style.transform = "translateY(20px)";
    el.style.transition = "opacity 0.5s ease, transform 0.5s ease";
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const index = elementOrder.get(entry.target) || 0;
          const delay = Math.min(index * 80, 800);

          setTimeout(() => {
            entry.target.style.opacity = "1";
            entry.target.style.transform = "translateY(0)";
          }, delay);

          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  animatedElements.forEach((el) => observer.observe(el));
}

// ========================================
// Handle legacy scroll-to-top buttons
// ========================================
document.addEventListener("DOMContentLoaded", () => {
  // Support legacy .scroll-to-top and .scroll-top buttons
  const legacyBtns = document.querySelectorAll(".scroll-to-top, .scroll-top");
  legacyBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });

  // Expose scrollTopSmooth globally for inline onclick handlers
  window.scrollTopSmooth = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };
  window.scrollToTop = window.scrollTopSmooth;
});

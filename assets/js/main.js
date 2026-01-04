// ========================================
// ITI Notes Hub - Complete JavaScript
// All functionality in one file
// ========================================

console.log("Main.js loaded successfully");

// Initialize everything when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM Content Loaded");
  initializeDarkMode();
  initializeReadingProgress();
  initializeBackToTop();
  initializeCodeCopy();
  initializeSidebar();
  initializeKeyboardShortcuts();
  initializeSearch();
  observeAnimations();
  console.log("All features initialized");
});

// ========================================
// Dark Mode Manager
// ========================================
function initializeDarkMode() {
  console.log("Initializing dark mode...");

  // Get saved theme or default to light
  const savedTheme = localStorage.getItem("theme") || "light";
  console.log("Saved theme:", savedTheme);

  // Apply theme immediately
  if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
  }

  // Create dark mode toggle button if it doesn't exist
  let toggleBtn = document.querySelector(".dark-mode-toggle");
  if (!toggleBtn) {
    console.log("Creating dark mode toggle button");
    toggleBtn = document.createElement("button");
    toggleBtn.className = "dark-mode-toggle";
    toggleBtn.setAttribute("aria-label", "Toggle Dark Mode");
    toggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
    document.body.appendChild(toggleBtn);
  }

  // Update icon based on current theme
  const updateIcon = () => {
    const isDark = document.body.classList.contains("dark-mode");
    const icon = toggleBtn.querySelector("i");
    if (icon) {
      icon.className = isDark ? "fas fa-sun" : "fas fa-moon";
    }
    console.log("Icon updated to:", isDark ? "sun" : "moon");
  };

  updateIcon();

  // Toggle dark mode on click
  toggleBtn.addEventListener("click", () => {
    console.log("Dark mode toggle clicked");
    document.body.classList.toggle("dark-mode");
    const isDark = document.body.classList.contains("dark-mode");
    const theme = isDark ? "dark" : "light";
    localStorage.setItem("theme", theme);
    console.log("Theme saved:", theme);
    updateIcon();
  });

  console.log("Dark mode initialized successfully");
}

// ========================================
// Reading Progress Bar
// ========================================
function initializeReadingProgress() {
  // Create progress bar if it doesn't exist
  let progressBar = document.querySelector(".reading-progress");
  if (!progressBar) {
    progressBar = document.createElement("div");
    progressBar.className = "reading-progress";
    document.body.appendChild(progressBar);
  }

  // Update progress on scroll
  window.addEventListener("scroll", () => {
    const winScroll =
      document.body.scrollTop || document.documentElement.scrollTop;
    const height =
      document.documentElement.scrollHeight -
      document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    progressBar.style.width = scrolled + "%";
  });
}

// ========================================
// Back to Top Button
// ========================================
function initializeBackToTop() {
  // Create back to top button if it doesn't exist
  let backToTopBtn = document.querySelector(".back-to-top");
  if (!backToTopBtn) {
    backToTopBtn = document.createElement("button");
    backToTopBtn.className = "back-to-top";
    backToTopBtn.setAttribute("aria-label", "Back to Top");
    backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    document.body.appendChild(backToTopBtn);
  }

  // Show/hide button based on scroll position
  window.addEventListener("scroll", () => {
    if (window.pageYOffset > 300) {
      backToTopBtn.classList.add("visible");
    } else {
      backToTopBtn.classList.remove("visible");
    }
  });

  // Scroll to top on click
  backToTopBtn.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });
}

// ========================================
// Code Copy Functionality
// ========================================
function initializeCodeCopy() {
  const codeBlocks = document.querySelectorAll("pre code");

  codeBlocks.forEach((codeBlock) => {
    const pre = codeBlock.parentElement;

    // Create copy button if it doesn't exist
    if (!pre.querySelector(".code-copy-btn")) {
      const copyBtn = document.createElement("button");
      copyBtn.className = "code-copy-btn";
      copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';

      copyBtn.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(codeBlock.textContent);
          copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
          copyBtn.classList.add("copied");

          setTimeout(() => {
            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
            copyBtn.classList.remove("copied");
          }, 2000);
        } catch (err) {
          console.error("Failed to copy code:", err);
        }
      });

      pre.appendChild(copyBtn);
    }
  });
}

// ========================================
// Sidebar Navigation
// ========================================
function initializeSidebar() {
  const sidebar = document.querySelector(".sidebar");

  if (sidebar) {
    // Create toggle button if it doesn't exist
    let toggleBtn = document.querySelector(".sidebar-toggle");
    if (!toggleBtn) {
      toggleBtn = document.createElement("button");
      toggleBtn.className = "sidebar-toggle";
      toggleBtn.setAttribute("aria-label", "Toggle Sidebar");
      toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
      document.body.appendChild(toggleBtn);
    }

    // Toggle sidebar on click
    toggleBtn.addEventListener("click", () => {
      sidebar.classList.toggle("active");
      const icon = toggleBtn.querySelector("i");
      if (icon) {
        icon.className = sidebar.classList.contains("active")
          ? "fas fa-times"
          : "fas fa-bars";
      }
    });

    // Close sidebar when clicking outside
    document.addEventListener("click", (e) => {
      if (
        !sidebar.contains(e.target) &&
        !toggleBtn.contains(e.target) &&
        sidebar.classList.contains("active")
      ) {
        sidebar.classList.remove("active");
        const icon = toggleBtn.querySelector("i");
        if (icon) {
          icon.className = "fas fa-bars";
        }
      }
    });

    // Highlight active section in sidebar
    const sections = document.querySelectorAll("[id]");
    const navLinks = sidebar.querySelectorAll('a[href^="#"]');

    window.addEventListener("scroll", () => {
      let current = "";

      sections.forEach((section) => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (window.pageYOffset >= sectionTop - 100) {
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

    // Ctrl/Cmd + K: Focus search (if exists)
    if ((e.ctrlKey || e.metaKey) && e.key === "k") {
      e.preventDefault();
      const searchInput = document.querySelector(".search-input");
      if (searchInput) searchInput.focus();
    }

    // Escape: Close sidebar
    if (e.key === "Escape") {
      const sidebar = document.querySelector(".sidebar");
      if (sidebar && sidebar.classList.contains("active")) {
        sidebar.classList.remove("active");
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
// Search Functionality (if search box exists)
// ========================================
function initializeSearch() {
  const searchInput = document.querySelector(".search-input");
  const searchableItems = document.querySelectorAll(
    ".course-card, .searchable-item"
  );

  if (searchInput && searchableItems.length > 0) {
    searchInput.addEventListener("input", (e) => {
      const searchTerm = e.target.value.toLowerCase();

      searchableItems.forEach((item) => {
        const text = item.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
          item.style.display = "";
        } else {
          item.style.display = "none";
        }
      });
    });
  }
}

// ========================================
// Animation Observers
// ========================================
const observeAnimations = () => {
  const animatedElements = document.querySelectorAll(".course-card");

  if (animatedElements.length === 0) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.style.opacity = "1";
            entry.target.style.transform = "translateY(0)";
          }, index * 100);
        }
      });
    },
    {
      threshold: 0.1,
    }
  );

  animatedElements.forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(20px)";
    el.style.transition = "opacity 0.5s ease, transform 0.5s ease";
    observer.observe(el);
  });
};

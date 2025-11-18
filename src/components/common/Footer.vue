<script setup lang="ts">
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-content">
        <div class="footer-grid">
          <!-- Company Info -->
          <div class="footer-section">
            <h3>First AI Journey (FCAJ)</h3>
            <p>Designed for Students</p>
            <p>Community Powered: AWS Study Groups & University Clubs. </p>
            <p>Hands-On Focus: Real-world labs, not just textbooks.</p>
            <p>Career Ready: Build the tech and soft skills to land your first job.</p>
          </div>

          <!-- Quick Links -->
          <div class="footer-section">
            <h3>Quick Links</h3>
            <ul class="footer-links">
              <li><a href="https://awsstudygroup.com/">About AWS Study Group</a></li>
              <li><a href="https://cloudjourney.awsstudygroup.com/">About FCAJ</a></li>
              <li><a href="https://aws.amazon.com/blogs">AWS Blog (English)</a></li>
              <li><a href="https://awsstudygroup.com/category/aws-blogs/">AWS Blog (Vietnamese)</a></li>
            </ul>
          </div>

          <!-- Support -->
          <div class="footer-section">
            <h3>Support</h3>
            <ul class="footer-links">
              <li><a href="https://docs.aws.amazon.com/">AWS Documentation</a></li>
              <li><a href="/faq">FAQ</a></li>
              <li><a href="/contact-us">Contact Support</a></li>
              <li><a href="https://fcj-pagoda-website.vercel.app/">Mediation Hub</a></li>
            </ul>
          </div>
        </div>

        <div class="footer-bottom">
          <p>&copy; {{ currentYear }} FCAJ. All rights reserved.</p>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: var(--color-gray-light);
  padding: var(--spacing-xl) var(--spacing-lg);
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
}

.footer-content {
  background: var(--color-primary-navy);
  color: var(--color-white);
  border-radius: 24px; /* Rounded corners like AWS */
  padding: var(--spacing-xl) var(--spacing-lg) var(--spacing-md);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(20px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.footer-section h3 {
  font-size: var(--font-size-h3);
  margin-bottom: var(--spacing-md);
  color: var(--color-accent-orange);
}

.footer-section p {
  margin-bottom: var(--spacing-xs);
  color: var(--color-gray-medium);
  font-size: 14px;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: var(--spacing-xs);
}

.footer-links a {
  color: var(--color-gray-medium);
  text-decoration: none;
  transition: all var(--transition-fast);
  display: inline-block;
  font-size: 14px;
}

.footer-links a:hover {
  color: var(--color-accent-orange);
  transform: translateX(4px);
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: var(--spacing-md);
  text-align: center;
  color: var(--color-gray-medium);
  font-size: 14px;
}

@media (max-width: 768px) {
  .footer {
    padding: var(--spacing-lg) var(--spacing-md);
  }

  .footer-content {
    border-radius: 16px;
    padding: var(--spacing-lg) var(--spacing-md) var(--spacing-sm);
  }

  .footer-grid {
    grid-template-columns: 1fr;
  }
}
</style>
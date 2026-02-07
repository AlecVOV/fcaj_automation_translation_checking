<template>
  <div class="contact-page">
    <section class="hero fade-in">
      <div class="hero-background">
        <div class="animated-gradient"></div>
      </div>
      <div class="hero-content">
        <h1 class="hero-title">Meet Our Team</h1>
        <p class="hero-subtitle">Get to know the developers behind FCAJ Translation Validator</p>
        <p class="hero-hint">📜 Scroll up to meet each team member</p>
      </div>
    </section>

    <!-- Team Section -->
    <section class="team-section">
      <div class="container">
        <!-- Sticky Stacking Cards (reversed order) -->
        <div class="sticky-cards-container">
          <div
            v-for="(member, index) in [...teamMembers].reverse()"
            :key="member.id"
            class="sticky-card-wrapper"
            :style="{ '--card-index': index, '--total-cards': teamMembers.length }"
          >
            <div class="sticky-card">
              <div class="card-number">
                {{ String(teamMembers.length - index).padStart(2, '0') }}
              </div>
              <div class="member-content">
                <div class="member-image">
                  <img :src="member.image" :alt="member.name" />
                </div>
                <div class="member-info">
                  <h3 class="member-name">{{ member.name }}</h3>
                  <div class="member-role">{{ member.role }}</div>
                  <div class="member-education">
                    <strong>School:</strong> {{ member.school }}<br />
                    <strong>Major:</strong> {{ member.major }}
                  </div>
                  <div class="member-company" v-if="member.company">
                    <strong>Company:</strong> {{ member.company }}
                  </div>
                  <p class="member-description">{{ member.description }}</p>
                  <div class="member-contribution">
                    <strong>Contribution:</strong> {{ member.contribution }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Contact Info Card -->
        <div class="contact-info-card">
          <div class="contact-icon">📧</div>
          <h2>Get in Touch</h2>
          <p>Have questions or want to collaborate? Feel free to reach out to us!</p>
          <a href="mailto:contact@fcaj.vn" class="btn-primary">Email Us</a>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
interface TeamMember {
  id: number
  name: string
  image: string
  school: string
  major: string
  role: string
  company?: string
  description: string
  contribution: string
}

const teamMembers: TeamMember[] = [
  {
    id: 1,
    name: 'Le Hoang Triet Thong',
    image: 'https://res.cloudinary.com/dtv3ad4kv/image/upload/v1770455219/chilonthon_ebjymm.jpg',
    school: 'Swinburne University of Technology (Swinburne Vietnam)',
    major: 'Artificial Intelligence',
    role: 'AI/ML Ambassador',
    company: 'AWS Study Group',
    description:
      'Passionate about building  web interface and AI-powered solutions. Have experience in Vue.js for buiding web application and AWS services.',
    contribution: 'Frontend Architecture, UI/UX Design, Prompt Engineering, Project Management',
  },
  {
    id: 2,
    name: 'Nguyen Binh Ca',
    image: 'https://res.cloudinary.com/dtv3ad4kv/image/upload/v1770455219/nguyenbinhca_qlcctf.jpg',
    school: 'Swinburne University of Technology (Swinburne Vietnam)',
    major: 'Software Development',
    role: 'Cloud Engineer Ambassador',
    company: 'AWS Study Group',
    description:
      'Passionate about building cloud architecture to solve business problem. Have some experience in some compute, network, storage, and serverless AWS services along with basic knowledge for front-end and back-end web development',
    contribution: 'Solution Architect, Backend Logic',
  },
  {
    id: 3,
    name: 'Phan Nguyen Quoc Viet',
    image:
      'https://res.cloudinary.com/dtv3ad4kv/image/upload/v1770455219/phannguyenquocviet_q8xad6.jpg',
    school: 'Swinburne University of Technology (Swinburne Vietnam)',
    major: 'Software Development',
    role: 'Web Security Engineer',
    company: 'AWS Study Group',
    description:
      'Passionate about enhancing web security. Experienced in identifying vulnerabilities and implementing secure authentication systems.',
    contribution: 'Web Security Analysis, Vulnerability Assessment, Secure Authentication Design.',
  },
  {
    id: 4,
    name: 'Nguyen Ha Thuy Trang',
    image:
      'https://res.cloudinary.com/dtv3ad4kv/image/upload/v1770455219/nguyenhathuytrang_wneuhx.jpg',
    school: 'Swinburne University of Technology (Swinburne Vietnam)',
    major: 'Software Development',
    role: 'Backend Developer',
    company: 'N/A',
    description:
      'Enthusiastic about building robust, scalable backend systems. Experienced with React.js for building modern UIs and authentication.',
    contribution: 'Prompt Engineering, Data Cleaning, UI/UX Design, Authentication System.',
  },
  {
    id: 5,
    name: 'Phan Truong Thinh',
    image:
      'https://res.cloudinary.com/dtv3ad4kv/image/upload/v1770455221/phantruongthinh_uupwat.jpg',
    school: 'Swinburne University of Technology (Swinburne Vietnam)',
    major: 'Software Development',
    role: 'Analytics Engineer',
    company: 'N/A',
    description:
      'Enthusiastic about building scalable backend systems. Experienced with React.js for building modern UIs and authentication',
    contribution: 'Dashboard Analytics, Data Visualization, Quality Metrics',
  },
  {
    id: 6,
    name: 'Chung Dung Toan',
    image: 'https://res.cloudinary.com/dtv3ad4kv/image/upload/v1770455218/chungdungtoan_ubujil.jpg',
    school: 'Swinburne University of Technology (Swinburne Vietnam)',
    major: 'Software Development',
    role: 'Analytics Engineer',
    company: 'N/A',
    description:
      'Enthusiastic about building scalable backend systems. Experienced with React.js for building modern UIs and authentication',
    contribution: 'Dashboard Analytics, Data Visualization, Quality Metrics',
  },
]
</script>

<style scoped>
.contact-page {
  min-height: 100vh;
}

/* Hero Section */
.hero {
  position: relative;
  background: var(--color-gray-light);
  color: var(--color-primary-navy);
  padding: var(--spacing-xl) var(--spacing-lg);
  text-align: center;
  overflow: hidden;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.animated-gradient {
  position: absolute;
  top: -15%;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 80%;
  background: radial-gradient(
    rgba(255, 180, 180, 0.6),
    rgba(180, 210, 255, 0.6),
    rgba(255, 220, 180, 0.6),
    rgba(180, 255, 220, 0.6),
    rgba(220, 180, 255, 0.6),
    rgba(255, 255, 180, 0.6),
    rgba(180, 255, 255, 0.6),
    rgba(255, 180, 220, 0.6),
    rgba(220, 255, 180, 0.6),
    rgba(255, 180, 180, 0.6)
  );
  background-size: 400% 400%;
  animation: gradient-shift 10s ease infinite;
  filter: blur(40px);
  opacity: 0.8;
}

@keyframes gradient-shift {
  0% {
    background-position: 0% 50%;
    transform: translateX(-50%) scale(1);
  }
  25% {
    background-position: 100% 50%;
    transform: translateX(-50%) scale(1.1);
  }
  50% {
    background-position: 100% 100%;
    transform: translateX(-50%) scale(1);
  }
  75% {
    background-position: 0% 100%;
    transform: translateX(-50%) scale(1.1);
  }
  100% {
    background-position: 0% 50%;
    transform: translateX(-50%) scale(1);
  }
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: var(--font-size-h1);
  font-weight: 700;
  margin-bottom: var(--spacing-md);
  color: var(--color-primary-navy);
  text-shadow: 0 2px 8px rgba(255, 255, 255, 0.9);
}

.hero-subtitle {
  font-size: 20px;
  color: var(--color-gray-dark);
  max-width: 600px;
  margin: 0 auto;
  font-weight: 400;
  text-shadow: 0 1px 4px rgba(255, 255, 255, 0.8);
}

.hero-hint {
  font-size: 16px;
  color: var(--color-accent-orange);
  font-weight: 600;
  margin-top: var(--spacing-sm);
}

/* Team Section */
.team-section {
  padding: var(--spacing-xl) var(--spacing-lg);
  background: var(--color-gray-light);
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

/* Sticky Stacking Cards */
.sticky-cards-container {
  position: relative;
  padding: var(--spacing-lg) 0;
  display: flex;
  flex-direction: column-reverse;
}

.sticky-card-wrapper {
  position: sticky;
  bottom: calc(var(--card-index) * 5px);
  margin-top: var(--spacing-lg);
  transition: all 0.3s ease;
}

.sticky-card {
  background: linear-gradient(135deg, var(--color-white) 0%, #f8f9fa 100%);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  border: 2px solid var(--color-accent-orange);
  position: relative;
  overflow: hidden;
  transform-origin: bottom center;
  transition: all 0.3s ease;
}

.sticky-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: linear-gradient(90deg, var(--color-accent-orange), #e67e22);
}

.sticky-card:hover {
  transform: translateY(5px);
  box-shadow: 0 15px 50px rgba(255, 127, 0, 0.2);
}

.card-number {
  position: absolute;
  top: var(--spacing-lg);
  right: var(--spacing-lg);
  font-size: 48px;
  font-weight: 700;
  color: var(--color-accent-orange);
  opacity: 0.1;
  line-height: 1;
}

/* Member Content */
.member-content {
  display: flex;
  gap: var(--spacing-xl);
  align-items: flex-start;
}

.member-image {
  flex-shrink: 0;
  width: 200px;
  height: 200px;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.member-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.member-info {
  flex: 1;
}

.member-name {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-primary-navy);
  margin-bottom: var(--spacing-xs);
}

.member-role {
  display: inline-block;
  padding: 6px 16px;
  background: var(--color-accent-orange);
  color: var(--color-white);
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 600;
  margin-bottom: var(--spacing-md);
}

.member-education,
.member-company {
  font-size: 15px;
  line-height: 1.8;
  color: #555;
}

.member-description {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  margin: var(--spacing-md) 0;
}

.member-contribution {
  font-size: 15px;
  line-height: 1.8;
  color: #555;
  padding: var(--spacing-sm);
  background: rgba(255, 127, 0, 0.05);
  border-left: 3px solid var(--color-accent-orange);
  border-radius: var(--radius-sm);
}

/* Contact Info Card */
.contact-info-card {
  background: var(--color-primary-navy);
  color: var(--color-white);
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  box-shadow: 0 8px 30px rgba(255, 127, 0, 0.3);
  text-align: center;
  margin-bottom: var(--spacing-xl);
  position: relative;
  z-index: 1;
}

.contact-icon {
  font-size: 64px;
  margin-bottom: var(--spacing-md);
  animation: wave 1.5s infinite;
}

@keyframes wave {
  0%,
  100% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(-15deg);
  }
  75% {
    transform: rotate(15deg);
  }
}

.contact-info-card h2 {
  font-size: var(--font-size-h2);
  color: var(--color-white);
  margin-bottom: var(--spacing-md);
  font-weight: 700;
}

.contact-info-card p {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: var(--spacing-lg);
  font-size: 18px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.btn-primary {
  display: inline-block;
  background: var(--color-white);
  color: var(--color-accent-orange);
  padding: var(--spacing-sm) var(--spacing-xl);
  font-size: 18px;
  font-weight: 700;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  text-decoration: none;
}

.btn-primary:hover {
  background: var(--color-accent-orange);
  color: var(--color-white);
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 32px;
  }

  .hero-subtitle {
    font-size: 16px;
  }

  .hero-hint {
    font-size: 14px;
  }

  .sticky-card-wrapper {
    bottom: calc(var(--card-index) * 20px);
  }

  .sticky-card {
    padding: var(--spacing-lg);
  }

  .card-number {
    font-size: 32px;
    top: var(--spacing-md);
    right: var(--spacing-md);
  }

  .member-content {
    flex-direction: column;
    align-items: center;
  }

  .member-image {
    width: 150px;
    height: 150px;
  }

  .member-info {
    text-align: center;
  }

  .member-name {
    font-size: 24px;
  }

  .contact-icon {
    font-size: 48px;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .container {
    max-width: 800px;
  }

  .member-image {
    width: 150px;
    height: 150px;
  }
}
</style>

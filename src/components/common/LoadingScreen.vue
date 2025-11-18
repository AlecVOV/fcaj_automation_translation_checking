<template>
  <div class="loading-screen">
    <div class="aws-glow"></div>
    <div class="content">
      <img src="/LOGO_AWS_FACJ.png" alt="FCAJ AWS Logo" class="logo" />
      <p class="message">Initializing AWS translation workspace...</p>
      <div class="loading-track">
        <div class="loading-fill"></div>
        <img src="/bus.svg" alt="AWS Bus" class="bus-icon" />
      </div>
      <span class="timer">Journey on Cloud Computing with AWS</span>
    </div>
  </div>
</template>

<style scoped>
.loading-screen {
  min-height: 100vh;
  background: linear-gradient(135deg, #4979b2, #1f2a37 40%, #3475c4);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
  color: var(--color-white);
}
.aws-glow {
  position: absolute;
  width: 160%;
  height: 160%;
  background: radial-gradient(circle at center, rgb(255, 255, 255), transparent 60%);
  filter: blur(40px);
  animation: pulse 2000ms ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(0.95); opacity: 0.8; }
  50% { transform: scale(1.05); opacity: 1; }
}
.content {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  background: var(--color-primary-navy, #232F3E);
  box-shadow: var(--shadow-card);
  width: min(640px, 120vw);
}
.logo {
  width: 180px;
  margin-bottom: var(--spacing-md);
}
.message {
  font-size: 18px;
  margin-bottom: var(--spacing-lg);
}
.loading-track {
  position: relative;
  height: 18px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 999px;
  overflow: hidden;
  margin-top: var(--spacing-md);
}
.bus-icon {
  position: absolute;
  bottom: calc(100% + 12px);
  width: 48px;
  transform: translateX(-50%);
  animation: drive 3s linear forwards;
  filter: drop-shadow(0 6px 8px rgba(0, 0, 0, 0.4));
}
.loading-fill {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, #ff9900, #ec7211);
  border-radius: inherit;
  transform-origin: left;
  animation: fill-bar 2s ease forwards;
}
@keyframes fill-bar {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
@keyframes drive {
  from { left: 5%; }
  to { left: 95%; }
}
.timer {
  display: block;
  margin-top: var(--spacing-sm);
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
}
</style>
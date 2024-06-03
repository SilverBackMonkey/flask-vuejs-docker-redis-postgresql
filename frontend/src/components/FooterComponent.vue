<template>
  <footer>
    <div class="footer-top">
      <div class="footer-section footer-section__logo">
        <div class="footer-logotype">
          <img src="@/assets/logo.svg" alt="TopFunds">
        </div>
        <div class="footer-copyright">
          <p>
            TopFunds — tools and community
            of fundamental investors
          </p>
        </div>
      </div>
      <div class="footer-section footer-section__contacts">
        <span>Contact</span>
        <a href="mailto:topfunds@gmail.com">topfunds@gmail.com</a>
      </div>
      <div class="footer-section footer-section__address">
        <span>Address</span>
        <p>Heswall, BOURNEMOUTH, BH1 1AA, UK</p>
      </div>
      <div class="footer-section footer-section__social">
        <a href="#" class="footer-social">
          <img src="@/assets/icons/facebook.svg" alt="Facebook">
        </a>
        <a href="#" class="footer-social">
          <img src="@/assets/icons/twitter.svg" alt="Twitter">
        </a>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="footer-section footer-section__logo">
        <div class="footer-logotype">
          <img src="@/assets/icons/sp_global.svg" alt="S&P Global">
        </div>
        <div class="footer-copyright">
          <p>Historical data provided by S&P Global Market Intelligence</p>
        </div>
      </div>
      <div class="footer-section footer-section__terms">
        <a href="#">Terms of service</a>
      </div>
      <div class="footer-section footer-section__terms">
        <a href="#">Disclaimer</a>
      </div>
    </div>
  </footer>
</template>

<style>
footer {
  margin-top: 40px;
}

.footer-top {
  display: flex;
  background: var(--theme-text-color);
  padding: var(--theme-vertical-padding) var(--theme-horizontal-padding);
}

.footer-top .footer-logotype {
  height: 20px;
}

.footer-top .footer-section {
  display: flex;
  align-items: center;
  color: var(--theme-text-color-contrast);
}

.footer-top .footer-section span {
  color: var(--theme-text-gray-3);
  font-size: 12px;
  font-weight: 600;
}

.footer-top .footer-section p,
.footer-top .footer-section a {
  font-size: 14px;
  font-weight: 600;
  color: inherit;
  text-decoration: none;
}

.footer-top .footer-section.footer-section__logo {
  flex: 1;
}

.footer-top .footer-section.footer-section__logo > .footer-logotype {
  padding-right: 31px;
  border-right: 1px solid var(--theme-text-color-contrast);
}

.footer-top .footer-section.footer-section__logo > .footer-copyright {
  max-width: 225px;
  padding-left: 32px;
}

.footer-top .footer-section.footer-section__logo p {
  font-weight: 600;
  font-size: 12px;
  line-height: 18px;
}

.footer-top .footer-section.footer-section__contacts,
.footer-top .footer-section.footer-section__address {
  flex: .6;
  align-items: flex-start;
  flex-direction: column;
}

.footer-top .footer-section.footer-section__social {
  gap: 16px;
}

.footer-top .footer-social {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--theme-text-color-contrast);
}

.footer-bottom {
  display: flex;
  background: var(--theme-text-color-2);
  padding: var(--theme-vertical-padding) var(--theme-horizontal-padding);
}

.footer-bottom .footer-section {
  display: flex;
  color: var(--theme-text-gray-3);
}

.footer-bottom .footer-section.footer-section__logo {
  flex: 1;
  gap: 36px;
  font-size: 12px;
  font-weight: 600;
}

.footer-bottom .footer-section.footer-section__terms {
  flex: .6;
}

.footer-bottom .footer-section.footer-section__terms a {
  color: inherit;
  text-decoration: none;
  font-size: 12px;
  font-weight: 600;
}
</style>

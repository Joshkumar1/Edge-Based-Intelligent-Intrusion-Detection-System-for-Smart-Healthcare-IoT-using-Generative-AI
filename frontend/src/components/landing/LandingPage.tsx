import React from 'react';
import { LandingNavbar } from './LandingNavbar';
import { Section01Hero } from './Section01Hero';
import { Section02TrustIndicators } from './Section02TrustIndicators';
import { Section03WhyEdgeShield } from './Section03WhyEdgeShield';
import { Section04HowItWorks } from './Section04HowItWorks';
import { Section05Architecture } from './Section05Architecture';
import { Section06AttackSandbox } from './Section06AttackSandbox';
import { Section07AIExplainerShowcase } from './Section07AIExplainerShowcase';
import { Section08AnalyticsPreview } from './Section08AnalyticsPreview';
import { Section09Research } from './Section09Research';
import { Section10TechStack } from './Section10TechStack';
import { Section11Testimonials } from './Section11Testimonials';
import { Section12CTA } from './Section12CTA';
import { LandingFooter } from './LandingFooter';

interface LandingPageProps {
  onLaunchDashboard: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onLaunchDashboard }) => {
  return (
    <div className="min-h-screen bg-background text-foreground selection:bg-medical-teal selection:text-white">
      {/* Sticky Landing Navbar */}
      <LandingNavbar onLaunchDashboard={onLaunchDashboard} />

      {/* Section 1: Hero */}
      <Section01Hero onLaunchDashboard={onLaunchDashboard} />

      {/* Section 2: Trust Indicators */}
      <Section02TrustIndicators />

      {/* Section 3: Why EdgeShield AI */}
      <Section03WhyEdgeShield />

      {/* Section 4: How It Works */}
      <Section04HowItWorks />

      {/* Section 5: Interactive Architecture */}
      <Section05Architecture />

      {/* Section 6: Attack Demonstration Sandbox */}
      <Section06AttackSandbox />

      {/* Section 7: Generative AI Showcase */}
      <Section07AIExplainerShowcase />

      {/* Section 8: Analytics Preview */}
      <Section08AnalyticsPreview />

      {/* Section 9: IEEE Research Highlights */}
      <Section09Research />

      {/* Section 10: Technology Stack */}
      <Section10TechStack />

      {/* Section 11: Testimonials */}
      <Section11Testimonials />

      {/* Section 12: Call to Action */}
      <Section12CTA onLaunchDashboard={onLaunchDashboard} />

      {/* Section 13: Footer */}
      <LandingFooter />
    </div>
  );
};

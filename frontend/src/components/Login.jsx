import React, { useState } from 'react';
import { ArrowRight, Camera, CheckCircle2, Flame, Sparkles } from 'lucide-react';
import { loginWithGoogle } from '../services/auth';

export default function Login() {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async () => {
    setBusy(true);
    setError('');
    try {
      await loginWithGoogle();
    } catch (err) {
      console.error(err);
      setError('Google sign-in was cancelled or could not start. Please try again.');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="landing">
      <div className="landing-glow glow-one" />
      <div className="landing-glow glow-two" />

      <div className="landing-shell">
        <section className="landing-copy">
          <div className="landing-brand"><span><Flame /></span> Calorify</div>
          <div className="eyebrow"><Sparkles /> AI-POWERED NUTRITION TRACKING</div>
          <h1>Eat smarter.<br /><span>Feel better.</span></h1>
          <p className="hero-text">
            Turn everyday meals into clear nutrition insights. Snap a photo or type what you ate,
            and let Cali estimate your calories and macros.
          </p>

          <div className="feature-list">
            <div><CheckCircle2 /> AI food calorie estimates</div>
            <div><CheckCircle2 /> Simple daily food diary</div>
            <div><CheckCircle2 /> Water and nutrition tracking</div>
          </div>

          <div className="hero-mini-card">
            <div className="mini-icon"><Camera /></div>
            <div><b>Meet Cali</b><small>Your personal AI nutrition assistant</small></div>
            <ArrowRight />
          </div>
        </section>

        <section className="login-card landing-login">
          <div className="logo"><Flame /></div>
          <small className="login-label">WELCOME TO CALORIFY</small>
          <h2>Your nutrition,<br /><span>made simple.</span></h2>
          <p>Sign in to start tracking your meals, calories and hydration in one place.</p>
          <button className="google-button" onClick={handleLogin} disabled={busy}>
            {busy ? 'Opening Google...' : 'Continue with Google'}
            {!busy && <ArrowRight />}
          </button>
          {error && <div className="login-error">{error}</div>}
          <em>Your data is linked to your Google account. AI estimates are informational.</em>
        </section>
      </div>
    </div>
  );
}

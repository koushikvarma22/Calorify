import React from 'react';
import { Flame } from 'lucide-react';
import { loginWithGoogle } from '../services/auth';

export default function Login() {
  return (
    <div className="login">
      <div className="login-card">
        <div className="logo"><Flame /></div>
        <small>CALORIFY • AI NUTRITION</small>
        <h1>Eat. Track.<br /><span>Improve.</span></h1>
        <p>Track meals, calories and nutrition with Cali, your AI nutrition assistant.</p>
        <button className="primary full" onClick={loginWithGoogle}>
          Continue with Google
        </button>
        <em>AI food estimates are informational.</em>
      </div>
    </div>
  );
}

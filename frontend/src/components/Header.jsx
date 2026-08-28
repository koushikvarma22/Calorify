import React from 'react';
import { Flame, LogOut } from 'lucide-react';
import { logoutUser } from '../services/auth';

export default function Header({ tab, setTab }) {
  const navItems = [
    ['dashboard', 'Dashboard'],
    ['diary', 'Food Diary'],
    ['scanner', 'AI Scanner'],
  ];

  return (
    <header className="app-header">
      <div className="brand">
        <div className="brand-sm"><Flame /></div>
        <b>Calor<span>ify</span></b>
      </div>
      <nav className="header-nav">
        {navItems.map(([id, label]) => (
          <button
            key={id}
            className={tab === id ? 'active' : ''}
            onClick={() => setTab(id)}
          >
            {label}
          </button>
        ))}
      </nav>
      <button className="logout" onClick={logoutUser} title="Sign Out">
        <LogOut />
      </button>
    </header>
  );
}

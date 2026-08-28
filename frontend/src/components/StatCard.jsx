import React from 'react';

export default function StatCard({ icon, title, value, buttonLabel, onIncrement }) {
  return (
    <div className="card stat">
      <div className="stat-icon">{icon}</div>
      <small>{title}</small>
      <strong>{value}</strong>
      <button onClick={onIncrement}>{buttonLabel}</button>
    </div>
  );
}

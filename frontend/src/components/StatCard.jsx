import React from 'react';

export default function StatCard({ icon, title, value, buttonLabel, onIncrement, secondaryLabel, onDecrement }) {
  return (
    <div className="card stat">
      <div className="stat-icon">{icon}</div>
      <small>{title}</small>
      <strong>{value}</strong>
      <div className="stat-actions">
        {onDecrement && <button onClick={onDecrement} aria-label={`Decrease ${title}`}>{secondaryLabel || '−'}</button>}
        <button onClick={onIncrement} aria-label={`Increase ${title}`}>{buttonLabel}</button>
      </div>
    </div>
  );
}

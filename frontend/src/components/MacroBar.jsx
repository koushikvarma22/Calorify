import React from 'react';

export default function MacroBar({ name, value, target = 150 }) {
  const percentage = Math.min(100, Math.round((value / target) * 100));

  return (
    <div className="macro card">
      <span>{name}</span>
      <b>{Math.round(value)} g</b>
      <i>
        <u style={{ width: `${percentage}%` }} />
      </i>
    </div>
  );
}

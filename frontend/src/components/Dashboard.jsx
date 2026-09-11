import React from 'react';
import { Camera, Droplets } from 'lucide-react';
import StatCard from './StatCard';
import MacroBar from './MacroBar';
import FoodList from './FoodList';

export default function DashboardView({ user, summary, foods, onDeleteFood, onLogWater, setTab }) {
  const percentage = Math.min(100, (summary.calories / summary.goal) * 100);
  const remaining = Math.max(0, summary.goal - summary.calories).toFixed(0);

  return (
    <>
      <div className="intro">
        <div>
          <small>TODAY • YOUR NUTRITION</small>
          <h2>Hello, {user.displayName?.split(' ')[0] || 'there'} 👋</h2>
          <p>Let's keep your nutrition on track.</p>
        </div>
        <button className="primary" onClick={() => setTab('scanner')}>
          <Camera /> Scan food
        </button>
      </div>

      <section className="cards">
        <div className="card calories">
          <div className="circle" style={{ '--pct': `${percentage}%` }}>
            <div>
              <strong>{Math.round(summary.calories)}</strong>
              <span>/{summary.goal} kcal</span>
            </div>
          </div>
          <div>
            <small>DAILY CALORIES</small>
            <h3>{remaining} kcal remaining</h3>
            <p>Keep going — every meal counts.</p>
          </div>
        </div>

        <StatCard
          icon={<Droplets />}
          title="Water"
          value={`${(summary.water_ml / 1000).toFixed(1)} L`}
          buttonLabel="+250 ml"
          secondaryLabel="−250 ml"
          onIncrement={() => onLogWater(summary.water_ml + 250)}
          onDecrement={() => onLogWater(Math.max(0, summary.water_ml - 250))}
        />
      </section>

      <div className="macros">
        <MacroBar name="Protein" value={summary.protein} target={120} />
        <MacroBar name="Carbs" value={summary.carbs} target={250} />
        <MacroBar name="Fat" value={summary.fat} target={70} />
      </div>

      <FoodList foods={foods} onDelete={onDeleteFood} />
    </>
  );
}

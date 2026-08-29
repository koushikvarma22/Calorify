import React from 'react';
import { Trash2 } from 'lucide-react';

export default function FoodList({ foods = [], onDelete, title = "Today's meals" }) {
  return (
    <section className="food-section">
      <small>FOOD DIARY</small>
      <h3>{title}</h3>
      {foods.length ? (
        foods.map((item) => (
          <div className="food card" key={item.id}>
            <div className="food-icon">🍽️</div>
            <div className="food-info">
              <b>{item.food_name}</b>
              <small>
                {item.meal} · {new Date(item.consumed_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </small>
            </div>
            <strong>
              {Math.round(item.calories)} <small>kcal</small>
            </strong>
            <button className="delete" onClick={() => onDelete(item.id)} title="Delete Meal">
              <Trash2 />
            </button>
          </div>
        ))
      ) : (
        <div className="empty">No meals logged yet. Add your first meal ✨</div>
      )}
    </section>
  );
}

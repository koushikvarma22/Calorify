import React, { useEffect, useState } from 'react';
import { Flame } from 'lucide-react';
import { subscribeToAuth } from './services/auth';
import api from './services/api';
import Header from './components/Header';
import Login from './components/Login';
import DashboardView from './components/Dashboard';
import FoodList from './components/FoodList';
import FoodScanner from './components/FoodScanner';
import './styles.css';

const initialSummary = { calories: 0, goal: 2000, protein: 0, carbs: 0, fat: 0, water_ml: 0, exercise_minutes: 0 };

function App() {
  const [user, setUser] = useState(undefined);
  const [tab, setTab] = useState('dashboard');
  const [foods, setFoods] = useState([]);
  const [summary, setSummary] = useState(initialSummary);

  useEffect(() => subscribeToAuth(setUser), []);

  const loadData = async (uid) => {
    try {
      const [sumRes, foodsRes] = await Promise.all([
        api.get(`/summary/${uid}`),
        api.get(`/foods/${uid}`),
      ]);
      setSummary(sumRes.data);
      setFoods(foodsRes.data);
      return true;
    } catch (err) {
      console.error('Failed to load user data:', err);
      return false;
    }
  };

  useEffect(() => {
    if (!user) return;
    const syncUser = async () => {
      try {
        await api.post('/users', {
          firebase_uid: user.uid,
          name: user.displayName || '',
          email: user.email || '',
        });
        await loadData(user.uid);
      } catch (err) {
        console.error('Could not connect user to Calorify:', err);
        alert(err.response?.data?.error || 'Could not connect to the Calorify server.');
      }
    };
    syncUser();
  }, [user]);

  const handleDeleteFood = async (id) => {
    try {
      await api.delete(`/foods/${id}`);
      if (user) await loadData(user.uid);
    } catch (err) {
      alert(err.response?.data?.error || 'Could not delete this food entry.');
    }
  };

  const handleLogWater = async (water) => {
    if (!user) return;
    try {
      await api.post('/daily-log', {
        firebase_uid: user.uid,
        water_ml: Math.max(0, Number(water) || 0),
      });
      await loadData(user.uid);
    } catch (err) {
      alert(err.response?.data?.error || 'Could not update water intake. Check the Render API connection.');
    }
  };

  if (user === undefined) {
    return <div className="loading"><Flame /><h2>Calorify</h2></div>;
  }

  if (!user) return <Login />;

  return (
    <div className="app">
      <Header tab={tab} setTab={setTab} />
      <main>
        {tab === 'dashboard' && (
          <DashboardView user={user} summary={summary} foods={foods} onDeleteFood={handleDeleteFood} onLogWater={handleLogWater} setTab={setTab} />
        )}
        {tab === 'diary' && <FoodList foods={foods} title="All Logged Meals" onDelete={handleDeleteFood} />}
        {tab === 'scanner' && (
          <FoodScanner uid={user.uid} onSaved={async () => { await loadData(user.uid); setTab('dashboard'); }} />
        )}
      </main>
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);

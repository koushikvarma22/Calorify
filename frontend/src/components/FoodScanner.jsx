import React, { useState } from 'react';
import { Camera, Sparkles, Type } from 'lucide-react';
import api from '../services/api';

export default function FoodScanner({ uid, onSaved }) {
  const [file, setFile] = useState(null);
  const [foodName, setFoodName] = useState('');
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);

  const analyze = async (formData) => {
    setBusy(true);
    setResult(null);
    try {
      const res = await api.post('/analyze-food', formData);
      setResult(res.data);
    } catch (e) {
      alert(e.response?.data?.error || 'Analysis failed. Please try again.');
    } finally {
      setBusy(false);
    }
  };

  const scan = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append('image', file);
    await analyze(formData);
  };

  const estimateByName = async () => {
    const name = foodName.trim();
    if (!name) return;
    const formData = new FormData();
    formData.append('food_name', name);
    await analyze(formData);
  };

  const save = async () => {
    if (!result) return;
    try {
      await api.post('/foods', {
        firebase_uid: uid,
        food_name: result.food_name,
        meal: 'Snack',
        calories: result.estimated_calories,
        protein: result.protein_g,
        carbs: result.carbs_g,
        fat: result.fat_g,
        fiber: result.fiber_g,
      });
      setFile(null);
      setFoodName('');
      setResult(null);
      onSaved();
    } catch (e) {
      alert(e.response?.data?.error || 'Could not save food to diary');
    }
  };

  return (
    <section className="scanner card">
      <small>CALI • AI FOOD SCANNER</small>
      <h2>What did you eat?</h2>
      <p>Upload a food photo or enter the food name and Cali will estimate calories and macros.</p>

      <label className="upload">
        <Camera />
        <b>{file ? file.name : 'Choose a food photo'}</b>
        <span>JPG, PNG or WEBP • Max 10 MB</span>
        <input
          type="file"
          accept="image/jpeg,image/png,image/webp,image/gif"
          onChange={(e) => {
            setFile(e.target.files?.[0] || null);
            setResult(null);
          }}
        />
      </label>

      {file && (
        <button className="primary full" disabled={busy} onClick={scan}>
          {busy ? 'Cali is analyzing...' : 'Analyze photo'} <Sparkles />
        </button>
      )}

      <div className="manual-entry">
        <div className="manual-title"><Type /> <b>Enter food manually</b></div>
        <input
          type="text"
          value={foodName}
          placeholder="e.g. Chicken biryani, 2 rotis, banana"
          onChange={(e) => setFoodName(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && estimateByName()}
        />
        <button className="secondary full" disabled={busy || !foodName.trim()} onClick={estimateByName}>
          {busy ? 'Cali is estimating...' : 'Estimate calories'} <Sparkles />
        </button>
      </div>

      {result && (
        <div className="result">
          <h3>{result.food_name}</h3>
          <div className="result-grid">
            <strong>{result.estimated_calories} <small>kcal</small></strong>
            <span>Protein {result.protein_g}g</span>
            <span>Carbs {result.carbs_g}g</span>
            <span>Fat {result.fat_g}g</span>
          </div>
          <p>{result.portion_note} · Confidence: {result.confidence}</p>
          <button className="primary full" onClick={save}>Save to diary</button>
        </div>
      )}
    </section>
  );
}

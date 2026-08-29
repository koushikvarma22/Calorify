import React, { useState } from 'react';
import { Camera, Sparkles } from 'lucide-react';
import api from '../services/api';

export default function FoodScanner({ uid, onSaved }) {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);

  const scan = async () => {
    if (!file) return;
    setBusy(true);
    const formData = new FormData();
    formData.append('image', file);

    try {
      const res = await api.post('/analyze-food', formData);
      setResult(res.data);
    } catch (e) {
      alert(e.response?.data?.error || 'Analysis failed');
    } finally {
      setBusy(false);
    }
  };

  const save = async () => {
    if (!result) return;
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
    setResult(null);
    onSaved();
  };

  return (
    <section className="scanner card">
      <small>CALI • AI FOOD SCANNER</small>
      <h2>What did you eat?</h2>
      <p>Upload a food photo and Cali will estimate calories and macros.</p>
      
      <label className="upload">
        <Camera />
        <b>{file ? file.name : 'Choose a food photo'}</b>
        <span>JPG, PNG or WEBP</span>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => {
            setFile(e.target.files?.[0] || null);
            setResult(null);
          }}
        />
      </label>

      {file && (
        <button className="primary" disabled={busy} onClick={scan}>
          {busy ? 'Cali is analyzing...' : 'Analyze food'} <Sparkles />
        </button>
      )}

      {result && (
        <div className="result">
          <h3>{result.food_name}</h3>
          <div className="result-grid">
            <strong>
              {result.estimated_calories} <small>kcal</small>
            </strong>
            <span>Protein {result.protein_g}g</span>
            <span>Carbs {result.carbs_g}g</span>
            <span>Fat {result.fat_g}g</span>
          </div>
          <p>{result.portion_note} · Confidence: {result.confidence}</p>
          <button className="primary" onClick={save}>Save to diary</button>
        </div>
      )}
    </section>
  );
}

import { GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged } from 'firebase/auth';
import { auth } from '../firebase';

export const loginWithGoogle = async () => {
  const provider = new GoogleAuthProvider();
  return await signInWithPopup(auth, provider);
};

export const logoutUser = async () => {
  return await signOut(auth);
};

export const subscribeToAuth = (callback) => {
  return onAuthStateChanged(auth, callback);
};

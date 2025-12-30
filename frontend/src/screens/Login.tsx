import React from 'react';
import { useAuth } from '../auth/AuthProvider';

const Login: React.FC = () => {
  const { login, user, loading } = useAuth();

  return (
    <div className="card">
      <h2>Login</h2>
      {loading ? (
        <p>Authentifizierung wird geladen...</p>
      ) : user ? (
        <p>Angemeldet als {user.profile?.email ?? user.profile?.preferred_username ?? 'Nutzer'}.</p>
      ) : (
        <p>Bitte melden Sie sich mit Ihrem OIDC-Anbieter an.</p>
      )}
      <button className="primary" type="button" onClick={() => void login()}>
        OIDC Login starten
      </button>
    </div>
  );
};

export default Login;

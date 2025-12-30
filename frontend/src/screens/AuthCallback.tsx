import React, { useEffect, useState } from 'react';
import { userManager } from '../auth/oidc';

const AuthCallback: React.FC = () => {
  const [status, setStatus] = useState('Authentifizierung wird abgeschlossen...');

  useEffect(() => {
    const finalizeLogin = async () => {
      try {
        await userManager.signinRedirectCallback();
        setStatus('Login erfolgreich. Sie werden weitergeleitet...');
        window.location.replace('/');
      } catch (error) {
        setStatus('Login fehlgeschlagen. Bitte erneut versuchen.');
      }
    };

    void finalizeLogin();
  }, []);

  return (
    <div className="card">
      <h2>OIDC Callback</h2>
      <p>{status}</p>
    </div>
  );
};

export default AuthCallback;

import React, { useEffect } from 'react';
import { userManager } from '../auth/oidc';

const SilentRenew: React.FC = () => {
  useEffect(() => {
    const renew = async () => {
      try {
        await userManager.signinSilentCallback();
      } catch (error) {
        // Silent renew errors are handled by the OIDC client; no UI needed.
      }
    };

    void renew();
  }, []);

  return <div className="card">Session wird erneuert...</div>;
};

export default SilentRenew;

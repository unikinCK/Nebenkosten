import React from 'react';
import { NavLink, Route, Routes } from 'react-router-dom';
import { useAuth } from './auth/AuthProvider';
import Dashboard from './screens/Dashboard';
import Login from './screens/Login';
import MeterReadings from './screens/MeterReadings';
import Invoices from './screens/Invoices';
import Billing from './screens/Billing';
import Tenants from './screens/Tenants';
import Reports from './screens/Reports';
import AuthCallback from './screens/AuthCallback';
import SilentRenew from './screens/SilentRenew';

const App: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h1>Nebenkosten Portal</h1>
        <nav className="nav-links">
          <NavLink to="/">Dashboard</NavLink>
          <NavLink to="/zaehlerstaende">Zählerstände</NavLink>
          <NavLink to="/rechnungen">Rechnungen</NavLink>
          <NavLink to="/abrechnung">Abrechnung</NavLink>
          <NavLink to="/mieter">Mieter</NavLink>
          <NavLink to="/reports">Reports</NavLink>
          <NavLink to="/login">Login</NavLink>
        </nav>
      </aside>
      <main className="content">
        <div className="top-bar">
          <div>
            <strong>{user ? `Angemeldet als ${user.profile?.email ?? 'Nutzer'}` : 'Nicht angemeldet'}</strong>
          </div>
          {user ? (
            <button className="secondary" type="button" onClick={() => void logout()}>
              Logout
            </button>
          ) : null}
        </div>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/login" element={<Login />} />
          <Route path="/zaehlerstaende" element={<MeterReadings />} />
          <Route path="/rechnungen" element={<Invoices />} />
          <Route path="/abrechnung" element={<Billing />} />
          <Route path="/mieter" element={<Tenants />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/auth/callback" element={<AuthCallback />} />
          <Route path="/auth/silent-renew" element={<SilentRenew />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;

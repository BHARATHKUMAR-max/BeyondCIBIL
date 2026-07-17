import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import LandingPage from '../pages/common/LandingPage';
import LoginPage from '../pages/auth/LoginPage';
import RegisterPage from '../pages/auth/RegisterPage';
import DashboardPage from '../pages/dashboard/DashboardPage';
import NewPredictionPage from '../pages/prediction/NewPredictionPage';
import PredictionResultPage from '../pages/prediction/PredictionResultPage';
import HistoryPage from '../pages/history/HistoryPage';
import ProfilePage from '../pages/profile/ProfilePage';
import SettingsPage from '../pages/settings/SettingsPage';
import NotFoundPage from '../pages/common/NotFoundPage';
import AboutPage from '../pages/common/AboutPage';
import ContactPage from '../pages/common/ContactPage';
import ConnectBankPage from '../pages/banking/ConnectBankPage';

function App() {
  return (
    <Router>
      <AnimatePresence mode="wait">
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/contact" element={<ContactPage />} />
          
          {/* Protected Routes */}
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/connect-bank" element={<ConnectBankPage />} />
          <Route path="/new-prediction" element={<NewPredictionPage />} />
          <Route path="/predictions" element={<HistoryPage />} />
          <Route path="/predictions/:id" element={<PredictionResultPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/settings" element={<SettingsPage />} />
          
          {/* Legacy Routes */}
          <Route path="/prediction/new" element={<Navigate to="/new-prediction" replace />} />
          <Route path="/prediction/result" element={<Navigate to="/predictions/result" replace />} />
          <Route path="/history" element={<Navigate to="/predictions" replace />} />
          
          {/* 404 Page */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </AnimatePresence>
    </Router>
  );
}

export default App;

import { Link, useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export default function Sidebar({ isOpen = true, onClose }: SidebarProps) {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout } = useAuth();

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/connect-bank', label: 'Connect Bank', icon: '🏦' },
    { path: '/predictions', label: 'History', icon: '📜' },
    { path: '/profile', label: 'Profile', icon: '👤' },
    { path: '/settings', label: 'Settings', icon: '⚙️' },
  ];

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <motion.aside
      initial={{ x: -250 }}
      animate={{ x: isOpen ? 0 : -250 }}
      transition={{ duration: 0.3 }}
      className="fixed left-0 top-0 h-full w-64 bg-white shadow-large z-50 md:relative md:shadow-soft md:z-0"
    >
      <div className="p-6">
        <Link to="/dashboard" className="text-2xl font-bold text-primary-600">
          BEYOND CIBIL
        </Link>
      </div>
      <nav className="mt-6">
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            onClick={onClose}
            className={`flex items-center px-6 py-3 transition-colors ${
              location.pathname === item.path
                ? 'bg-primary-50 text-primary-600 border-r-4 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-primary-600'
            }`}
          >
            <span className="mr-3">{item.icon}</span>
            {item.label}
          </Link>
        ))}
        <button
          onClick={handleLogout}
          className="flex items-center w-full px-6 py-3 text-gray-700 hover:bg-gray-50 hover:text-error-600 transition-colors"
        >
          <span className="mr-3">🚪</span>
          Logout
        </button>
      </nav>
    </motion.aside>
  );
}

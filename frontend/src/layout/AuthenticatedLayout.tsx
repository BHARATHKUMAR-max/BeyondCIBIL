import { Outlet, Link } from 'react-router-dom';
import { motion } from 'framer-motion';

export default function AuthenticatedLayout() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
      className="min-h-screen bg-gray-50"
    >
      {/* Navbar */}
      <nav className="bg-white shadow-soft">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link to="/dashboard" className="text-2xl font-bold text-primary-600">
                BEYOND CIBIL
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                to="/dashboard"
                className="text-gray-700 hover:text-primary-600 transition-colors"
              >
                Dashboard
              </Link>
              <Link
                to="/prediction/new"
                className="text-gray-700 hover:text-primary-600 transition-colors"
              >
                Prediction
              </Link>
              <Link
                to="/history"
                className="text-gray-700 hover:text-primary-600 transition-colors"
              >
                History
              </Link>
              <Link
                to="/profile"
                className="text-gray-700 hover:text-primary-600 transition-colors"
              >
                Profile
              </Link>
              <Link
                to="/settings"
                className="text-gray-700 hover:text-primary-600 transition-colors"
              >
                Settings
              </Link>
              <button className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <Outlet />
    </motion.div>
  );
}

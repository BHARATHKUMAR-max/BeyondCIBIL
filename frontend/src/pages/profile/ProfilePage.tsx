import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import HorizontalNav from '../../layout/HorizontalNav';
import Footer from '../../layout/Footer';
import AnimatedBackground from '../../components/AnimatedBackground';

export default function ProfilePage() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const handleUpdateProfile = (e: React.FormEvent) => {
    e.preventDefault();
    alert('Profile updated successfully!');
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
      className="min-h-screen flex flex-col"
    >
      <AnimatedBackground variant="bubbles" />
      <HorizontalNav />
      
      <div className="flex-1 flex flex-col">
        {/* Top Header */}
        <header className="bg-white dark:bg-gray-800 shadow-sm">
          <div className="px-6 py-4 flex justify-between items-center">
            <h1 className="text-xl font-semibold text-gray-900 dark:text-white">Profile</h1>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-6">
          <div className="max-w-2xl mx-auto space-y-6">
            {/* Profile Card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              whileHover={{ scale: 1.01 }}
              className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft"
            >
              <div className="flex items-center space-x-4 mb-6">
                <div className="w-20 h-20 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center">
                  <span className="text-3xl">👤</span>
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">{user?.full_name || 'John Doe'}</h2>
                  <p className="text-gray-600 dark:text-gray-400">{user?.email || 'john.doe@example.com'}</p>
                </div>
              </div>
              
              <form onSubmit={handleUpdateProfile} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Full Name
                  </label>
                  <input
                    type="text"
                    defaultValue={user?.full_name || 'John Doe'}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    defaultValue={user?.email || 'john.doe@example.com'}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Phone
                  </label>
                  <input
                    type="tel"
                    defaultValue="+91 98765 43210"
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
                <button
                  type="submit"
                  className="w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold"
                >
                  Update Profile
                </button>
              </form>
            </motion.div>

            {/* Account Stats */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="grid grid-cols-2 gap-4"
            >
              <div className="bg-white dark:bg-gray-800 p-4 rounded-2xl shadow-soft text-center cursor-pointer hover:shadow-medium transition-shadow" onClick={() => navigate('/predictions')}>
                <p className="text-2xl font-bold text-primary-600">12</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Predictions</p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-4 rounded-2xl shadow-soft text-center">
                <p className="text-2xl font-bold text-secondary-600">720</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Avg Score</p>
              </div>
            </motion.div>

            {/* Account Actions */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.4 }}
              className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft"
            >
              <h3 className="text-xl font-semibold text-gray-700 dark:text-gray-200 mb-4">Account Actions</h3>
              <div className="space-y-3">
                <button
                  onClick={() => navigate('/settings')}
                  className="w-full py-3 border-2 border-primary-600 text-primary-600 dark:text-primary-400 rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900/30 transition-colors font-semibold"
                >
                  Account Settings
                </button>
                <button
                  className="w-full py-3 border-2 border-error-600 text-error-600 dark:text-error-400 rounded-lg hover:bg-error-50 dark:hover:bg-error-900/30 transition-colors font-semibold"
                >
                  Delete Account
                </button>
              </div>
            </motion.div>
          </div>
        </main>
      </div>
      <Footer />
    </motion.div>
  );
}

import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import HorizontalNav from '../../layout/HorizontalNav';
import Footer from '../../layout/Footer';
import AnimatedBackground from '../../components/AnimatedBackground';

export default function PredictionResultPage() {
  const navigate = useNavigate();

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
      className="min-h-screen flex flex-col"
    >
      <AnimatedBackground variant="stars" />
      <HorizontalNav />
      
      <div className="flex-1 flex flex-col">
        {/* Top Header */}
        <header className="bg-white dark:bg-gray-800 shadow-sm">
          <div className="px-6 py-4 flex justify-between items-center">
            <h1 className="text-xl font-semibold text-gray-900 dark:text-white">Prediction Result</h1>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-6">
          <div className="max-w-4xl mx-auto space-y-6">
            {/* Main Score Card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              whileHover={{ scale: 1.01 }}
              className="bg-gradient-to-r from-primary-600 to-secondary-600 p-8 rounded-2xl shadow-large text-white"
            >
              <div className="text-center">
                <p className="text-lg mb-2">Alternative Credit Score</p>
                <p className="text-6xl font-bold mb-2">720</p>
                <p className="text-xl">Low Risk</p>
              </div>
            </motion.div>

            {/* Details Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.3 }}
                whileHover={{ scale: 1.02 }}
                className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft"
              >
                <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-2">Repayment Probability</h3>
                <p className="text-3xl font-bold text-secondary-600">78%</p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.35 }}
                whileHover={{ scale: 1.02 }}
                className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft"
              >
                <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-2">Confidence Score</h3>
                <p className="text-3xl font-bold text-accent-600">56%</p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.4 }}
                whileHover={{ scale: 1.02 }}
                className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft"
              >
                <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-2">Risk Category</h3>
                <p className="text-3xl font-bold text-success-600">Low Risk</p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.45 }}
                whileHover={{ scale: 1.02 }}
                className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft"
              >
                <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-2">Prediction Time</h3>
                <p className="text-3xl font-bold text-warning-600">45ms</p>
              </motion.div>
            </div>

            {/* SHAP Explanation */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.5 }}
              className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft"
            >
              <h3 className="text-xl font-semibold text-gray-700 dark:text-gray-200 mb-4">SHAP Explanation</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center p-3 bg-success-50 dark:bg-success-900/20 rounded-lg">
                  <span className="text-gray-700 dark:text-gray-300">Average Monthly Income</span>
                  <span className="text-success-600 font-semibold">+0.15</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-success-50 dark:bg-success-900/20 rounded-lg">
                  <span className="text-gray-700 dark:text-gray-300">Savings Ratio</span>
                  <span className="text-success-600 font-semibold">+0.08</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-error-50 dark:bg-error-900/20 rounded-lg">
                  <span className="text-gray-700 dark:text-gray-300">Total Expense</span>
                  <span className="text-error-600 font-semibold">-0.03</span>
                </div>
              </div>
            </motion.div>

            {/* Recommendations */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.6 }}
              className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft"
            >
              <h3 className="text-xl font-semibold text-gray-700 dark:text-gray-200 mb-4">Recommendations</h3>
              <div className="space-y-3">
                <div className="flex items-start space-x-3 p-3 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
                  <span className="text-2xl">💡</span>
                  <p className="text-gray-700 dark:text-gray-300">Maintain stable income patterns to improve creditworthiness</p>
                </div>
                <div className="flex items-start space-x-3 p-3 bg-secondary-50 dark:bg-secondary-900/20 rounded-lg">
                  <span className="text-2xl">📊</span>
                  <p className="text-gray-700 dark:text-gray-300">Monitor and control spending patterns</p>
                </div>
              </div>
            </motion.div>

            {/* Actions */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.7 }}
              className="flex space-x-4"
            >
              <button
                onClick={() => navigate('/new-prediction')}
                className="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold"
              >
                New Prediction
              </button>
              <Link
                to="/predictions"
                className="flex-1 py-3 border-2 border-primary-600 text-primary-600 dark:text-primary-400 rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900/30 transition-colors font-semibold text-center"
              >
                View History
              </Link>
            </motion.div>
          </div>
        </main>
      </div>
      <Footer />
    </motion.div>
  );
}

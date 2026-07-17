import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../../layout/Sidebar';

export default function NewPredictionPage() {
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    navigate('/predictions/result');
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
      className="min-h-screen bg-gray-50 flex"
    >
      <Sidebar />
      
      <div className="flex-1 flex flex-col">
        {/* Top Navigation */}
        <header className="bg-white shadow-soft">
          <div className="px-6 py-4 flex justify-between items-center">
            <h1 className="text-xl font-semibold text-gray-900">New Prediction</h1>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="max-w-2xl mx-auto bg-white p-8 rounded-2xl shadow-soft"
          >
            <h2 className="text-2xl font-bold text-primary-900 mb-6">Generate Credit Score Prediction</h2>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Savings Ratio
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  max="1"
                  required
                  defaultValue="0.45"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="0.45"
                />
                <p className="text-xs text-gray-500 mt-1">Ratio of savings to income (0-1)</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Average Monthly Income
                </label>
                <input
                  type="number"
                  required
                  defaultValue="35000"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="35000"
                />
                <p className="text-xs text-gray-500 mt-1">Monthly income in currency units</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Income Consistency
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  required
                  defaultValue="0.38"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="0.38"
                />
                <p className="text-xs text-gray-500 mt-1">Consistency score (0-1)</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Total Expense
                </label>
                <input
                  type="number"
                  required
                  defaultValue="18000"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="18000"
                />
                <p className="text-xs text-gray-500 mt-1">Monthly expenses in currency units</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Transaction Frequency
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  required
                  defaultValue="0.75"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="0.75"
                />
                <p className="text-xs text-gray-500 mt-1">Transactions per day</p>
              </div>

              <div className="flex space-x-4">
                <button
                  type="submit"
                  className="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold"
                >
                  Generate Prediction
                </button>
                <button
                  type="button"
                  onClick={() => navigate('/dashboard')}
                  className="px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-semibold"
                >
                  Cancel
                </button>
              </div>
            </form>
          </motion.div>
        </main>
      </div>
    </motion.div>
  );
}

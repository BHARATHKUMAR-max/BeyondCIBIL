import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useEffect, useState } from 'react';
import HorizontalNav from '../../layout/HorizontalNav';
import Footer from '../../layout/Footer';
import AnimatedBackground from '../../components/AnimatedBackground';
import type { BankConnectionResponse } from '../../services/api/predictionApi';

export default function DashboardPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [predictionData, setPredictionData] = useState<BankConnectionResponse | null>(null);

  useEffect(() => {
    // Check if we have bank prediction data from the connect bank flow
    const storedData = localStorage.getItem('bankPredictionResult');
    if (storedData) {
      try {
        setPredictionData(JSON.parse(storedData));
      } catch (e) {
        console.error('Failed to parse stored prediction data', e);
      }
    }
  }, []);

  const displayData = predictionData || {
    alternative_credit_score: 720,
    repayment_probability: 78,
    confidence: 56,
    risk_category: 'Low Risk',
    shap_explanation: {
      top_positive_factors: [
        { feature: 'Average Monthly Income', contribution: 0.15, impact: 'positive' },
        { feature: 'Savings Ratio', contribution: 0.08, impact: 'positive' }
      ],
      top_negative_factors: [
        { feature: 'Total Expense', contribution: -0.03, impact: 'negative' }
      ]
    },
    recommendations: [
      'Maintain stable income patterns to improve creditworthiness',
      'Monitor and control spending patterns'
    ],
    customer: {
      monthly_income: 35000,
      total_expense: 18000,
      savings: 17000,
      account_balance: 150000
    },
    transaction_summary: {
      total_transactions: 245,
      total_debit: 216000,
      total_credit: 420000,
      top_spending_category: 'Shopping'
    }
  };

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
            <h1 className="text-xl font-semibold text-gray-900 dark:text-white">Dashboard</h1>
            <div className="flex items-center space-x-4">
              <span className="text-gray-600 dark:text-gray-300">Welcome, {user?.full_name || 'User'}</span>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-6">
          {!predictionData ? (
            // Show Connect Bank CTA when no prediction data
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="flex flex-col items-center justify-center h-full"
            >
              <div className="text-center max-w-4xl">
                <div className="text-8xl mb-6">🏦</div>
                <h2 className="text-3xl font-bold text-primary-900 dark:text-primary-100 mb-4">
                  Connect Your Bank to Get Started
                </h2>
                <p className="text-gray-600 dark:text-gray-400 mb-8 text-lg">
                  Connect your bank account to analyze your financial data and get your alternative credit score.
                </p>
                
                {/* What happens after connecting */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-soft">
                    <div className="text-4xl mb-3">📊</div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Alternative Credit Score</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Get a comprehensive credit score (300-900) based on your banking behavior</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-soft">
                    <div className="text-4xl mb-3">💰</div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Financial Analysis</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">View detailed breakdown of income, expenses, savings, and spending patterns</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-soft">
                    <div className="text-4xl mb-3">🎯</div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Personalized Insights</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Receive AI-powered recommendations to improve your financial health</p>
                  </div>
                </div>

                <Link
                  to="/connect-bank"
                  className="inline-block px-8 py-4 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold text-lg cursor-pointer"
                >
                  Connect Bank Now
                </Link>
                <div className="mt-8 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg inline-block">
                  <p className="text-sm text-blue-800 dark:text-blue-300">
                    🔒 Your data is secure. We use bank-grade encryption to protect your information.
                  </p>
                </div>
              </div>
            </motion.div>
          ) : (
            // Show dashboard with prediction data
            <>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="mb-8"
              >
                <h2 className="text-2xl font-bold text-primary-900 dark:text-primary-100 mb-2">Welcome Back!</h2>
                <p className="text-gray-600 dark:text-gray-400">Here's an overview of your credit health</p>
              </motion.div>

          {/* Main Credit Score Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="bg-gradient-to-r from-primary-600 to-secondary-600 p-8 rounded-2xl shadow-large text-white mb-6"
          >
            <div className="text-center">
              <p className="text-lg mb-2">Alternative Credit Score</p>
              <p className="text-6xl font-bold mb-2">{displayData.alternative_credit_score}</p>
              <p className="text-xl">{displayData.risk_category}</p>
            </div>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
            {/* Repayment Probability */}
            <motion.div
              whileHover={{ scale: 1.02, y: -4 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
              className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft hover:shadow-lg transition-shadow cursor-pointer"
              onClick={() => navigate('/predictions')}
            >
              <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-2">Repayment Probability</h3>
              <p className="text-4xl font-bold text-secondary-600">{displayData.repayment_probability}%</p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">High confidence</p>
            </motion.div>

            {/* Confidence Score */}
            <motion.div
              whileHover={{ scale: 1.02, y: -4 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
              className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft hover:shadow-lg transition-shadow cursor-pointer"
            >
              <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-2">Confidence Score</h3>
              <p className="text-4xl font-bold text-accent-600">{displayData.confidence}%</p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">Model confidence</p>
            </motion.div>

            {/* Account Balance */}
            <motion.div
              whileHover={{ scale: 1.02, y: -4 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
              className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft hover:shadow-lg transition-shadow cursor-pointer"
            >
              <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-2">Account Balance</h3>
              <p className="text-4xl font-bold text-success-600">₹{displayData.customer?.account_balance?.toLocaleString() || '150,000'}</p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">Current balance</p>
            </motion.div>

            {/* Monthly Income */}
            <motion.div
              whileHover={{ scale: 1.02, y: -4 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
              className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft hover:shadow-lg transition-shadow cursor-pointer"
            >
              <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-2">Monthly Income</h3>
              <p className="text-4xl font-bold text-primary-600">₹{displayData.customer?.monthly_income?.toLocaleString() || '35,000'}</p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">Average monthly</p>
            </motion.div>

            {/* Monthly Expenses */}
            <motion.div
              whileHover={{ scale: 1.02, y: -4 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
              className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft hover:shadow-lg transition-shadow cursor-pointer"
            >
              <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-2">Monthly Expenses</h3>
              <p className="text-4xl font-bold text-warning-600">₹{displayData.customer?.total_expense?.toLocaleString() || '18,000'}</p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">Average monthly</p>
            </motion.div>

            {/* Total Transactions */}
            <motion.div
              whileHover={{ scale: 1.02, y: -4 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
              className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft hover:shadow-lg transition-shadow cursor-pointer"
              onClick={() => navigate('/predictions')}
            >
              <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-2">Total Transactions</h3>
              <p className="text-4xl font-bold text-info-600">{displayData.transaction_summary?.total_transactions || 245}</p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">Last 12 months</p>
            </motion.div>
          </div>

          {/* SHAP Explanation */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft mb-6"
          >
            <h3 className="text-xl font-semibold text-gray-700 dark:text-gray-200 mb-4">Key Factors Affecting Your Score</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="text-sm font-medium text-success-600 mb-3">Positive Factors</h4>
                <div className="space-y-2">
                  {(displayData.shap_explanation?.top_positive_factors || []).map((factor: any, index: number) => (
                    <div key={index} className="flex justify-between items-center p-3 bg-success-50 dark:bg-success-900/20 rounded-lg">
                      <span className="text-gray-700 dark:text-gray-300">{factor.feature}</span>
                      <span className="text-success-600 font-semibold">+{Math.abs(factor.contribution).toFixed(2)}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <h4 className="text-sm font-medium text-error-600 mb-3">Negative Factors</h4>
                <div className="space-y-2">
                  {(displayData.shap_explanation?.top_negative_factors || []).map((factor: any, index: number) => (
                    <div key={index} className="flex justify-between items-center p-3 bg-error-50 dark:bg-error-900/20 rounded-lg">
                      <span className="text-gray-700 dark:text-gray-300">{factor.feature}</span>
                      <span className="text-error-600 font-semibold">{factor.contribution.toFixed(2)}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>

          {/* Recommendations */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft mb-6"
          >
            <h3 className="text-xl font-semibold text-gray-700 dark:text-gray-200 mb-4">Recommendations</h3>
            <div className="space-y-3">
              {(displayData.recommendations || []).map((recommendation: string, index: number) => (
                <div key={index} className="flex items-start space-x-3 p-3 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
                  <span className="text-2xl">💡</span>
                  <p className="text-gray-700 dark:text-gray-300">{recommendation}</p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Action Button */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
            className="flex space-x-4"
          >
            <Link
              to="/connect-bank"
              className="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold text-center cursor-pointer"
            >
              Connect New Bank
            </Link>
            <Link
              to="/predictions"
              className="flex-1 py-3 border-2 border-primary-600 text-primary-600 dark:text-primary-400 rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900/30 transition-colors font-semibold text-center cursor-pointer"
            >
              View History
            </Link>
          </motion.div>
            </>
          )}
        </main>
      </div>
      <Footer />
    </motion.div>
  );
}

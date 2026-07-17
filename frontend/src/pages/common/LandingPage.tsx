import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

export default function LandingPage() {
  const scrollToFeatures = () => {
    const featuresSection = document.getElementById('features');
    if (featuresSection) {
      featuresSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
      className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50"
    >
      {/* Navbar */}
      <nav className="bg-white shadow-soft sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link to="/" className="text-2xl font-bold text-primary-600">
                BEYOND CIBIL
              </Link>
            </div>
            <div className="flex items-center space-x-6">
              <Link to="/" className="text-gray-700 hover:text-primary-600 transition-colors">
                Home
              </Link>
              <Link to="/about" className="text-gray-700 hover:text-primary-600 transition-colors">
                About
              </Link>
              <Link to="/contact" className="text-gray-700 hover:text-primary-600 transition-colors">
                Contact
              </Link>
              <Link
                to="/login"
                className="text-gray-700 hover:text-primary-600 transition-colors"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="text-center"
        >
          <h1 className="text-5xl font-bold text-primary-900 mb-4">
            AI-Powered Credit Scoring
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Discover your alternative credit score using advanced machine learning. 
            Beyond traditional credit bureaus, we analyze your financial behavior to provide accurate assessments.
          </p>
          <div className="flex justify-center space-x-4">
            <Link
              to="/login"
              className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold"
            >
              Get Started
            </Link>
            <button
              onClick={scrollToFeatures}
              className="px-6 py-3 border-2 border-primary-600 text-primary-600 rounded-lg hover:bg-primary-50 transition-colors font-semibold"
            >
              Learn More
            </button>
          </div>
        </motion.div>
      </div>

      {/* Features Section */}
      <div id="features" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl font-bold text-primary-900 mb-4">Why Choose BEYOND CIBIL?</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Our AI-powered platform provides accurate credit assessments using advanced machine learning
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              icon: '🤖',
              title: 'AI-Powered Analysis',
              description: 'Advanced machine learning models analyze your financial patterns for accurate predictions'
            },
            {
              icon: '⚡',
              title: 'Instant Results',
              description: 'Get your alternative credit score in seconds, not days'
            },
            {
              icon: '🔍',
              title: 'Transparent Insights',
              description: 'Understand what factors influence your score with SHAP explanations'
            },
            {
              icon: '🔒',
              title: 'Secure & Private',
              description: 'Your financial data is protected with bank-grade security'
            },
            {
              icon: '📊',
              title: 'Detailed Analytics',
              description: 'Comprehensive breakdown of your financial health and risk factors'
            },
            {
              icon: '🎯',
              title: 'Actionable Insights',
              description: 'Get personalized recommendations to improve your creditworthiness'
            }
          ].map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.4 + index * 0.1 }}
              className="bg-white rounded-2xl shadow-soft p-6 text-center"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.8 }}
          className="bg-gradient-to-r from-primary-600 to-secondary-600 rounded-2xl shadow-large p-12 text-center text-white"
        >
          <h2 className="text-3xl font-bold mb-4">Ready to Discover Your Credit Score?</h2>
          <p className="text-lg mb-6 opacity-90">
            Join thousands of users who have already discovered their alternative credit score
          </p>
          <Link
            to="/register"
            className="inline-block px-8 py-3 bg-white text-primary-600 rounded-lg hover:bg-gray-100 transition-colors font-semibold"
          >
            Create Free Account
          </Link>
        </motion.div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-2xl font-bold mb-4 md:mb-0">BEYOND CIBIL</div>
            <div className="flex space-x-6">
              <Link to="/about" className="text-gray-400 hover:text-white transition-colors">
                About
              </Link>
              <Link to="/contact" className="text-gray-400 hover:text-white transition-colors">
                Contact
              </Link>
              <Link to="/login" className="text-gray-400 hover:text-white transition-colors">
                Login
              </Link>
            </div>
          </div>
          <div className="text-center text-gray-400 mt-8">
            © 2026 BEYOND CIBIL. All rights reserved.
          </div>
        </div>
      </footer>
    </motion.div>
  );
}

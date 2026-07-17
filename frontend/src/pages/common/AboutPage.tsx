import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

export default function AboutPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
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
              <Link to="/about" className="text-primary-600 font-semibold">
                About
              </Link>
              <Link to="/contact" className="text-gray-700 hover:text-primary-600 transition-colors">
                Contact
              </Link>
              <Link
                to="/login"
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                Login
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl font-bold text-primary-900 mb-4">
            About BEYOND CIBIL
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Revolutionizing credit assessment with AI-powered alternative credit scoring
          </p>
        </motion.div>

        {/* Mission Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="bg-white rounded-2xl shadow-soft p-8 mb-8"
        >
          <h2 className="text-3xl font-bold text-primary-900 mb-4">Our Mission</h2>
          <p className="text-gray-700 text-lg leading-relaxed">
            At BEYOND CIBIL, we believe that everyone deserves access to fair credit. Our AI-powered
            alternative credit scoring system analyzes financial behavior patterns to provide accurate
            credit assessments for individuals who may not have traditional credit histories. We're
            committed to financial inclusion and empowering underserved communities with the tools
            they need to achieve their financial goals.
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {[
            {
              icon: '🤖',
              title: 'AI-Powered Analysis',
              description: 'Advanced machine learning models analyze financial patterns for accurate predictions'
            },
            {
              icon: '🔒',
              title: 'Secure & Private',
              description: 'Bank-grade security ensures your financial data remains protected'
            },
            {
              icon: '⚡',
              title: 'Instant Results',
              description: 'Get real-time credit assessments in seconds, not days'
            }
          ].map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.4 + index * 0.1 }}
              className="bg-white rounded-2xl shadow-soft p-6"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">{feature.description}</p>
            </motion.div>
          ))}
        </div>

        {/* Technology Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.7 }}
          className="bg-white rounded-2xl shadow-soft p-8 mb-8"
        >
          <h2 className="text-3xl font-bold text-primary-900 mb-4">Our Technology</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Machine Learning</h3>
              <p className="text-gray-600">
                Our XGBoost-based model is trained on diverse financial datasets to identify
                patterns that traditional credit scoring might miss.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">SHAP Explanations</h3>
              <p className="text-gray-600">
                We provide transparent, explainable AI insights so you understand exactly what
                factors influence your credit score.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Real-time Processing</h3>
              <p className="text-gray-600">
                Our optimized pipeline delivers predictions in under 100ms, enabling instant
                credit decisions.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Continuous Learning</h3>
              <p className="text-gray-600">
                Our models are regularly retrained with new data to improve accuracy and adapt
                to changing financial patterns.
              </p>
            </div>
          </div>
        </motion.div>

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.8 }}
          className="text-center"
        >
          <h2 className="text-3xl font-bold text-primary-900 mb-4">Ready to Get Started?</h2>
          <p className="text-gray-600 mb-6">
            Join thousands of users who have already discovered their alternative credit score
          </p>
          <Link
            to="/register"
            className="inline-block px-8 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold"
          >
            Create Free Account
          </Link>
        </motion.div>
      </div>
    </motion.div>
  );
}

import { motion } from 'framer-motion';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import HorizontalNav from '../../layout/HorizontalNav';
import Footer from '../../layout/Footer';
import AnimatedBackground from '../../components/AnimatedBackground';
import { predictionApi, type BankConnectionRequest } from '../../services/api/predictionApi';

const POPULAR_BANKS = [
  "SBI",
  "HDFC",
  "ICICI",
  "Axis",
  "Kotak",
  "Canara",
  "Punjab National Bank",
  "Union Bank",
  "Indian Bank",
  "Bank of Baroda"
];

export default function ConnectBankPage() {
  const navigate = useNavigate();
  const [step, setStep] = useState<'bank' | 'otp' | 'loading'>('bank');
  const [selectedBank, setSelectedBank] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [otp, setOtp] = useState('');
  const [error, setError] = useState('');

  const handleConnectBank = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedBank && phoneNumber.length === 10) {
      setStep('otp');
      setError('');
    }
  };

  const handleVerifyOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('OTP verification started', { otp, phoneNumber, selectedBank });
    
    if (otp.length === 4) {
      setStep('loading');
      setError('');
      
      try {
        const request: BankConnectionRequest = {
          phone_number: phoneNumber,
          bank_name: selectedBank
        };
        
        console.log('Making API request', request);
        const response = await predictionApi.predictFromBank(request);
        console.log('API response received', response);
        
        // Store the result in localStorage for dashboard to use
        localStorage.setItem('bankPredictionResult', JSON.stringify(response));
        console.log('Data stored in localStorage, navigating to dashboard');
        
        navigate('/dashboard');
      } catch (err) {
        console.error('API error:', err);
        setError('Failed to connect bank. Please try again.');
        setStep('otp');
      }
    } else {
      console.log('OTP length invalid:', otp.length);
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
      <AnimatedBackground variant="bubbles" />
      <HorizontalNav />
      
      <div className="flex-1 flex flex-col">
        {/* Top Header */}
        <header className="bg-white dark:bg-gray-800 shadow-sm">
          <div className="px-6 py-4 flex justify-between items-center">
            <h1 className="text-xl font-semibold text-gray-900 dark:text-white">Connect Your Bank</h1>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-6">
          <div className="max-w-2xl mx-auto">
            {/* Bank Selection Step */}
            {step === 'bank' && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-soft"
              >
                <div className="text-center mb-8">
                  <div className="text-6xl mb-4">🏦</div>
                  <h2 className="text-2xl font-bold text-primary-900 dark:text-primary-100 mb-2">
                    Connect Your Bank Account
                  </h2>
                  <p className="text-gray-600 dark:text-gray-400">
                    Select your bank and enter your mobile number to get your credit score
                  </p>
                </div>

                <form onSubmit={handleConnectBank} className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Select Bank
                    </label>
                    <select
                      value={selectedBank}
                      onChange={(e) => setSelectedBank(e.target.value)}
                      required
                      className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    >
                      <option value="">Choose your bank</option>
                      {POPULAR_BANKS.map((bank) => (
                        <option key={bank} value={bank}>
                          {bank}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Mobile Number
                    </label>
                    <input
                      type="tel"
                      value={phoneNumber}
                      onChange={(e) => setPhoneNumber(e.target.value.replace(/\D/g, '').slice(0, 10))}
                      placeholder="Enter 10-digit mobile number"
                      required
                      maxLength={10}
                      className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    />
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      We'll send an OTP to this number for verification
                    </p>
                  </div>

                  <button
                    type="submit"
                    disabled={!selectedBank || phoneNumber.length !== 10}
                    className="w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold disabled:bg-gray-300 disabled:cursor-not-allowed"
                  >
                    Connect Bank
                  </button>
                </form>

                <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <p className="text-sm text-blue-800 dark:text-blue-300">
                    🔒 Your data is secure. We use bank-grade encryption to protect your information.
                  </p>
                </div>

                {error && (
                  <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 rounded-lg">
                    <p className="text-sm text-red-800 dark:text-red-300">{error}</p>
                  </div>
                )}
              </motion.div>
            )}

            {/* OTP Verification Step */}
            {step === 'otp' && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-soft"
              >
                <div className="text-center mb-8">
                  <div className="text-6xl mb-4">📱</div>
                  <h2 className="text-2xl font-bold text-primary-900 dark:text-primary-100 mb-2">
                    Verify Your Mobile Number
                  </h2>
                  <p className="text-gray-600 dark:text-gray-400">
                    We've sent a 4-digit OTP to {phoneNumber}
                  </p>
                </div>

                <form onSubmit={handleVerifyOTP} className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Enter OTP
                    </label>
                    <div className="flex justify-center space-x-2">
                      {[0, 1, 2, 3].map((index) => (
                        <input
                          key={index}
                          type="text"
                          maxLength={1}
                          value={otp[index] || ''}
                          onChange={(e) => {
                            const newOtp = otp.split('');
                            newOtp[index] = e.target.value;
                            setOtp(newOtp.join(''));
                            if (e.target.value && index < 3) {
                              const nextInput = e.target.nextElementSibling as HTMLInputElement;
                              nextInput?.focus();
                            }
                          }}
                          className="w-16 h-16 text-center text-2xl font-bold border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        />
                      ))}
                    </div>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
                      Demo OTP: 1234
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 text-center">
                      Test phone numbers: 9876543210-9876543219
                    </p>
                  </div>

                  <button
                    type="submit"
                    disabled={otp.length !== 4}
                    className="w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold disabled:bg-gray-300 disabled:cursor-not-allowed"
                  >
                    Verify & Get Score
                  </button>

                  <button
                    type="button"
                    onClick={() => setStep('bank')}
                    className="w-full py-3 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors font-semibold"
                  >
                    Change Bank
                  </button>
                </form>
              </motion.div>
            )}

            {/* Loading Step */}
            {step === 'loading' && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
                className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-soft text-center"
              >
                <div className="text-6xl mb-4">🔄</div>
                <h2 className="text-2xl font-bold text-primary-900 dark:text-primary-100 mb-2">
                  Analyzing Your Financial Data
                </h2>
                <p className="text-gray-600 dark:text-gray-400 mb-6">
                  We're fetching your banking data and generating your credit score...
                </p>
                <div className="space-y-3">
                  <div className="flex items-center justify-center space-x-2 text-green-600">
                    <span>✓</span>
                    <span>Bank connected successfully</span>
                  </div>
                  <div className="flex items-center justify-center space-x-2 text-green-600">
                    <span>✓</span>
                    <span>Transaction data fetched</span>
                  </div>
                  <div className="flex items-center justify-center space-x-2 text-blue-600">
                    <span>⟳</span>
                    <span>Running AI analysis...</span>
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        </main>
      </div>
      <Footer />
    </motion.div>
  );
}

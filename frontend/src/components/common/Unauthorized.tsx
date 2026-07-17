import { Link } from 'react-router-dom';
import Alert from '../ui/Alert';

export default function Unauthorized() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full">
        <Alert type="error">
          <div className="text-center">
            <h2 className="text-xl font-semibold mb-2">Unauthorized Access</h2>
            <p className="text-gray-600 mb-4">
              You don't have permission to access this page.
            </p>
            <Link
              to="/login"
              className="inline-block px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              Login
            </Link>
          </div>
        </Alert>
      </div>
    </div>
  );
}

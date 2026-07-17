export const validationRules = {
  email: {
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    message: 'Invalid email address',
  },
  password: {
    minLength: 8,
    message: 'Password must be at least 8 characters',
  },
  phone: {
    pattern: /^[+]?[\d\s-()]{10,}$/,
    message: 'Invalid phone number',
  },
};

export function validateEmail(email: string): boolean {
  return validationRules.email.pattern.test(email);
}

export function validatePassword(password: string): boolean {
  return password.length >= validationRules.password.minLength;
}

export function validatePhone(phone: string): boolean {
  return validationRules.phone.pattern.test(phone);
}

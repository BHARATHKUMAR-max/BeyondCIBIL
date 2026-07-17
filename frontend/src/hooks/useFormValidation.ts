import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

export function useFormValidation(schema: any, defaultValues?: any) {
  const form = useForm({
    resolver: zodResolver(schema),
    defaultValues,
  });

  return form;
}

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import SignupPage from '@/src/app/signup/page';

// Mock next/router
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('SignupPage', () => {
  it('renders the signup form correctly', () => {
    render(<SignupPage />);
    
    expect(screen.getByText('Create Account')).toBeInTheDocument();
    expect(screen.getByText('Join us today')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('John')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Doe')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('john.doe@example.com')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('••••••••')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Sign Up' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Sign up with Google' })).toBeInTheDocument();
  });

  it('validates required fields', async () => {
    render(<SignupPage />);
    
    const submitButton = screen.getByRole('button', { name: 'Sign Up' });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('First name is required')).toBeInTheDocument();
      expect(screen.getByText('Last name is required')).toBeInTheDocument();
      expect(screen.getByText('Email is required')).toBeInTheDocument();
      expect(screen.getByText('Password must be at least 8 characters')).toBeInTheDocument();
      expect(screen.getByText('Please confirm your password')).toBeInTheDocument();
    });
  });

  it('validates password match', async () => {
    render(<SignupPage />);
    
    const firstNameInput = screen.getByPlaceholderText('John');
    const lastNameInput = screen.getByPlaceholderText('Doe');
    const emailInput = screen.getByPlaceholderText('john.doe@example.com');
    const passwordInput = screen.getByPlaceholderText('••••••••');
    const confirmPasswordInput = screen.getAllByPlaceholderText('••••••••')[1];
    const submitButton = screen.getByRole('button', { name: 'Sign Up' });
    
    fireEvent.change(firstNameInput, { target: { value: 'John' } });
    fireEvent.change(lastNameInput, { target: { value: 'Doe' } });
    fireEvent.change(emailInput, { target: { value: 'john.doe@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'Password123' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'DifferentPassword' } });
    
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText("Passwords don't match")).toBeInTheDocument();
    });
  });
});
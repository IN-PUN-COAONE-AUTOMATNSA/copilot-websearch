import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Atos AI Assistant', () => {
  render(<App />);
  const linkElement = screen.getByText(/Atos AI Assistant/i);
  expect(linkElement).toBeInTheDocument();
});

test('renders powered by message', () => {
  render(<App />);
  const poweredByElement = screen.getByText(/Powered by Atos AI/i);
  expect(poweredByElement).toBeInTheDocument();
});

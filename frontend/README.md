# Authentication UI Enhancement

This project implements enhanced authentication UI components for signin and signup pages with gradient backgrounds and modern design elements.

## Features

- Visually appealing signin and signup pages
- Gradient backgrounds and gradient action buttons
- Perfect alignment and spacing
- Responsive layout and accessibility
- Smooth and professional visual experience

## Tech Stack

- Next.js 14+ with App Router
- TypeScript
- Tailwind CSS
- React Server Components
- React Hook Form for form management
- Zod for form validation

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the frontend directory
3. Install dependencies:

```bash
npm install
```

### Running the Application

To run the application in development mode:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

### Building for Production

To build the application for production:

```bash
npm run build
```

To run the production build:

```bash
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── signin/
│   │   │   ├── page.tsx
│   │   │   └── components/
│   │   └── signup/
│   │       ├── page.tsx
│   │       └── components/
│   ├── components/
│   │   ├── ui/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Form.tsx
│   │   └── auth/
│   │       ├── AuthForm.tsx
│   │       ├── GradientButton.tsx
│   │       └── GradientBackground.tsx
│   ├── styles/
│   │   └── globals.css
│   └── lib/
│       └── utils.ts
└── tests/
    ├── components/
    ├── pages/
    └── e2e/
        └── auth-flow.cy.ts
```

## Components

### UI Components

- `Button.tsx`: Custom button component with gradient styling capability
- `Input.tsx`: Input component with focus/hover states
- `Form.tsx`: Form component with validation capabilities
- `Label.tsx`: Accessible label component
- `Card.tsx`: Card component for grouping content

### Auth Components

- `GradientBackground.tsx`: Component with blue→purple→pink gradient background
- `GradientButton.tsx`: Button with gradient styling
- `AuthForm.tsx`: Reusable authentication form wrapper

## Testing

Unit tests are written using Jest and React Testing Library.
End-to-end tests are written using Cypress.

To run unit tests:

```bash
npm run test
```

To run end-to-end tests:

```bash
npm run test:e2e
```

## Environment Variables

If needed, create a `.env.local` file in the root of the frontend directory with your environment variables.
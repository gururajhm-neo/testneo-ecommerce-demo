# E-commerce Frontend

Modern React e-commerce application built with Vite, React Router, and Tailwind CSS.

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

```bash
npm install
```

### Running the Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Building for Production

```bash
npm run build
```

## Features

- 🛍️ Product catalog with search
- 🔐 User authentication (Login/Register)
- 🛒 Shopping cart
- 📱 Responsive design
- 🎨 Modern UI with Tailwind CSS
- ⚡ Fast performance with Vite

## API Integration

The frontend connects to the FastAPI backend running on `http://localhost:9000`

Make sure the backend is running before starting the frontend.

## Project Structure

```
src/
├── api.js              # API client configuration
├── App.jsx             # Main app component with routing
├── main.jsx            # Entry point
├── components/         # Reusable components
│   └── Layout.jsx
├── context/           # React context providers
│   └── AuthContext.jsx
└── pages/             # Page components
    ├── Home.jsx
    ├── Products.jsx
    ├── ProductDetail.jsx
    ├── Login.jsx
    └── Register.jsx
```

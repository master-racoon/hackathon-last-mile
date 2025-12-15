import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background">
        <header className="border-b">
          <div className="container mx-auto px-4 py-4">
            <h1 className="text-2xl font-bold">My App</h1>
          </div>
        </header>
        
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

function Home() {
  return (
    <div className="space-y-4">
      <h2 className="text-3xl font-bold">Welcome!</h2>
      <p className="text-muted-foreground">
        This is a clean starter template with React, TypeScript, and Tailwind CSS.
      </p>
    </div>
  );
}

export default App;

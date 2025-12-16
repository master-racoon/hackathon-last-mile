import { BrowserRouter, Routes, Route, Navigate, Link } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { OrdersListView } from "./pages/OrdersListView";
import { CreateOrderForm } from "./pages/CreateOrderForm";
import { RecommendationsView } from "./pages/RecommendationsView";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-background">
          <header className="border-b">
            <div className="container mx-auto px-4 py-4">
              <Link to="/">
                <h1 className="text-2xl font-bold">
                  LastMile - Shipping Management
                </h1>
              </Link>
            </div>
          </header>

          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<OrdersListView />} />
              <Route path="/orders/new" element={<CreateOrderForm />} />
              <Route
                path="/orders/:orderId/recommendations"
                element={<RecommendationsView />}
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;

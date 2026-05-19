import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Scanner from "./pages/Scanner";
import Result from "./pages/Result";
import Auth from "./pages/Auth";
import History from "./pages/History";

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<Scanner />} />
        <Route path="/result/:barcode" element={<Result />} />
        <Route path="/auth" element={<Auth />} />
        <Route path="/history" element={<History />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  );
}

import { Routes, Route, Navigate } from "react-router-dom";
import Scanner from "./pages/Scanner";
import Result from "./pages/Result";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Scanner />} />
      <Route path="/result/:barcode" element={<Result />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

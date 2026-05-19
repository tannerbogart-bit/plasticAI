import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login, register } from "../api";
import { useAuth } from "../context/AuthContext";
import styles from "./Auth.module.css";

export default function Auth() {
  const [mode, setMode] = useState("login"); // login | register
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const { setUser } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const fn = mode === "login" ? login : register;
    const data = await fn(email.trim().toLowerCase(), password).catch(() => null);

    setLoading(false);

    if (!data || data.error) {
      setError(data?.error ?? "Something went wrong. Try again.");
      return;
    }

    setUser(data.user);
    navigate("/");
  };

  return (
    <div className={styles.page}>
      <button className={styles.back} onClick={() => navigate("/")}>← Back</button>

      <div className={styles.card}>
        <h1 className={styles.logo}>ClearScan</h1>

        <div className={styles.tabs}>
          <button
            className={`${styles.tab} ${mode === "login" ? styles.active : ""}`}
            onClick={() => { setMode("login"); setError(null); }}
          >
            Sign in
          </button>
          <button
            className={`${styles.tab} ${mode === "register" ? styles.active : ""}`}
            onClick={() => { setMode("register"); setError(null); }}
          >
            Create account
          </button>
        </div>

        <form className={styles.form} onSubmit={handleSubmit}>
          <label className={styles.label}>
            Email
            <input
              type="email"
              className={styles.input}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              autoComplete="email"
            />
          </label>

          <label className={styles.label}>
            Password
            <input
              type="password"
              className={styles.input}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              autoComplete={mode === "login" ? "current-password" : "new-password"}
              minLength={8}
            />
          </label>

          {error && <p className={styles.error}>{error}</p>}

          <button type="submit" className={styles.submit} disabled={loading}>
            {loading ? "…" : mode === "login" ? "Sign in" : "Create account"}
          </button>
        </form>

        {mode === "login" && (
          <p className={styles.sub}>
            Don't have an account?{" "}
            <button className={styles.link} onClick={() => setMode("register")}>
              Sign up free
            </button>
          </p>
        )}
      </div>

      <div className={styles.premiumNote}>
        <p>Premium unlocks detailed ingredient breakdowns,</p>
        <p>alternatives + weekly exposure tracking — $4.99/mo</p>
      </div>
    </div>
  );
}

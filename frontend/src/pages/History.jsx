import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getHistory } from "../api";
import { useAuth } from "../context/AuthContext";
import styles from "./History.module.css";

function scoreColor(pct) {
  if (pct <= 5)  return "#22c55e";
  if (pct <= 20) return "#84cc16";
  if (pct <= 40) return "#f59e0b";
  if (pct <= 65) return "#f97316";
  return "#ef4444";
}

export default function History() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) { navigate("/auth"); return; }
    getHistory().then((data) => {
      setScans(data.scans || []);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [user, navigate]);

  return (
    <div className={styles.page}>
      <div className={styles.topBar}>
        <button className={styles.navBtn} onClick={() => navigate("/")}>← Scan</button>
        <span className={styles.title}>My Scans</span>
        <div style={{ width: 60 }} />
      </div>

      {loading && (
        <div className={styles.center}>
          <div className={styles.spinner} />
        </div>
      )}

      {!loading && scans.length === 0 && (
        <div className={styles.center}>
          <p className={styles.empty}>No scans yet — scan a product to get started.</p>
          <button className={styles.ctaBtn} onClick={() => navigate("/")}>Scan now</button>
        </div>
      )}

      {!loading && scans.length > 0 && (
        <ul className={styles.list}>
          {scans.map((s) => {
            const pct = Math.round(s.plastic_percentage ?? 0);
            const color = scoreColor(pct);
            return (
              <li
                key={s.scan_id}
                className={styles.item}
                onClick={() => navigate(`/result/${s.barcode}`)}
              >
                {s.image_url
                  ? <img src={s.image_url} alt={s.name} className={styles.thumb} />
                  : <div className={styles.thumbPlaceholder} />
                }
                <div className={styles.info}>
                  <p className={styles.name}>{s.name || s.barcode}</p>
                  {s.brand && <p className={styles.brand}>{s.brand}</p>}
                  <div className={styles.bar}>
                    <div
                      className={styles.barFill}
                      style={{ width: `${pct}%`, background: color }}
                    />
                  </div>
                </div>
                <div className={styles.score} style={{ color }}>
                  {pct}%
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

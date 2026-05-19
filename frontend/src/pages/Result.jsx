import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { scanBarcode } from "../api";
import styles from "./Result.module.css";

function verdictFor(pct) {
  if (pct <= 5)  return { label: "Clean",    color: "#22c55e", bg: "rgba(34,197,94,0.12)" };
  if (pct <= 20) return { label: "Low",      color: "#84cc16", bg: "rgba(132,204,22,0.12)" };
  if (pct <= 40) return { label: "Moderate", color: "#f59e0b", bg: "rgba(245,158,11,0.12)" };
  if (pct <= 65) return { label: "High",     color: "#f97316", bg: "rgba(249,115,22,0.12)" };
  return         { label: "Very High",       color: "#ef4444", bg: "rgba(239,68,68,0.12)" };
}

// SVG ring gauge — draws an arc proportional to pct
function Gauge({ pct, color }) {
  const r = 54;
  const circ = 2 * Math.PI * r;
  const dash = (pct / 100) * circ;

  return (
    <svg className={styles.gaugeSvg} viewBox="0 0 120 120">
      <circle cx="60" cy="60" r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="10" />
      <circle
        cx="60" cy="60" r={r} fill="none"
        stroke={color} strokeWidth="10"
        strokeDasharray={`${dash} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 60 60)"
        style={{ transition: "stroke-dasharray 0.8s cubic-bezier(.4,0,.2,1)" }}
      />
      <text x="60" y="54" textAnchor="middle" fill="#fff" fontSize="22" fontWeight="800">{pct}%</text>
      <text x="60" y="72" textAnchor="middle" fill="rgba(255,255,255,0.45)" fontSize="9">plastic</text>
    </svg>
  );
}

export default function Result() {
  const { barcode } = useParams();
  const navigate = useNavigate();
  const [phase, setPhase] = useState("loading");
  const [product, setProduct] = useState(null);

  useEffect(() => {
    scanBarcode(barcode).then((data) => {
      if (data.status === "ok") {
        setProduct(data.product);
        setPhase("ok");
      } else {
        setPhase(data.status === "not_found" ? "not_found" : "error");
      }
    }).catch(() => setPhase("error"));
  }, [barcode]);

  if (phase === "loading") {
    return (
      <div className={styles.splash}>
        <div className={styles.spinner} />
        <p className={styles.splashText}>Analyzing product…</p>
      </div>
    );
  }

  if (phase !== "ok") {
    return (
      <div className={styles.splash}>
        <p className={styles.splashText}>
          {phase === "not_found" ? "Product not found in database." : "Something went wrong."}
        </p>
        <button className={styles.outlineBtn} onClick={() => navigate("/")}>Try another</button>
      </div>
    );
  }

  const pct = Math.round(product.plastic_percentage ?? 0);
  const verdict = verdictFor(pct);
  const flagged = product.flagged_ingredients || [];

  return (
    <div className={styles.page}>
      {/* Back button row — safe-area aware */}
      <div className={styles.backRow}>
        <button className={styles.backBtn} onClick={() => navigate("/")}>← Scan another</button>
      </div>

      {/* Hero */}
      <div className={styles.hero} style={{ background: verdict.bg }}>
        {product.image_url && (
          <img src={product.image_url} alt={product.name} className={styles.productImg} />
        )}
        <div className={styles.heroContent}>
          <Gauge pct={pct} color={verdict.color} />
          <div className={styles.heroText}>
            <p className={styles.verdictLabel} style={{ color: verdict.color }}>
              {verdict.label} plastic content
            </p>
            <p className={styles.productName}>{product.name}</p>
            {product.brand && <p className={styles.brand}>{product.brand}</p>}
          </div>
        </div>
      </div>

      {/* Summary */}
      <div className={styles.section}>
        <p className={styles.summary}>{product.risk_summary}</p>
      </div>

      {/* Flagged ingredients */}
      {flagged.length > 0 && (
        <div className={styles.section}>
          <p className={styles.sectionTitle}>What we found</p>
          <ul className={styles.flagList}>
            {flagged.map((f, i) => (
              <li key={i} className={styles.flagItem}>
                <span className={styles.flagName}>{f.name}</span>
                <span className={styles.flagReason}>{f.reason}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Premium upsell */}
      <div className={styles.upsell}>
        <p className={styles.upsellTitle}>See the full breakdown</p>
        <p className={styles.upsellSub}>
          Detailed ingredient analysis, lower-plastic alternatives, and weekly exposure tracking.
        </p>
        <button className={styles.upgradeBtn}>
          Get Premium — $4.99/mo
        </button>
      </div>

      <button className={styles.scanAgain} onClick={() => navigate("/")}>
        Scan another product
      </button>
    </div>
  );
}

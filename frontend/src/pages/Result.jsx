import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { scanBarcode } from "../api";
import styles from "./Result.module.css";

function riskColor(score) {
  if (score <= 3) return "var(--low)";
  if (score <= 6) return "var(--mid)";
  return "var(--high)";
}

function riskLabel(score) {
  if (score <= 3) return "Low Risk";
  if (score <= 6) return "Moderate Risk";
  return "High Risk";
}

export default function Result() {
  const { barcode } = useParams();
  const navigate = useNavigate();
  const [state, setState] = useState("loading"); // loading | ok | not_found | error
  const [product, setProduct] = useState(null);

  useEffect(() => {
    scanBarcode(barcode).then((data) => {
      if (data.status === "ok") {
        setProduct(data.product);
        setState("ok");
      } else if (data.status === "not_found") {
        setState("not_found");
      } else {
        setState("error");
      }
    }).catch(() => setState("error"));
  }, [barcode]);

  if (state === "loading") {
    return (
      <div className={styles.center}>
        <div className={styles.spinner} />
        <p>Analyzing product...</p>
      </div>
    );
  }

  if (state === "not_found") {
    return (
      <div className={styles.center}>
        <p className={styles.notFound}>Product not found in database.</p>
        <button className={styles.back} onClick={() => navigate("/")}>Scan another</button>
      </div>
    );
  }

  if (state === "error") {
    return (
      <div className={styles.center}>
        <p className={styles.notFound}>Something went wrong. Try again.</p>
        <button className={styles.back} onClick={() => navigate("/")}>Go back</button>
      </div>
    );
  }

  const color = riskColor(product.risk_score);
  const label = riskLabel(product.risk_score);

  return (
    <div className={styles.page}>
      <button className={styles.backBtn} onClick={() => navigate("/")}>← Scan another</button>

      <div className={styles.card}>
        {product.image_url && (
          <img src={product.image_url} alt={product.name} className={styles.productImage} />
        )}
        <div className={styles.productInfo}>
          <p className={styles.brand}>{product.brand}</p>
          <h2 className={styles.name}>{product.name}</h2>
        </div>

        <div className={styles.scoreRow}>
          <div
            className={styles.scoreCircle}
            style={{ borderColor: color, color }}
          >
            <span className={styles.scoreNum}>{product.risk_score.toFixed(1)}</span>
            <span className={styles.scoreDenom}>/10</span>
          </div>
          <div>
            <p className={styles.riskLabel} style={{ color }}>{label}</p>
            <p className={styles.summary}>{product.risk_summary}</p>
          </div>
        </div>

        <div className={styles.premiumGate}>
          <p className={styles.gateTitle}>Unlock full breakdown</p>
          <ul className={styles.gateFeatures}>
            <li>Detailed ingredient-by-ingredient analysis</li>
            <li>Lower-plastic alternative products</li>
            <li>Weekly exposure tracking</li>
          </ul>
          <button className={styles.upgradeBtn}>Get ClearScan Premium — $4.99/mo</button>
        </div>
      </div>

      <p className={styles.barcode}>Barcode: {barcode}</p>
    </div>
  );
}

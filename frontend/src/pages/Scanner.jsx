import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { BrowserMultiFormatReader } from "@zxing/library";
import { useAuth } from "../context/AuthContext";
import styles from "./Scanner.module.css";

export default function Scanner() {
  const videoRef = useRef(null);
  const readerRef = useRef(null);
  const navigate = useNavigate();
  const { user } = useAuth();
  const [status, setStatus] = useState("starting"); // starting | ready | denied
  const [manualBarcode, setManualBarcode] = useState("");
  const [showManual, setShowManual] = useState(false);

  useEffect(() => {
    const reader = new BrowserMultiFormatReader();
    readerRef.current = reader;

    reader
      .decodeFromVideoDevice(null, videoRef.current, (result) => {
        if (result) {
          reader.reset();
          navigate(`/result/${result.getText()}`);
        }
      })
      .then(() => setStatus("ready"))
      .catch(() => {
        setStatus("denied");
        setShowManual(true);
      });

    return () => reader.reset();
  }, [navigate]);

  const handleManual = (e) => {
    e.preventDefault();
    const code = manualBarcode.trim();
    if (code) navigate(`/result/${code}`);
  };

  return (
    <div className={styles.page}>
      <video ref={videoRef} className={styles.video} muted playsInline />

      <div className={styles.ui}>
        <div className={styles.topBar}>
          <span className={styles.logo}>ClearScan</span>
          <button className={styles.authBtn} onClick={() => navigate("/auth")}>
            {user ? (user.is_premium ? "★ Premium" : "Sign in") : "Sign in"}
          </button>
        </div>

        <div className={styles.middle}>
          <div className={styles.frame}>
            <span className={styles.corner} data-pos="tl" />
            <span className={styles.corner} data-pos="tr" />
            <span className={styles.corner} data-pos="bl" />
            <span className={styles.corner} data-pos="br" />
            {status === "ready" && <div className={styles.scanLine} />}
          </div>
          <p className={styles.hint}>
            {status === "starting" && "Starting camera…"}
            {status === "ready" && "Point at any product barcode"}
            {status === "denied" && "Camera blocked — use manual entry"}
          </p>
        </div>

        <div className={styles.bottom}>
          {!showManual ? (
            <button className={styles.manualToggle} onClick={() => setShowManual(true)}>
              Enter barcode manually
            </button>
          ) : (
            <form className={styles.manualForm} onSubmit={handleManual}>
              <input
                autoFocus
                type="text"
                inputMode="numeric"
                placeholder="Barcode number…"
                value={manualBarcode}
                onChange={(e) => setManualBarcode(e.target.value)}
                className={styles.input}
              />
              <button type="submit" className={styles.goBtn}>Go</button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}

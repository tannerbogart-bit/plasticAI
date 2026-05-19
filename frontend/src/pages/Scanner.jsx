import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { BrowserMultiFormatReader } from "@zxing/library";
import styles from "./Scanner.module.css";

export default function Scanner() {
  const videoRef = useRef(null);
  const readerRef = useRef(null);
  const navigate = useNavigate();
  const [manualBarcode, setManualBarcode] = useState("");
  const [error, setError] = useState(null);
  const [scanning, setScanning] = useState(false);

  useEffect(() => {
    const reader = new BrowserMultiFormatReader();
    readerRef.current = reader;

    reader
      .decodeFromVideoDevice(null, videoRef.current, (result, err) => {
        if (result) {
          reader.reset();
          navigate(`/result/${result.getText()}`);
        }
      })
      .then(() => setScanning(true))
      .catch((e) => {
        setError("Camera access denied. Use manual entry below.");
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
      <header className={styles.header}>
        <h1 className={styles.logo}>ClearScan</h1>
        <p className={styles.tagline}>Find plastics in products</p>
      </header>

      <div className={styles.viewfinder}>
        <video ref={videoRef} className={styles.video} muted playsInline />
        <div className={styles.overlay}>
          <div className={styles.scanLine} />
          <span className={styles.hint}>
            {error ? error : scanning ? "Point at a barcode" : "Starting camera..."}
          </span>
        </div>
      </div>

      <form className={styles.manual} onSubmit={handleManual}>
        <input
          type="text"
          inputMode="numeric"
          placeholder="Or enter barcode manually"
          value={manualBarcode}
          onChange={(e) => setManualBarcode(e.target.value)}
          className={styles.input}
        />
        <button type="submit" className={styles.btn}>Scan</button>
      </form>
    </div>
  );
}

const BASE = "/api";

export async function scanBarcode(barcode, premium = false) {
  const res = await fetch(`${BASE}/scan/${barcode}?premium=${premium}`);
  return res.json();
}

export async function login(email, password) {
  const res = await fetch(`${BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
    credentials: "include",
  });
  return res.json();
}

export async function register(email, password) {
  const res = await fetch(`${BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
    credentials: "include",
  });
  return res.json();
}

export async function getMe() {
  const res = await fetch(`${BASE}/auth/me`, { credentials: "include" });
  return res.json();
}

export async function getHistory() {
  const res = await fetch(`${BASE}/auth/history`, { credentials: "include" });
  return res.json();
}

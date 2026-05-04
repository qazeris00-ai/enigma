"use client";

import { useState, useRef, useCallback, useEffect } from "react";

export default function Home() {
  const [clicking, setClicking] = useState(false);
  const [interval, setIntervalVal] = useState(100);
  const [clickCount, setClickCount] = useState(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const clearTimer = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  useEffect(() => {
    if (clicking) {
      clearTimer();
      timerRef.current = setInterval(() => {
        setClickCount((prev) => prev + 1);
      }, interval);
    } else {
      clearTimer();
    }
    return clearTimer;
  }, [clicking, interval, clearTimer]);

  const toggleClicking = useCallback(() => {
    setClicking((prev) => !prev);
  }, []);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.code === "Space" && e.target === document.body) {
        e.preventDefault();
        setClicking((prev) => !prev);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  return (
    <main className="min-h-screen bg-neutral-900 flex flex-col items-center justify-center gap-8 text-white">
      <h1 className="text-4xl font-bold">Auto Clicker</h1>
      <div className="text-6xl font-mono tabular-nums">{clickCount}</div>
      <div className="flex items-center gap-4">
        <label className="text-sm text-neutral-400">Interval (ms):</label>
        <input
          type="number"
          min={10}
          max={10000}
          value={interval}
          onChange={(e) => setIntervalVal(Math.max(10, Number(e.target.value)))}
          disabled={clicking}
          className="w-24 bg-neutral-800 border border-neutral-700 rounded px-3 py-2 text-center disabled:opacity-50"
        />
      </div>
      <button
        onClick={toggleClicking}
        className={`px-8 py-4 rounded-lg font-semibold text-lg transition-colors ${
          clicking
            ? "bg-red-600 hover:bg-red-700"
            : "bg-green-600 hover:bg-green-700"
        }`}
      >
        {clicking ? "Stop" : "Start"}
      </button>
      <button
        onClick={() => setClickCount(0)}
        disabled={clicking || clickCount === 0}
        className="px-4 py-2 bg-neutral-700 hover:bg-neutral-600 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Reset
      </button>
      <p className="text-neutral-500 text-sm">Press Space to toggle</p>
    </main>
  );
}

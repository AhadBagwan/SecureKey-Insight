import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [breachStatus, setBreachStatus] = useState("");
  const [copied, setCopied] = useState(false);
  const [commonWarning, setCommonWarning] = useState("");

  const commonPasswords = [
    "123456", "password", "12345678", "qwerty", "123456789", "12345",
    "1234", "111111", "1234567", "dragon"
  ];

  const checkStrength = (pwd) => {
    let score = 0;
    const suggestions = [];

    if (pwd.length >= 8) score++;
    else suggestions.push("Use at least 8 characters");

    if (/[a-z]/.test(pwd)) score++;
    else suggestions.push("Add lowercase letters");

    if (/[A-Z]/.test(pwd)) score++;
    else suggestions.push("Add uppercase letters");

    if (/\d/.test(pwd)) score++;
    else suggestions.push("Include numbers");

    if (/[!@#$%^&*(),.?\":{}|<>]/.test(pwd)) score++;
    else suggestions.push("Add special characters");

    const passed = score === 5;

    return {
      passed,
      score,
      suggestions
    };
  };

  const { passed, score, suggestions } = checkStrength(password);

  const checkBreach = async () => {
    try {
      const res = await axios.post("https://securekey-insight.onrender.com/api/check", { password });

      setBreachStatus(res.data.breach_result);
    } catch {
      setBreachStatus("Error checking breach");
    }
  };

  const generatePassword = () => {
    const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()?";
    let pwd = "";
    for (let i = 0; i < 12; i++) {
      pwd += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    setPassword(pwd);
    setBreachStatus("");
    setCommonWarning(commonPasswords.includes(pwd) ? "This is a very common password!" : "");
  };

  const handlePasswordChange = (e) => {
    const pwd = e.target.value;
    setPassword(pwd);
    setBreachStatus("");
    setCommonWarning(commonPasswords.includes(pwd) ? "This is a very common password!" : "");
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(password);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getStrengthLabel = (score) => {
    if (score <= 2) return "Weak";
    if (score === 3 || score === 4) return "Moderate";
    return "Strong";
  };

  return (
    <div className={`container ${darkMode ? "dark-mode" : "light-mode"}`}>
      <header>
        <h1>SecureKey Insight</h1>
        <button className="toggle-mode" onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? "☀ Light Mode" : "🌙 Dark Mode"}
        </button>
      </header>

      <div className="input-group">
        <input
          type={showPassword ? "text" : "password"}
          value={password}
          onChange={handlePasswordChange}
          placeholder="Enter your password"
        />
        <button onClick={() => setShowPassword((prev) => !prev)}>
          {showPassword ? "👁️‍🗨️ Hide" : "👁️ Show"}
        </button>
      </div>

      <div className="button-group">
        <button onClick={generatePassword}>Generate</button>
        <button onClick={checkBreach}>Check Breach</button>
        <button onClick={copyToClipboard}>Copy</button>
      </div>

      <div className="results">
        {copied && <p className="info">Password copied to clipboard!</p>}
        {password && (
          <>
            <div className="strength-bar">
              <div className={`bar score-${score}`} />
            </div>
            <p className={`strength-label ${getStrengthLabel(score).toLowerCase()}`}>
              Strength: {getStrengthLabel(score)}
            </p>

            {suggestions.length > 0 && (
              <ul className="suggestions">
                {suggestions.map((sug, idx) => (
                  <li key={idx}>➤ {sug}</li>
                ))}
              </ul>
            )}
            {commonWarning && <p className="warning">{commonWarning}</p>}
          </>
        )}
        {breachStatus && <p className="breach">{breachStatus}</p>}
      </div>

      <div className="tips">
        <h3>Phishing Protection Tips</h3>
        <ul>
          <li>Never reuse passwords across multiple sites.</li>
          <li>Always verify website URLs before entering credentials.</li>
          <li>Use a password manager for strong and unique passwords.</li>
          <li>Watch for suspicious emails or links asking for login info.</li>
        </ul>
      </div>
    </div>
  );
}

export default App;

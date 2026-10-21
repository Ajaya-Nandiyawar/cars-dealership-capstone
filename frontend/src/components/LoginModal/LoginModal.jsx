import React, { useState } from "react";

const LoginModal = ({ isOpen, onClose, onLoginSuccess, onSwitchToRegister }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!username.trim() || !password) {
      setError("Please enter both username and password.");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("/api/auth/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username.trim(),
          password: password,
        }),
      });

      const data = await response.json();
      if (response.ok && (data.status === "Authenticated" || data.userName)) {
        onLoginSuccess({
          authenticated: true,
          userName: data.userName,
          firstName: data.firstName,
          lastName: data.lastName,
          email: data.email,
        });
        onClose();
      } else {
        setError(data.error || "Invalid username or password.");
      }
    } catch (err) {
      setError("Network connection failure. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" id="login-modal-overlay" onClick={onClose}>
      <div
        className="modal-content"
        id="login-modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          type="button"
          className="modal-close"
          id="login-modal-close"
          onClick={onClose}
        >
          &times;
        </button>

        <div style={{ textAlign: "center", marginBottom: "1.5rem" }}>
          <div className="register-badge">🚗 Dealership Account</div>
          <h2 style={{ fontSize: "1.6rem", marginTop: "0.5rem" }}>Sign In</h2>
          <p style={{ color: "#94a3b8", fontSize: "0.9rem" }}>
            Access verified reviews and submit dealership ratings
          </p>
        </div>

        {error && (
          <div className="alert alert-error" id="login-error-alert" role="alert">
            <span>⚠️ {error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} id="login-form">
          <div className="form-group">
            <label htmlFor="login-username">Username</label>
            <input
              type="text"
              id="login-username"
              placeholder="e.g. testuser or admin"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="login-password">Password</label>
            <input
              type="password"
              id="login-password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              required
            />
          </div>

          <button
            type="submit"
            className="btn-register"
            id="login-submit-btn"
            disabled={loading}
          >
            {loading ? "Signing In..." : "Log In"}
          </button>
        </form>

        <div className="register-footer" style={{ marginTop: "1.25rem" }}>
          <span>Don't have an account? </span>
          <button
            type="button"
            className="btn-link"
            id="switch-to-register-btn"
            onClick={() => {
              onClose();
              if (onSwitchToRegister) onSwitchToRegister();
            }}
          >
            Register here
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginModal;

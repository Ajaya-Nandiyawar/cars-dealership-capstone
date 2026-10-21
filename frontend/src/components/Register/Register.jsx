import React, { useState } from "react";
import "./Register.css";

const Register = ({ onNavigateToLogin, apiBaseUrl = "" }) => {
  const [formData, setFormData] = useState({
    username: "",
    firstName: "",
    lastName: "",
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear field-specific error as user types
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }));
    }
    setServerError("");
  };

  const validate = () => {
    const errs = {};
    if (!formData.username.trim()) {
      errs.username = "Username is required";
    }
    if (!formData.firstName.trim()) {
      errs.firstName = "First name is required";
    }
    if (!formData.lastName.trim()) {
      errs.lastName = "Last name is required";
    }
    if (!formData.email.trim()) {
      errs.email = "Email is required";
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(formData.email.trim())) {
        errs.email = "Please enter a valid email address";
      }
    }
    if (!formData.password) {
      errs.password = "Password is required";
    } else if (formData.password.length < 6) {
      errs.password = "Password must be at least 6 characters";
    }
    return errs;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setServerError("");
    setSuccessMessage("");

    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setLoading(true);
    try {
      const url = `${apiBaseUrl}/api/auth/register/`;
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: formData.username.trim(),
          first_name: formData.firstName.trim(),
          last_name: formData.lastName.trim(),
          email: formData.email.trim().toLowerCase(),
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccessMessage(
          "Registration successful! Redirecting to login..."
        );
        setTimeout(() => {
          if (onNavigateToLogin) {
            onNavigateToLogin();
          } else {
            window.location.href = "/login";
          }
        }, 1500);
      } else {
        setServerError(
          data.error || data.detail || "Registration failed. Please try again."
        );
      }
    } catch (err) {
      setServerError("Network error. Could not connect to the server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container" id="register-page">
      <div className="register-card">
        <div className="register-header">
          <div className="register-badge">🚗 Cars Dealership</div>
          <h2>Create New Account</h2>
          <p>Join the national dealership network to review dealers and save favorites</p>
        </div>

        {serverError && (
          <div className="alert alert-error" id="register-error-alert" role="alert">
            <span>⚠️ {serverError}</span>
          </div>
        )}

        {successMessage && (
          <div className="alert alert-success" id="register-success-alert" role="alert">
            <span>✓ {successMessage}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} noValidate id="registration-form">
          {/* 1. Username */}
          <div className="form-group">
            <label htmlFor="reg-username">Username *</label>
            <input
              type="text"
              id="reg-username"
              name="username"
              placeholder="e.g. johndoe"
              value={formData.username}
              onChange={handleChange}
              className={errors.username ? "input-error" : ""}
              autoComplete="username"
              required
            />
            {errors.username && <span className="field-error">{errors.username}</span>}
          </div>

          {/* 2. First Name */}
          <div className="form-group">
            <label htmlFor="reg-firstName">First Name *</label>
            <input
              type="text"
              id="reg-firstName"
              name="firstName"
              placeholder="e.g. John"
              value={formData.firstName}
              onChange={handleChange}
              className={errors.firstName ? "input-error" : ""}
              autoComplete="given-name"
              required
            />
            {errors.firstName && <span className="field-error">{errors.firstName}</span>}
          </div>

          {/* 3. Last Name */}
          <div className="form-group">
            <label htmlFor="reg-lastName">Last Name *</label>
            <input
              type="text"
              id="reg-lastName"
              name="lastName"
              placeholder="e.g. Doe"
              value={formData.lastName}
              onChange={handleChange}
              className={errors.lastName ? "input-error" : ""}
              autoComplete="family-name"
              required
            />
            {errors.lastName && <span className="field-error">{errors.lastName}</span>}
          </div>

          {/* 4. Email */}
          <div className="form-group">
            <label htmlFor="reg-email">Email Address *</label>
            <input
              type="email"
              id="reg-email"
              name="email"
              placeholder="e.g. john@example.com"
              value={formData.email}
              onChange={handleChange}
              className={errors.email ? "input-error" : ""}
              autoComplete="email"
              required
            />
            {errors.email && <span className="field-error">{errors.email}</span>}
          </div>

          {/* 5. Password */}
          <div className="form-group">
            <label htmlFor="reg-password">Password *</label>
            <input
              type="password"
              id="reg-password"
              name="password"
              placeholder="Minimum 6 characters"
              value={formData.password}
              onChange={handleChange}
              className={errors.password ? "input-error" : ""}
              autoComplete="new-password"
              required
            />
            {errors.password && <span className="field-error">{errors.password}</span>}
          </div>

          <button
            type="submit"
            className="btn-register"
            id="register-submit-btn"
            disabled={loading}
          >
            {loading ? "Creating Account..." : "Register Account"}
          </button>
        </form>

        <div className="register-footer">
          <span>Already have an account? </span>
          <button
            type="button"
            className="btn-link"
            id="to-login-btn"
            onClick={() => (onNavigateToLogin ? onNavigateToLogin() : (window.location.href = "/login"))}
          >
            Log in here
          </button>
        </div>
      </div>
    </div>
  );
};

export default Register;

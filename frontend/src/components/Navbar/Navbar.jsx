import React from "react";

const Navbar = ({
  user,
  onOpenLogin,
  onNavigateRegister,
  onNavigateHome,
  onLogout,
  currentView,
}) => {
  return (
    <header className="app-header">
      <div className="header-inner">
        <div
          className="app-brand"
          id="brand-logo"
          onClick={onNavigateHome}
          role="button"
          tabIndex={0}
        >
          <div className="brand-badge">🚗</div>
          <div>
            <div className="brand-title">Cars Dealership</div>
            <span className="brand-subtitle">National Certified Network</span>
          </div>
        </div>

        <nav className="nav-links">
          <button
            type="button"
            className={`nav-btn ${currentView === "dealers" || currentView === "detail" ? "active" : ""}`}
            id="nav-dealers"
            onClick={onNavigateHome}
          >
            🏢 Dealerships
          </button>
          <a href="/about.html" className="nav-btn" id="nav-about">
            ℹ️ About Us
          </a>
          <a href="/contact.html" className="nav-btn" id="nav-contact">
            📞 Contact Us
          </a>
          <a
            href="/admin/"
            target="_blank"
            rel="noopener noreferrer"
            className="nav-btn"
            id="nav-admin"
          >
            🛡️ Admin Portal
          </a>
        </nav>

        <div className="user-menu">
          {user && user.authenticated ? (
            <>
              <div className="user-pill" id="logged-in-user-pill">
                <span className="user-avatar">
                  {user.userName ? user.userName.charAt(0).toUpperCase() : "U"}
                </span>
                <span id="header-username">{user.userName}</span>
              </div>
              <button
                type="button"
                className="btn-outline-sm"
                id="header-logout-btn"
                onClick={onLogout}
              >
                Log Out
              </button>
            </>
          ) : (
            <>
              <button
                type="button"
                className="btn-outline-sm"
                id="header-login-btn"
                onClick={onOpenLogin}
              >
                Log In
              </button>
              <button
                type="button"
                className="btn-primary-sm"
                id="header-register-btn"
                onClick={onNavigateRegister}
              >
                Register
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;

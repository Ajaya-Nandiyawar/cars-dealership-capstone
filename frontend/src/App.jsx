import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar/Navbar";
import DealerList from "./components/DealerList/DealerList";
import DealerDetail from "./components/DealerDetail/DealerDetail";
import Register from "./components/Register/Register";
import LoginModal from "./components/LoginModal/LoginModal";

function App() {
  const [user, setUser] = useState({ authenticated: false, userName: null });
  const [currentView, setCurrentView] = useState("dealers"); // 'dealers' | 'detail' | 'register'
  const [selectedDealerId, setSelectedDealerId] = useState(null);
  const [openReviewDirectly, setOpenReviewDirectly] = useState(false);
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const [selectedStateFilter, setSelectedStateFilter] = useState("All States");

  // Check current session user on mount
  useEffect(() => {
    fetch("/api/auth/me/")
      .then((res) => res.json())
      .then((data) => {
        if (data && data.authenticated) {
          setUser(data);
        }
      })
      .catch((err) => console.log("Session check:", err));
  }, []);

  const handleSelectDealer = (id, openReview = false) => {
    setSelectedDealerId(id);
    setOpenReviewDirectly(openReview);
    setCurrentView("detail");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleLogout = async () => {
    try {
      await fetch("/api/auth/logout/", { method: "POST" });
    } catch (err) {
      console.error("Logout request error:", err);
    }
    setUser({ authenticated: false, userName: null });
  };

  return (
    <div className="app-root">
      {/* Top Navigation */}
      <Navbar
        user={user}
        currentView={currentView}
        onOpenLogin={() => setIsLoginModalOpen(true)}
        onNavigateRegister={() => setCurrentView("register")}
        onNavigateHome={() => setCurrentView("dealers")}
        onLogout={handleLogout}
      />

      {/* Main Content Area based on currentView */}
      <main>
        {currentView === "dealers" && (
          <DealerList
            user={user}
            onSelectDealer={handleSelectDealer}
            initialState={selectedStateFilter}
            onOpenLogin={() => setIsLoginModalOpen(true)}
          />
        )}

        {currentView === "detail" && selectedDealerId && (
          <DealerDetail
            dealerId={selectedDealerId}
            user={user}
            initialShowReviewForm={openReviewDirectly}
            onBack={() => setCurrentView("dealers")}
            onOpenLogin={() => setIsLoginModalOpen(true)}
          />
        )}

        {currentView === "register" && (
          <Register
            onNavigateToLogin={() => {
              setCurrentView("dealers");
              setIsLoginModalOpen(true);
            }}
          />
        )}
      </main>

      {/* Login Modal */}
      <LoginModal
        isOpen={isLoginModalOpen}
        onClose={() => setIsLoginModalOpen(false)}
        onLoginSuccess={(userData) => {
          setUser(userData);
          setIsLoginModalOpen(false);
        }}
        onSwitchToRegister={() => setCurrentView("register")}
      />

      {/* Footer */}
      <footer style={{ borderTop: "1px solid #1e293b", padding: "2.5rem 1.5rem", textAlign: "center", color: "#64748b", fontSize: "0.9rem", marginTop: "4rem" }}>
        <p>&copy; 2026 Cars Dealership Full-Stack Capstone. All rights reserved. Demonstration Project.</p>
        <div style={{ marginTop: "0.5rem", display: "flex", justifyContent: "center", gap: "1.5rem" }}>
          <a href="/about.html" style={{ color: "#94a3b8" }}>About Us</a>
          <a href="/contact.html" style={{ color: "#94a3b8" }}>Contact Us</a>
          <a href="/admin/" style={{ color: "#94a3b8" }}>Admin</a>
        </div>
      </footer>
    </div>
  );
}

export default App;

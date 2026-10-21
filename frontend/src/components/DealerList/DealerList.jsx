import React, { useState, useEffect } from "react";

const US_STATES = [
  "All States",
  "Kansas",
  "California",
  "Texas",
  "New York",
  "Florida",
  "Illinois",
  "Washington",
  "Colorado",
];

const DealerList = ({
  user,
  onSelectDealer,
  initialState = "All States",
  onOpenLogin,
}) => {
  const [dealers, setDealers] = useState([]);
  const [selectedState, setSelectedState] = useState(initialState);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const currentEndpoint =
    selectedState === "All States"
      ? "/api/dealers/"
      : `/api/dealers/?state=${encodeURIComponent(selectedState)}`;

  const fetchDealers = async (state) => {
    setLoading(true);
    setError("");
    try {
      let url = "/api/dealers/";
      if (state && state !== "All States") {
        url = `/api/dealers/?state=${encodeURIComponent(state)}`;
      }
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Server returned HTTP ${response.status}`);
      }
      const data = await response.json();
      setDealers(data);
    } catch (err) {
      setError(`Failed to load dealerships (${err.message}). Check backend connection.`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDealers(selectedState);
  }, [selectedState]);

  const handleStateChange = (e) => {
    setSelectedState(e.target.value);
  };

  const filteredDealers = dealers.filter((d) => {
    const q = searchQuery.toLowerCase();
    return (
      d.full_name?.toLowerCase().includes(q) ||
      d.city?.toLowerCase().includes(q) ||
      d.state?.toLowerCase().includes(q) ||
      d.short_name?.toLowerCase().includes(q)
    );
  });

  return (
    <div id="dealers-landing-page">
      {/* Hero Banner */}
      <section className="hero-banner">
        <div className="hero-pill">
          <span>🚗 Certified National Dealership Network</span>
        </div>
        <h1 className="hero-title">Find Trusted Auto Dealerships</h1>
        <p className="hero-subtitle">
          Explore certified branches across the US, read authentic customer reviews,
          and discover available car makes and models with automated sentiment scoring.
        </p>
      </section>

      {/* Filter and Search Bar */}
      <div className="filter-card" id="dealer-filter-bar">
        <div className="search-box">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            className="search-input"
            id="search-input"
            placeholder="Search by dealership name, city, or state..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <div className="state-filter-wrap">
          <label
            htmlFor="state-select"
            style={{ fontSize: "0.9rem", color: "#94a3b8", fontWeight: 600 }}
          >
            State Filter:
          </label>
          <select
            id="state-select"
            className="state-select"
            value={selectedState}
            onChange={handleStateChange}
          >
            {US_STATES.map((st) => (
              <option key={st} value={st}>
                {st}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Active API Query Banner (Critical for assignment screenshot evidence) */}
      <div
        style={{
          maxWidth: "1280px",
          margin: "-1.5rem auto 2rem",
          padding: "0 1.5rem",
        }}
      >
        <div
          id="active-endpoint-indicator"
          style={{
            background: "rgba(15, 23, 42, 0.75)",
            border: "1px solid #334155",
            borderRadius: "8px",
            padding: "0.6rem 1rem",
            fontSize: "0.85rem",
            color: "#94a3b8",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div>
            <strong style={{ color: "#38bdf8" }}>Active Endpoint:</strong>{" "}
            <code style={{ color: "#a5b4fc", fontFamily: "monospace" }}>
              {currentEndpoint}
            </code>
          </div>
          <span style={{ color: "#34d399", fontWeight: 600 }}>
            {filteredDealers.length} Dealership{filteredDealers.length === 1 ? "" : "s"} Found
          </span>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="state-container" id="dealers-loading">
          <div className="spinner"></div>
          <p>Loading certified dealerships from network database...</p>
        </div>
      )}

      {/* Error State */}
      {error && !loading && (
        <div className="state-container" id="dealers-error">
          <div style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>⚠️</div>
          <h3 style={{ color: "#ef4444", marginBottom: "0.5rem" }}>
            Connection Error
          </h3>
          <p style={{ color: "#94a3b8" }}>{error}</p>
          <button
            type="button"
            className="btn-primary-sm"
            style={{ marginTop: "1rem" }}
            onClick={() => fetchDealers(selectedState)}
          >
            Retry Fetch
          </button>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && filteredDealers.length === 0 && (
        <div className="state-container" id="dealers-empty">
          <div style={{ fontSize: "2.5rem", marginBottom: "0.5rem" }}>🏢</div>
          <h3>No dealerships match your query</h3>
          <p>Try resetting the state filter or searching for another location.</p>
          <button
            type="button"
            className="btn-outline-sm"
            style={{ marginTop: "1rem" }}
            onClick={() => {
              setSelectedState("All States");
              setSearchQuery("");
            }}
          >
            Reset Filters
          </button>
        </div>
      )}

      {/* Dealerships Grid */}
      {!loading && !error && filteredDealers.length > 0 && (
        <div className="dealers-grid" id="dealers-grid">
          {filteredDealers.map((dealer) => (
            <article
              key={dealer.id}
              className="dealer-card"
              id={`dealer-card-${dealer.id}`}
            >
              <div className="dealer-img-wrap">
                <img
                  src={
                    dealer.image ||
                    "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80"
                  }
                  alt={dealer.full_name}
                  loading="lazy"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src =
                      "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80";
                  }}
                />
                <span className="dealer-state-pill">
                  {dealer.st || dealer.state}
                </span>
              </div>

              <div className="dealer-body">
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.4rem" }}>
                  <span className="dealer-id-pill" style={{ background: "#0284c7", color: "#ffffff", padding: "0.2rem 0.6rem", borderRadius: "4px", fontSize: "0.85rem", fontWeight: "bold" }}>
                    ID: #{dealer.id}
                  </span>
                  <span style={{ color: "#38bdf8", fontSize: "0.85rem", fontWeight: 600 }}>State: {dealer.state}</span>
                </div>
                <h3 className="dealer-name">{dealer.full_name}</h3>
                <div className="dealer-location" style={{ marginBottom: "0.25rem" }}>
                  <span>📍</span>
                  <span>
                    <strong>City:</strong> {dealer.city} | <strong>State:</strong> {dealer.state} | <strong>Zip:</strong> {dealer.zip}
                  </span>
                </div>
                <p className="dealer-address" style={{ margin: "0.25rem 0 0.75rem", color: "#cbd5e1", fontSize: "0.88rem" }}>
                  <strong>Address:</strong> {dealer.address}, {dealer.city}, {dealer.state} {dealer.zip}
                </p>

                <div className="dealer-meta">
                  <span className="reviews-badge">
                    💬 {dealer.reviews_count || 0} Reviews
                  </span>
                  <div style={{ display: "flex", gap: "0.5rem" }}>
                    {/* Logged in Review Dealer Action */}
                    {user && user.authenticated && (
                      <button
                        type="button"
                        className="btn-primary-sm"
                        id={`review-dealer-btn-${dealer.id}`}
                        onClick={() => onSelectDealer(dealer.id, true)}
                        style={{ fontSize: "0.8rem", padding: "0.4rem 0.75rem" }}
                      >
                        ✍️ Review Dealer
                      </button>
                    )}
                    <button
                      type="button"
                      className="btn-view-dealer"
                      id={`view-dealer-btn-${dealer.id}`}
                      onClick={() => onSelectDealer(dealer.id, false)}
                    >
                      View Details &rarr;
                    </button>
                  </div>
                </div>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
};

export default DealerList;

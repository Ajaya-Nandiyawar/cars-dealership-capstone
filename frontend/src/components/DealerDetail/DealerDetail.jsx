import React, { useState, useEffect } from "react";
import ReviewForm from "../ReviewForm/ReviewForm";

const DealerDetail = ({
  dealerId,
  user,
  onBack,
  onOpenLogin,
  initialShowReviewForm = false,
}) => {
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [showReviewForm, setShowReviewForm] = useState(initialShowReviewForm);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const reviewsEndpoint = `/api/dealers/${dealerId}/reviews/`;
  const dealerEndpoint = `/api/dealers/${dealerId}/`;

  const fetchDealerAndReviews = async () => {
    setLoading(true);
    setError("");
    try {
      // 1. Fetch dealer details
      const dealerRes = await fetch(dealerEndpoint);
      if (!dealerRes.ok) throw new Error("Could not load dealer details");
      const dealerData = await dealerRes.json();
      setDealer(dealerData);

      // 2. Fetch dealer reviews
      const reviewsRes = await fetch(reviewsEndpoint);
      if (!reviewsRes.ok) throw new Error("Could not load dealer reviews");
      const reviewsData = await reviewsRes.json();
      setReviews(reviewsData);
    } catch (err) {
      setError(err.message || "Failed to retrieve dealership data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDealerAndReviews();
  }, [dealerId]);

  const handleReviewSubmitted = (newReview) => {
    setReviews((prev) => [newReview, ...prev]);
    setShowReviewForm(false);
  };

  return (
    <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "2rem 1.5rem 5rem" }} id="dealer-detail-page">
      {/* Back button */}
      <div style={{ marginBottom: "1.5rem" }}>
        <button
          type="button"
          className="btn-outline-sm"
          id="back-to-dealers-btn"
          onClick={onBack}
          style={{ display: "inline-flex", alignItems: "center", gap: "0.4rem" }}
        >
          &larr; Back to Dealerships
        </button>
      </div>

      {/* Active Endpoint Indicator Banner (Essential for assignment Task 20 screenshot: dealer_id_reviews.png) */}
      <div
        id="dealer-endpoint-banner"
        style={{
          background: "rgba(15, 23, 42, 0.85)",
          border: "1px solid #334155",
          borderRadius: "10px",
          padding: "0.75rem 1.25rem",
          marginBottom: "2rem",
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "space-between",
          alignItems: "center",
          gap: "1rem",
        }}
      >
        <div>
          <span style={{ color: "#38bdf8", fontWeight: 700 }}>Active Review Endpoint:</span>{" "}
          <code style={{ color: "#a5b4fc", fontFamily: "monospace", fontSize: "0.95rem" }}>
            {reviewsEndpoint}
          </code>
        </div>
        <div style={{ color: "#94a3b8", fontSize: "0.85rem" }}>
          Dealer ID: <strong style={{ color: "#ffffff" }}>{dealerId}</strong>
        </div>
      </div>

      {loading && (
        <div className="state-container">
          <div className="spinner"></div>
          <p>Loading dealership information and verified reviews...</p>
        </div>
      )}

      {error && !loading && (
        <div className="state-container">
          <div style={{ fontSize: "2rem" }}>⚠️</div>
          <p style={{ color: "#ef4444" }}>{error}</p>
        </div>
      )}

      {!loading && dealer && (
        <>
          {/* Dealer Hero Header */}
          <section
            style={{
              background: "#182234",
              border: "1px solid #2e3d55",
              borderRadius: "16px",
              padding: "2rem",
              marginBottom: "2.5rem",
              display: "grid",
              gridTemplateColumns: "1.2fr 1fr",
              gap: "2rem",
            }}
            id="dealer-header-card"
          >
            <div>
              <span className="dealer-state-pill" style={{ position: "static", display: "inline-block", marginBottom: "0.75rem" }}>
                {dealer.state} Certified
              </span>
              <h1 style={{ fontSize: "2.2rem", marginBottom: "0.5rem" }} id="dealer-full-name">
                {dealer.full_name}
              </h1>
              <div style={{ color: "#38bdf8", fontSize: "1.05rem", fontWeight: 600, marginBottom: "1rem" }}>
                📍 {dealer.city}, {dealer.state} {dealer.zip}
              </div>
              <p style={{ color: "#94a3b8", marginBottom: "1.5rem" }}>
                {dealer.address}
              </p>

              <div style={{ display: "flex", flexWrap: "wrap", gap: "1.5rem", fontSize: "0.9rem", color: "#cbd5e1" }}>
                <div>📞 <strong>Phone:</strong> {dealer.phone}</div>
                <div>✉️ <strong>Email:</strong> {dealer.email}</div>
                {dealer.website && (
                  <div>🌐 <a href={dealer.website} target="_blank" rel="noreferrer">Website</a></div>
                )}
              </div>
            </div>

            <div style={{ borderRadius: "12px", overflow: "hidden", height: "220px", background: "#0f172a" }}>
              <img
                src={dealer.image || "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80"}
                alt={dealer.full_name}
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
              />
            </div>
          </section>

          {/* Associated Car Models / Inventory Showcase */}
          {dealer.car_models && dealer.car_models.length > 0 && (
            <section style={{ marginBottom: "3rem" }} id="associated-inventory-section">
              <h2 style={{ fontSize: "1.4rem", marginBottom: "1rem", color: "#f8fafc" }}>
                Associated Vehicles & Makes at this Branch
              </h2>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", gap: "1rem" }}>
                {dealer.car_models.map((cm) => (
                  <div
                    key={cm.id}
                    style={{
                      background: "#111827",
                      border: "1px solid #2e3d55",
                      borderRadius: "10px",
                      padding: "1rem",
                    }}
                  >
                    <div style={{ fontSize: "0.75rem", color: "#38bdf8", fontWeight: 700, textTransform: "uppercase" }}>
                      {cm.car_make_name}
                    </div>
                    <div style={{ fontSize: "1.1rem", fontWeight: 700, color: "#ffffff", marginTop: "0.2rem" }}>
                      {cm.name}
                    </div>
                    <div style={{ color: "#94a3b8", fontSize: "0.85rem", marginTop: "0.25rem" }}>
                      {cm.car_type} &bull; {cm.year}
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Review Action Trigger / Banner */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "1.5rem",
              paddingBottom: "1rem",
              borderBottom: "1px solid #2e3d55",
            }}
          >
            <div>
              <h2 style={{ fontSize: "1.6rem" }}>
                Customer Reviews ({reviews.length})
              </h2>
              <p style={{ color: "#94a3b8", fontSize: "0.9rem" }}>
                Independent feedback with automated sentiment classification
              </p>
            </div>

            {user && user.authenticated ? (
              <button
                type="button"
                className="btn-primary-sm"
                id="toggle-post-review-btn"
                onClick={() => setShowReviewForm((prev) => !prev)}
                style={{ padding: "0.65rem 1.25rem", fontSize: "0.95rem" }}
              >
                {showReviewForm ? "Close Form" : "✍️ Write a Review"}
              </button>
            ) : (
              <button
                type="button"
                className="btn-outline-sm"
                id="login-to-review-btn"
                onClick={onOpenLogin}
              >
                Log in to Review Dealer
              </button>
            )}
          </div>

          {/* Review Submission Form Component */}
          {showReviewForm && user && user.authenticated && (
            <ReviewForm
              dealerId={dealer.id}
              dealerName={dealer.full_name}
              user={user}
              onReviewSubmitted={handleReviewSubmitted}
              onCancel={() => setShowReviewForm(false)}
            />
          )}

          {/* Reviews List */}
          <div className="reviews-list" id="reviews-list">
            {reviews.length === 0 ? (
              <div className="state-container" style={{ padding: "3rem 1rem" }}>
                <p>No customer reviews posted yet for this dealership. Be the first to review!</p>
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}>
                {reviews.map((rev) => (
                  <article
                    key={rev.id}
                    id={`review-item-${rev.id}`}
                    style={{
                      background: "#182234",
                      border: "1px solid #2e3d55",
                      borderRadius: "12px",
                      padding: "1.5rem",
                    }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "0.75rem" }}>
                      <div>
                        <strong style={{ fontSize: "1.05rem", color: "#ffffff" }}>
                          {rev.name}
                        </strong>
                        {rev.purchase && (
                          <span
                            style={{
                              marginLeft: "0.75rem",
                              background: "rgba(16, 185, 129, 0.15)",
                              border: "1px solid rgba(16, 185, 129, 0.4)",
                              color: "#34d399",
                              fontSize: "0.75rem",
                              padding: "0.2rem 0.5rem",
                              borderRadius: "4px",
                              fontWeight: 600,
                            }}
                          >
                            ✓ Verified Purchase
                          </span>
                        )}
                        <div style={{ fontSize: "0.8rem", color: "#64748b", marginTop: "0.25rem" }}>
                          {rev.created_at ? new Date(rev.created_at).toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" }) : "Recent"}
                        </div>
                      </div>

                      {/* Sentiment Badge */}
                      <span className={`sentiment-badge sentiment-${rev.sentiment || "neutral"}`}>
                        {rev.sentiment === "positive" ? "✓ " : rev.sentiment === "negative" ? "✗ " : "• "}
                        {rev.sentiment || "neutral"}
                        {typeof rev.sentiment_score === "number" && (
                          <span style={{ opacity: 0.8, marginLeft: "0.25rem" }}>
                            ({rev.sentiment_score.toFixed(2)})
                          </span>
                        )}
                      </span>
                    </div>

                    <p style={{ color: "#e2e8f0", fontSize: "0.95rem", lineHeight: 1.6, marginBottom: "0.75rem" }}>
                      "{rev.review}"
                    </p>

                    {(rev.car_make || rev.car_model) && (
                      <div style={{ fontSize: "0.85rem", color: "#94a3b8" }}>
                        🚗 Vehicle: <span style={{ color: "#38bdf8" }}>{rev.car_year || ""} {rev.car_make} {rev.car_model}</span>
                        {rev.purchase_date && <span> &bull; Purchased on {rev.purchase_date}</span>}
                      </div>
                    )}
                  </article>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default DealerDetail;

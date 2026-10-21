import React, { useState, useEffect } from "react";

const ReviewForm = ({
  dealerId,
  dealerName,
  user,
  onReviewSubmitted,
  onCancel,
}) => {
  const [reviewText, setReviewText] = useState("");
  const [purchase, setPurchase] = useState(false);
  const [purchaseDate, setPurchaseDate] = useState("2024-02-14");
  const [carMake, setCarMake] = useState("");
  const [carModel, setCarModel] = useState("");
  const [carYear, setCarYear] = useState(new Date().getFullYear());
  const [carMakesList, setCarMakesList] = useState([]);

  const [sentimentPreview, setSentimentPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Load car makes for dropdown
  useEffect(() => {
    fetch("/api/car-makes/")
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setCarMakesList(data);
          if (data.length > 0) {
            setCarMake(data[0].name);
          }
        }
      })
      .catch((err) => console.error("Error fetching car makes:", err));
  }, []);

  // Quick live sentiment preview when typing
  useEffect(() => {
    if (reviewText.trim().length > 6) {
      const timer = setTimeout(() => {
        fetch("/api/analyze-review/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: reviewText }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (data && data.sentiment) {
              setSentimentPreview(data);
            }
          })
          .catch(() => {});
      }, 500);
      return () => clearTimeout(timer);
    } else {
      setSentimentPreview(null);
    }
  }, [reviewText]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!reviewText.trim()) {
      setError("Please write your review feedback.");
      return;
    }

    setLoading(true);
    try {
      const payload = {
        name: user?.firstName
          ? `${user.firstName} ${user.lastName || ""}`.trim()
          : user?.userName || "Verified Customer",
        review: reviewText.trim(),
        purchase: purchase,
        purchase_date: purchase ? purchaseDate || null : null,
        car_make: purchase ? carMake : "",
        car_model: purchase ? carModel.trim() : "",
        car_year: purchase ? parseInt(carYear, 10) || null : null,
      };

      const response = await fetch(`/api/dealers/${dealerId}/reviews/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess("Your review has been successfully posted with sentiment scoring!");
        setTimeout(() => {
          if (onReviewSubmitted) {
            onReviewSubmitted(data);
          }
        }, 1200);
      } else {
        setError(data.error || "Failed to submit review. Please try again.");
      }
    } catch (err) {
      setError("Network communication error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        background: "#182234",
        border: "1px solid #2e3d55",
        borderRadius: "14px",
        padding: "2rem",
        marginBottom: "2.5rem",
        boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.4)",
      }}
      id="review-submission-container"
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem" }}>
        <div>
          <span className="register-badge">✍️ Customer Feedback</span>
          <h2 style={{ fontSize: "1.45rem", marginTop: "0.25rem", color: "#f8fafc" }}>
            Write a Review for {dealerName}
          </h2>
        </div>
        {onCancel && (
          <button
            type="button"
            className="btn-outline-sm"
            onClick={onCancel}
            id="cancel-review-btn"
          >
            Cancel
          </button>
        )}
      </div>

      {error && (
        <div className="alert alert-error" id="review-error-alert" role="alert">
          <span>⚠️ {error}</span>
        </div>
      )}

      {success && (
        <div className="alert alert-success" id="review-success-alert" role="alert">
          <span>✓ {success}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} id="review-form">
        <div className="form-group">
          <label htmlFor="reviewer-name">Reviewer Name</label>
          <input
            type="text"
            id="reviewer-name"
            disabled
            value={
              user?.firstName
                ? `${user.firstName} ${user.lastName || ""}`.trim()
                : user?.userName || "Authenticated User"
            }
            style={{ opacity: 0.8, cursor: "not-allowed" }}
          />
        </div>

        <div className="form-group">
          <label htmlFor="review-text">Review Content *</label>
          <textarea
            id="review-text"
            rows="4"
            placeholder="Share your experience with this dealership (e.g. Fantastic services, vehicle quality, staff helpfulness)..."
            value={reviewText}
            onChange={(e) => setReviewText(e.target.value)}
            required
            style={{
              width: "100%",
              padding: "0.75rem 1rem",
              background: "#0f172a",
              border: "1px solid #334155",
              borderRadius: "8px",
              color: "#ffffff",
              fontSize: "0.95rem",
              outline: "none",
            }}
          ></textarea>
        </div>

        {/* Live Sentiment Analysis Indicator */}
        {sentimentPreview && (
          <div
            id="live-sentiment-indicator"
            style={{
              marginBottom: "1.25rem",
              padding: "0.6rem 0.9rem",
              background: "rgba(15, 23, 42, 0.75)",
              border: "1px solid #334155",
              borderRadius: "8px",
              display: "flex",
              alignItems: "center",
              gap: "0.75rem",
              fontSize: "0.85rem",
            }}
          >
            <span style={{ color: "#94a3b8" }}>Real-time Sentiment Detection:</span>
            <span
              className={`sentiment-badge sentiment-${sentimentPreview.sentiment}`}
              id="preview-sentiment-badge"
            >
              {sentimentPreview.sentiment === "positive" ? "✓ " : sentimentPreview.sentiment === "negative" ? "✗ " : "• "}
              {sentimentPreview.sentiment} (Score: {sentimentPreview.score})
            </span>
          </div>
        )}

        <div
          style={{
            marginBottom: "1.25rem",
            display: "flex",
            alignItems: "center",
            gap: "0.75rem",
          }}
        >
          <input
            type="checkbox"
            id="purchase-checkbox"
            checked={purchase}
            onChange={(e) => setPurchase(e.target.checked)}
            style={{ width: "18px", height: "18px", accentColor: "#2563eb", cursor: "pointer" }}
          />
          <label
            htmlFor="purchase-checkbox"
            style={{ color: "#cbd5e1", fontSize: "0.9rem", cursor: "pointer", fontWeight: 600 }}
          >
            I purchased a vehicle from this dealership
          </label>
        </div>

        {purchase && (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
              gap: "1rem",
              padding: "1.25rem",
              background: "#0f172a",
              borderRadius: "10px",
              border: "1px solid #334155",
              marginBottom: "1.5rem",
            }}
          >
            <div className="form-group" style={{ margin: 0 }}>
              <label htmlFor="review-car-make">Car Make</label>
              <select
                id="review-car-make"
                value={carMake}
                onChange={(e) => setCarMake(e.target.value)}
                style={{
                  width: "100%",
                  padding: "0.65rem",
                  background: "#182234",
                  border: "1px solid #334155",
                  borderRadius: "6px",
                  color: "#ffffff",
                }}
              >
                {carMakesList.map((m) => (
                  <option key={m.id} value={m.name}>
                    {m.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group" style={{ margin: 0 }}>
              <label htmlFor="review-car-model">Car Model</label>
              <input
                type="text"
                id="review-car-model"
                placeholder="e.g. Camry or F-150"
                value={carModel}
                onChange={(e) => setCarModel(e.target.value)}
              />
            </div>

            <div className="form-group" style={{ margin: 0 }}>
              <label htmlFor="review-car-year">Year</label>
              <input
                type="number"
                id="review-car-year"
                min="1990"
                max="2030"
                value={carYear}
                onChange={(e) => setCarYear(e.target.value)}
              />
            </div>

            <div className="form-group" style={{ margin: 0 }}>
              <label htmlFor="review-purchase-date">Purchase Date</label>
              <input
                type="date"
                id="review-purchase-date"
                value={purchaseDate}
                onChange={(e) => setPurchaseDate(e.target.value)}
              />
            </div>
          </div>
        )}

        <button
          type="submit"
          className="btn-register"
          id="submit-review-btn"
          disabled={loading}
          style={{ width: "auto", minWidth: "200px" }}
        >
          {loading ? "Posting Review..." : "Post Review"}
        </button>
      </form>
    </div>
  );
};

export default ReviewForm;

import { useState } from "react";

function App() {
  const [formData, setFormData] = useState({});
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendMessage() {
  if (!message.trim()) return;

  setMessages((prev) => [...prev, { role: "user", text: message }]);
  setLoading(true);

  try {
    const res = await fetch("https://hcp-interaction-bot.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();
    console.log("BACKEND RESPONSE:", data); // ← move it here

    if (data.confirmation_question) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: data.confirmation_question },
      ]);
    }

    // Normalize backend → UI form
    const extracted = data.form_data || {};

    setFormData((prev) => ({
      ...prev,

      ...(extracted.hcpName !== undefined && {
        hcp_name: extracted.hcpName,
      }),
    
      ...(extracted.interaction_type !== undefined && {
        interaction_type: extracted.interaction_type,
      }),
    
      ...(extracted.date !== undefined && {
        date: extracted.date,
      }),
    
      ...(extracted.time !== undefined && {
        time: extracted.time,
      }),
    
      ...(extracted.attendees !== undefined && {
        attendees: Array.isArray(extracted.attendees)
          ? extracted.attendees.join(", ")
          : extracted.attendees,
      }),
    
      ...(extracted.topics_discussed !== undefined && {
        topics: extracted.topics_discussed,
      }),
    
      // 🔴 FIXED PART BELOW
    
      ...(extracted.outcome !== undefined && {
        outcomes: extracted.outcome ?? "",
      }),
    
      ...(extracted.follow_up_actions !== undefined && {
        follow_up_actions: extracted.follow_up_actions ?? "",
      }),
    
      ...(extracted.sentiment !== undefined && {
        sentiment:
          extracted.sentiment === null
            ? ""
            : extracted.sentiment.toLowerCase(),
      }),
    }));



    if (!data.confirmation_question) {

    setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "✅ Interaction logged successfully. I’ve filled in the details on the left.",
        },
      ]);
    }

    setMessage("");
  } catch (err) {
    console.error("SEND MESSAGE FAILED:", err);
    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        text: "⚠️ Something went wrong while logging the interaction.",
      },
    ]);
  } finally {
    setLoading(false);
  }
}


  return (
    <div style={styles.app}>
      {/* LEFT: FORM */}
      <div style={styles.left}>
        <h2>Log HCP Interaction</h2>

        <section style={styles.card}>
          <h4>Interaction Details</h4>

          <Field label="HCP Name" value={formData.hcp_name} />

          <Field
            label="Interaction Type"
            value={formData.interaction_type}
          />

          <Row>
            <Field label="Date" value={formData.date} />
            <Field label="Time" value={formData.time} />
          </Row>

          <Field label="Attendees" value={formData.attendees} />

          <Field
            label="Topics Discussed"
            value={formData.topics}
            textarea
          />

          <button style={styles.secondaryBtn}>
            Summarize from Voice Note (Requires Consent)
          </button>
        </section>


        <section style={styles.card}>
          <h4>Observed / Inferred HCP Sentiment</h4>

          <div style={styles.radioRow}>
            {["positive", "neutral", "negative"].map((s) => (
              <label key={s}>
                <input
                  type="radio"
                  name="sentiment"
                  checked={formData.sentiment === s}
                  disabled
                />
                {s.charAt(0).toUpperCase() + s.slice(1)}
              </label>
            ))}
          </div>
        </section>



        <section style={styles.card}>
          <h4>Outcomes</h4>
          <textarea
            value={formData.outcomes || ""}
            disabled
            style={{
              ...styles.textarea,
              opacity: 0.7,
              cursor: "not-allowed",
            }}
          />

        </section>

        <section style={styles.card}>
          <h4>Follow-up Actions</h4>
          <textarea
            value={formData.follow_up_actions || ""}
            disabled
            style={{
              ...styles.textarea,
              opacity: 0.7,
              cursor: "not-allowed",
            }}
          />

        </section>
      </div>

      {/* RIGHT: AI ASSISTANT */}
      <div style={styles.right}>
        <div style={styles.assistantHeader}>
          🤖 AI Assistant
          <div style={styles.subtle}>Log interaction via chat</div>
        </div>

        <div style={styles.tipCard}>
          Log interaction details here (e.g.  
          “Met Dr. Smith, discussed Product X efficacy, positive sentiment,
          shared brochure”) or ask for help.
        </div>

        <div style={styles.chat}>
          {messages.map((m, i) => (
            <div
              key={i}
              style={{
                ...styles.bubble,
                alignSelf: m.role === "user" ? "flex-end" : "flex-start",
                background: m.role === "user" ? "#2563eb" : "#1f2933",
                color: "#fff",
              }}
            >
              {m.text}
            </div>
          ))}

          {messages.length === 0 && (
            <div style={styles.placeholder}>
              Start typing to log an interaction…
            </div>
          )}
        </div>

        <div style={styles.inputBar}>
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Describe interaction..."
            style={styles.input}
          />
          <button
            onClick={() => {
              console.log("LOG CLICKED");
              sendMessage();
            }}
            style={styles.primaryBtn}
          >
            Log
          </button>

        </div>
      </div>
    </div>
  );
}

/* ------------------ SMALL COMPONENTS ------------------ */

function Field({ label, value = "", textarea }) {
  return (
    <div style={{ marginBottom: 10 }}>
      <label style={styles.label}>{label}</label>

      {textarea ? (
        <textarea
          value={value}
          disabled
          style={{
            ...styles.textarea,
            opacity: 0.7,
            cursor: "not-allowed",
          }}
        />
      ) : (
        <input
          value={value}
          disabled
          style={{
            ...styles.input,
            opacity: 0.7,
            cursor: "not-allowed",
          }}
        />
      )}
    </div>
  );
}



function Row({ children }) {
  return <div style={{ display: "flex", gap: 12 }}>{children}</div>;
}

/* ------------------ STYLES ------------------ */

const styles = {
  app: {
    display: "grid",
    gridTemplateColumns: "2.3fr 1fr",
    height: "100vh",
    background: "#0b0f19",
    color: "#e5e7eb",
    fontFamily: "Inter, sans-serif",
  },

  /* LEFT */
  left: {
    padding: 24,
    overflowY: "auto",
  },

  /* RIGHT */
  right: {
    padding: 16,
    display: "flex",
    flexDirection: "column",
    borderLeft: "1px solid #1f2937",
    background: "#0f172a",
    height: "100vh",
    overflow: "hidden", // 🔒 important
  },


  card: {
    background: "#111827",
    borderRadius: 10,
    padding: 16,
    marginBottom: 16,
    border: "1px solid #1f2937",
  },

  label: {
    fontSize: 12,
    color: "#9ca3af",
    marginBottom: 4,
    display: "block",
  },

  input: {
    boxSizing: "border-box",
    width: "100%",
    height: 38,
    padding: "0 10px",
    borderRadius: 6,
    background: "#020617",
    border: "1px solid #1f2937",
    color: "#e5e7eb",
    outline: "none",
  },

  textarea: {
    boxSizing: "border-box",
    width: "100%",
    minHeight: 70,
    padding: 8,
    borderRadius: 6,
    background: "#020617",
    border: "1px solid #1f2937",
    color: "#e5e7eb",
    outline: "none",
    resize: "vertical",
  },


  radioRow: {
    display: "flex",
    gap: 16,
    color: "#e5e7eb",
  },

  assistantHeader: {
    fontWeight: 600,
    marginBottom: 4,
  },

  subtle: {
    fontSize: 12,
    color: "#9ca3af",
  },

  tipCard: {
    background: "#020617",
    border: "1px dashed #1f2937",
    padding: 12,
    borderRadius: 8,
    fontSize: 13,
    marginBottom: 12,
    color: "#c7d2fe",
  },

  chat: {
    flex: 1,
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: 8,
    padding: 8,
    background: "#020617",
    borderRadius: 8,
    border: "1px solid #1f2937",
  },

  bubble: {
    padding: "8px 12px",
    borderRadius: 14,
    maxWidth: "85%",
    fontSize: 13,
    lineHeight: 1.4,
  },

  placeholder: {
    fontSize: 13,
    color: "#64748b",
  },

  inputBar: {
    display: "flex",
    gap: 8,
    marginTop: 8,
  },

  primaryBtn: {
    background: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: 6,
    padding: "0 16px",
    fontWeight: 600,
    cursor: "pointer",
  },

  secondaryBtn: {
    marginTop: 8,
    fontSize: 12,
    padding: "6px 10px",
    borderRadius: 6,
    border: "1px solid #1f2937",
    background: "#020617",
    color: "#e5e7eb",
    cursor: "pointer",
  },
};

export default App;

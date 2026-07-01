import os
import time
import psycopg2
from flask import Flask, request, jsonify

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = Flask(__name__)

MODEL_PATH = "/workspace/model"

print("\n=== ⚙️ STARTING TRANSFORMER ROUTING BACKEND ===\n")
print(f"--> Initializing Transformer Routing Engine... Loading weights from: {MODEL_PATH}")

# Global model pointers
tokenizer = None
model = None

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()  # Set layers to evaluation mode (disables dropout/batchnorm updates)
    print("--> ✅ Transformer Engine active and listening for text streams!")
except Exception as e:
    print(f"--> ❌ CRITICAL ERROR: Failed to load model weights. Pipeline running on keyword fallback.")
    print(f"    Details: {e}\n")


def get_db_connection():
    """Establishes an atomic connection to the PostgreSQL cluster using container environment variables."""
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "alert_db"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "secret123"),
        connect_timeout=5
    )


def init_db():
    """Verifies relational database structural tables and seeds primary profile components on startup."""
    print("--> Connecting to PostgreSQL service to verify schema architecture...")
    
    for attempt in range(5):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT,
                    interests TEXT,
                    location TEXT
                );
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tweets (
                    id SERIAL PRIMARY KEY,
                    user_id TEXT,
                    text TEXT,
                    classification TEXT,
                    location TEXT
                );
            """)
            
            cursor.execute("SELECT COUNT(*) FROM users;")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO users (user_id, name, interests, location) 
                    VALUES ('operator_1', 'System Operator', 'safety,alert,traffic', 'Bangalore');
                """)
                
            conn.commit()
            cursor.close()
            conn.close()
            print("--> 🗄️ Database tables verified, synchronized, and ready!")
            return
        except psycopg2.OperationalError as e:
            print(f"    [Attempt {attempt+1}/5] Database not fully up yet, waiting 2 seconds...")
            time.sleep(2)
            
    print("--> ⚠️ WARNING: Backend initialized without active database confirmation. Will attempt lazy evaluation on requests.")


@app.route('/submit_tweet', methods=['POST'])
def submit_tweet():
    """
    Intercepts unstructured social payloads, passes data sequences through the Transformer, 
    commits transactions to PostgreSQL, and returns an execution audit log array.
    """
    data = request.json or {}
    raw_text = data.get("text", "").strip()
    target_location = data.get("location", "Bangalore")
    
    if not raw_text:
        return jsonify({"status": "error", "error": "Empty text payload submitted."}), 400

    pipeline_logs = []
    
    pipeline_logs.append("📥 Ingestion Gateway: Intercepted raw text stream string.")
    time.sleep(0.3)  # Tiny micro-delay to allow visual steps to render neatly in the UI
    
    pipeline_logs.append("🤖 ML Pipeline: Splitting sequences into tokens and preparing tensor forward pass...")
    
    classification_result = "UNKNOWN"
    
    if model is not None and tokenizer is not None:
        try:
            inputs = tokenizer(raw_text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            
            with torch.no_grad():
                outputs = model(**inputs)
            
            logits = outputs.logits
            print(f"\n🔮 [DEBUG] Raw Logits Shape: {logits.shape} | Tensor Values: {logits.tolist()}")
            
            predicted_class_id = torch.argmax(logits, dim=1).item()
            
            labels_map = {0: "NON-ALERT", 1: "ALERT"}
            classification_result = labels_map.get(predicted_class_id, "UNKNOWN")
            
                
            pipeline_logs.append(f"✅ Inference System: Tensor evaluation complete. Label output: [{classification_result}]")
            
        except Exception as inference_err:
            pipeline_logs.append(f"❌ Tensor Engine Failure: {str(inference_err)}. Reverting to rule fallback.")
            classification_result = "ALERT" if any(w in raw_text.lower() for w in ["emergency", "accident", "crash", "alert"]) else "NON-ALERT"
    else:
        pipeline_logs.append("⚠️ System Warning: Active weights missing. Deploying structural keyword heuristic parser.")
        classification_result = "ALERT" if any(w in raw_text.lower() for w in ["emergency", "accident", "crash", "alert"]) else "NON-ALERT"
        time.sleep(0.5)

    pipeline_logs.append("🗄️ Database Hub: Connecting to PostgreSQL cluster to log operational transactions...")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO tweets (user_id, text, classification, location) 
            VALUES (%s, %s, %s, %s) RETURNING id;
            """,
            ('operator_1', raw_text, classification_result, target_location)
        )
        
        record_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        pipeline_logs.append(f"💾 Storage Engine: Transaction locked. Written to 'tweets' table under ID: {record_id}")
        pipeline_logs.append(f"⚡ Feed Dispatcher: Routed classification to active stream panels in [{target_location}].")
        
        return jsonify({
            "status": "success",
            "classification": classification_result,
            "logs": pipeline_logs
        }), 200

    except Exception as db_err:
        pipeline_logs.append(f"❌ Data Warehouse Error: Transaction aborted. Details: {str(db_err)}")
        return jsonify({
            "status": "error",
            "error": str(db_err),
            "logs": pipeline_logs
        }), 500

@app.route('/get_feeds', methods=['GET'])
def get_feeds():
    """Queries persistent PostgreSQL tables to extract sorted, filtered text alerts for dashboard display panels."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, text, classification, location FROM tweets ORDER BY id DESC;")
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        feed_payload = [
            {
                "id": row[0],
                "text": row[1],
                "classification": row[2],
                "location": row[3]
            } for row in rows
        ]
        return jsonify(feed_payload), 200
        
    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

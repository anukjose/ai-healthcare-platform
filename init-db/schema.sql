CREATE TABLE patient_lab_history (
   id BIGSERIAL PRIMARY KEY,
   patient_id TEXT NOT NULL,
   test TEXT NOT NULL,
   date DATE NOT NULL,
   value DOUBLE PRECISION NOT NULL,
   unit TEXT NOT NULL,
   source TEXT,
   created_at TIMESTAMP DEFAULT now(),
   updated_at TIMESTAMP DEFAULT now(),

   UNIQUE (patient_id, test, date)
);

CREATE INDEX idx_plh_patient_test_date
ON patient_lab_history (patient_id, test, date DESC);


CREATE TABLE patient_lab_summary (
   patient_id TEXT NOT NULL,
   test TEXT NOT NULL,

   latest_value DOUBLE PRECISION,
   trend TEXT,
   min_value DOUBLE PRECISION,
   max_value DOUBLE PRECISION,

   last_updated DATE,

   PRIMARY KEY (patient_id, test)
);


CREATE TABLE patient_chunks (
   id BIGSERIAL PRIMARY KEY,

   patient_id TEXT NOT NULL,
   chunk_type TEXT,
   content TEXT NOT NULL,

   embedding VECTOR(1536),

   created_at TIMESTAMP DEFAULT now()
);
import glob
import re
import numpy as np
import pandas as pd

# ============================================================
# LOAD DATA
# ============================================================

df_notices = pd.concat(
    [pd.read_csv(f) for f in sorted(glob.glob("notices/*.csv"))],
    ignore_index=True
)

df_labels = pd.read_csv("labelled_pairs.csv")

notices_dict = df_notices.set_index("notice_id").to_dict(orient="index")

print("=" * 70)
print("Q2(a) - SIMILARITY DEFINITION")
print("=" * 70)

print(f"Loaded {len(df_notices)} notices")
print(f"Portals: {df_notices['portal_id'].nunique()}")
print(f"Labelled pairs: {len(df_labels)}")
print(f"Same: {(df_labels['label'] == 'same').sum()}")
print(f"Different: {(df_labels['label'] == 'different').sum()}")


# ============================================================
# REMOVE PORTAL BOILERPLATE
# ============================================================

def strip_portal_boilerplate(body):

    text = re.sub(
        r'GOVERNMENT OF INDIA -- NATIONAL PROCUREMENT AGGREGATION SERVICE.*?NOTICE DETAILS FOLLOW\s*-+',
        '',
        body,
        flags=re.DOTALL
    )

    text = re.sub(
        r'-+\s*Disclaimer: this entry is reproduced by the aggregation service.*',
        '',
        text,
        flags=re.DOTALL
    )

    text = re.sub(
        r'STATE PROCUREMENT CELL -- CONSOLIDATED TENDER BULLETIN.*?={10,}',
        '',
        text,
        flags=re.DOTALL
    )

    return text


# ============================================================
# WORD 3-SHINGLES
# ============================================================

def tokenize_clean(title, body, k=3):

    clean_body = strip_portal_boilerplate(body)

    full = f"{title} {clean_body}"

    # Mask reference numbers
    full = re.sub(
        r'(?:Tender reference number|reference number|ref)[:\s]+[A-Za-z0-9/_-]+',
        ' ',
        full,
        flags=re.IGNORECASE
    )

    # Mask monetary values
    full = re.sub(
        r'(?:Rs\.?|INR|RUPEES)\s*[\d,]+(?:\.\d+)?(?:\s*(?:lakh|Cr|Crore|ONLY|/-))?',
        ' ',
        full,
        flags=re.IGNORECASE
    )

    # Mask dates
    full = re.sub(
        r'\b\d{1,2}[-/.](?:\d{1,2}|[A-Za-z]{3})[-/.]\d{2,4}\b',
        ' ',
        full
    )

    words = re.findall(r'\b[a-z0-9]+\b', full.lower())

    if len(words) < k:
        return set(words)

    return set(
        ' '.join(words[i:i+k])
        for i in range(len(words) - k + 1)
    )


# ============================================================
# JACCARD SIMILARITY
# ============================================================

def jaccard(a, b):

    if not a or not b:
        return 0.0

    return len(a & b) / len(a | b)


# ============================================================
# EVALUATE LABELLED PAIRS
# ============================================================

same_scores = []
different_scores = []

for _, row in df_labels.iterrows():

    notice_a = notices_dict[row["notice_id_a"]]
    notice_b = notices_dict[row["notice_id_b"]]

    shingles_a = tokenize_clean(
        notice_a["title"],
        notice_a["body"]
    )

    shingles_b = tokenize_clean(
        notice_b["title"],
        notice_b["body"]
    )

    score = jaccard(shingles_a, shingles_b)

    if row["label"] == "same":
        same_scores.append(score)
    else:
        different_scores.append(score)


# ============================================================
# RESULTS
# ============================================================

print("\nSimilarity results using cleaned word 3-shingles:")

print(
    f"Same pairs     : Mean={np.mean(same_scores):.4f}, "
    f"Min={np.min(same_scores):.4f}, "
    f"Max={np.max(same_scores):.4f}"
)

print(
    f"Different pairs: Mean={np.mean(different_scores):.4f}, "
    f"Min={np.min(different_scores):.4f}, "
    f"Max={np.max(different_scores):.4f}"
)

print(
    f"\nSeparation check:"
)

print(
    f"Max(Different) = {np.max(different_scores):.4f}"
)

print(
    f"Mean(Same) = {np.mean(same_scores):.4f}"
)

print("=" * 70)
# ============================================================
# Q2(b) - MINHASH APPROXIMATE SIMILARITY
# ============================================================

print("\n" + "=" * 70)
print("Q2(b) - MINHASH SKETCH")
print("=" * 70)

K = 128

MERSENNE_PRIME = (1 << 61) - 1

np.random.seed(42)

hash_a = np.random.randint(1, 10000000, size=K, dtype=np.int64)
hash_b = np.random.randint(0, 10000000, size=K, dtype=np.int64)


def string_hash(s):
    return hash(s) & 0x7FFFFFFF


shingle_cache = {}
signature_cache = {}


def get_shingles(notice_id):

    if notice_id not in shingle_cache:

        notice = notices_dict[notice_id]

        shingle_cache[notice_id] = tokenize_clean(
            notice["title"],
            notice["body"]
        )

    return shingle_cache[notice_id]


def get_minhash(notice_id):

    if notice_id not in signature_cache:

        shingles = get_shingles(notice_id)

        if not shingles:
            signature_cache[notice_id] = np.zeros(
                K,
                dtype=np.uint32
            )

        else:

            hashed = np.array(
                [string_hash(s) for s in shingles],
                dtype=np.int64
            )

            values = (
                hash_a[:, None] * hashed[None, :]
                + hash_b[:, None]
            ) % MERSENNE_PRIME

            signature_cache[notice_id] = (
                np.min(values, axis=1) & 0xFFFFFFFF
            ).astype(np.uint32)

    return signature_cache[notice_id]


# Compare exact Jaccard with MinHash estimate

exact_scores = []
estimated_scores = []
errors = []

for _, row in df_labels.iterrows():

    a = row["notice_id_a"]
    b = row["notice_id_b"]

    exact = jaccard(
        get_shingles(a),
        get_shingles(b)
    )

    sig_a = get_minhash(a)
    sig_b = get_minhash(b)

    estimated = np.mean(sig_a == sig_b)

    exact_scores.append(exact)
    estimated_scores.append(estimated)
    errors.append(estimated - exact)


exact_scores = np.array(exact_scores)
estimated_scores = np.array(estimated_scores)
errors = np.array(errors)


print(f"MinHash signature size: K = {K}")
print(f"Signature storage per notice: {K * 4} bytes")
print(f"Total for 12,000 notices: {12000 * K * 4 / (1024**2):.2f} MB")

print("\nError against labelled_pairs.csv:")

print(f"Mean Bias          : {np.mean(errors):+.5f}")
print(f"Mean Absolute Error: {np.mean(np.abs(errors)):.4f}")
print(f"RMSE               : {np.sqrt(np.mean(errors ** 2)):.4f}")
print(f"Maximum Error      : {np.max(np.abs(errors)):.4f}")

print("=" * 70)
# ============================================================
# Q2(c) - LSH CANDIDATE GENERATION
# ============================================================

print("\n" + "=" * 70)
print("Q2(c) - LSH CANDIDATE GENERATION")
print("=" * 70)

# 128 MinHash values = 32 bands × 4 rows
b = 32
r = 4

threshold = (1 / b) ** (1 / r)

print(f"MinHash values K = {K}")
print(f"LSH bands       = {b}")
print(f"Rows per band   = {r}")
print(f"b × r           = {b * r}")
print(f"Theoretical threshold ≈ {threshold:.4f}")


def probability_of_retrieval(s):
    return 1 - (1 - s ** r) ** b


print("\nCandidate survival probability:")

for s in [0.20, 0.30, 0.42, 0.55, 0.60, 0.65, 0.80, 0.95]:

    p = probability_of_retrieval(s)

    print(
        f"Similarity {s:.2f} -> "
        f"P(candidate) = {p:.4f} ({p * 100:.1f}%)"
    )


print("\nOperating point:")

p60 = probability_of_retrieval(0.60)
p25 = probability_of_retrieval(0.25)

print(
    f"At similarity 0.60: "
    f"{p60:.4f} ({p60 * 100:.1f}%)"
)

print(
    f"At similarity 0.25: "
    f"{p25:.4f} ({p25 * 100:.1f}%)"
)

print("=" * 70)
# ============================================================
# Q2(d) - RELATIONAL STORAGE AND ACCESS PATH
# ============================================================

import sqlite3
import time
import os

print("\n" + "=" * 70)
print("Q2(d) - RELATIONAL SCHEMA & ACCESS PATH")
print("=" * 70)

db_file = "setubid_lsh.db"

if os.path.exists(db_file):
    os.remove(db_file)

conn = sqlite3.connect(db_file)
cur = conn.cursor()

# LSH bucket table
cur.execute("""
CREATE TABLE lsh_buckets (
    band_id INTEGER NOT NULL,
    bucket_hash INTEGER NOT NULL,
    notice_id TEXT NOT NULL
)
""")

# MinHash signature table
cur.execute("""
CREATE TABLE notice_signatures (
    notice_id TEXT PRIMARY KEY,
    signature BLOB NOT NULL
)
""")

# Populate tables
all_nids = df_notices["notice_id"].tolist()

bucket_rows = []
signature_rows = []

for nid in all_nids:

    sig = get_minhash(nid)

    signature_rows.append(
        (nid, sig.tobytes())
    )

    for band_id in range(b):

        band = sig[
            band_id * r:
            (band_id + 1) * r
        ]

        bucket_hash = hash(
            band.tobytes()
        ) & 0x7FFFFFFFFFFFFFFF

        bucket_rows.append(
            (band_id, bucket_hash, nid)
        )

cur.executemany(
    "INSERT INTO notice_signatures VALUES (?, ?)",
    signature_rows
)

cur.executemany(
    "INSERT INTO lsh_buckets VALUES (?, ?, ?)",
    bucket_rows
)

conn.commit()

print(f"Notices stored: {len(signature_rows):,}")
print(f"LSH bucket rows: {len(bucket_rows):,}")


# ------------------------------------------------------------
# Candidate lookup
# ------------------------------------------------------------

lookup_sql = """
SELECT DISTINCT b2.notice_id
FROM lsh_buckets b1
JOIN lsh_buckets b2
  ON b1.band_id = b2.band_id
 AND b1.bucket_hash = b2.bucket_hash
WHERE b1.notice_id = ?
  AND b2.notice_id != ?
"""


# ------------------------------------------------------------
# Before index
# ------------------------------------------------------------

print("\nBefore indexing:")

plan_before = cur.execute(
    "EXPLAIN QUERY PLAN " + lookup_sql,
    ("N000001", "N000001")
).fetchall()

for row in plan_before:
    print(row[3])


sample_nids = all_nids[:5]

start = time.time()

for nid in sample_nids:
    cur.execute(
        lookup_sql,
        (nid, nid)
    ).fetchall()

scan_time = time.time() - start

print(
    f"5 lookups: {scan_time:.4f} seconds"
)


# ------------------------------------------------------------
# Composite B-tree index
# ------------------------------------------------------------

print("\nCreating composite B-tree index...")

start = time.time()

cur.execute("""
CREATE INDEX idx_band_bucket
ON lsh_buckets (band_id, bucket_hash)
""")

conn.commit()

index_time = time.time() - start

print(
    f"Index creation time: {index_time:.4f} seconds"
)


# ------------------------------------------------------------
# After index
# ------------------------------------------------------------

print("\nAfter indexing:")

plan_after = cur.execute(
    "EXPLAIN QUERY PLAN " + lookup_sql,
    ("N000001", "N000001")
).fetchall()

for row in plan_after:
    print(row[3])


start = time.time()

for nid in sample_nids:
    cur.execute(
        lookup_sql,
        (nid, nid)
    ).fetchall()

indexed_time = time.time() - start

print(
    f"5 indexed lookups: {indexed_time:.4f} seconds"
)

if indexed_time > 0:
    print(
        f"Measured speedup: "
        f"{scan_time / indexed_time:.2f}x"
    )

print("\nAccess method: Composite B-tree")
print("Indexed columns: band_id, bucket_hash")
print("Reason: candidate lookup searches directly for matching")
print("band/bucket keys instead of scanning the entire bucket table.")

print("=" * 70)


# ============================================================
# Q2(e) - SKEW ANALYSIS AND MITIGATION
# ============================================================

import math

print("\n" + "=" * 70)
print("Q2(e) - EMPIRICAL SKEW & MITIGATION")
print("=" * 70)

# ------------------------------------------------------------
# Bucket distribution
# ------------------------------------------------------------

bucket_distribution = cur.execute("""
SELECT band_id, bucket_hash, COUNT(*) AS cnt
FROM lsh_buckets
GROUP BY band_id, bucket_hash
ORDER BY cnt DESC
""").fetchall()

max_bucket_size = bucket_distribution[0][2]

print(
    f"Largest single bucket size: {max_bucket_size:,} notices"
)

print(
    "Top 5 largest bucket sizes:",
    [x[2] for x in bucket_distribution[:5]]
)


# ------------------------------------------------------------
# Candidate workload WITHOUT mitigation
# ------------------------------------------------------------

uncapped = cur.execute("""
SELECT SUM(cnt * (cnt - 1) / 2)
FROM (
    SELECT COUNT(*) AS cnt
    FROM lsh_buckets
    GROUP BY band_id, bucket_hash
)
""").fetchone()[0]

print(
    f"\nUncapped candidate pair comparisons: {uncapped:,.0f}"
)


# ------------------------------------------------------------
# Apply bucket-size cap
# ------------------------------------------------------------

C_MAX = 50

capped = cur.execute(f"""
SELECT SUM(cnt * (cnt - 1) / 2)
FROM (
    SELECT COUNT(*) AS cnt
    FROM lsh_buckets
    GROUP BY band_id, bucket_hash
    HAVING COUNT(*) <= {C_MAX}
)
""").fetchone()[0]

print(
    f"Capped candidate comparisons: {capped:,.0f}"
)

reduction = 1 - (capped / uncapped)

print(
    f"Candidate workload reduction: "
    f"{reduction * 100:.2f}%"
)


# ------------------------------------------------------------
# Retrieve candidates after capping
# ------------------------------------------------------------

capped_pairs = cur.execute(f"""
WITH valid_buckets AS (
    SELECT band_id, bucket_hash
    FROM lsh_buckets
    GROUP BY band_id, bucket_hash
    HAVING COUNT(*) <= {C_MAX}
)

SELECT DISTINCT
    b1.notice_id,
    b2.notice_id

FROM lsh_buckets b1

JOIN valid_buckets vb
  ON b1.band_id = vb.band_id
 AND b1.bucket_hash = vb.bucket_hash

JOIN lsh_buckets b2
  ON b1.band_id = b2.band_id
 AND b1.bucket_hash = b2.bucket_hash

WHERE b1.notice_id < b2.notice_id
""").fetchall()


capped_set = {
    tuple(sorted(pair))
    for pair in capped_pairs
}


# ------------------------------------------------------------
# Recall against labelled true duplicates
# ------------------------------------------------------------

same_pairs = {
    tuple(sorted([
        row["notice_id_a"],
        row["notice_id_b"]
    ]))
    for _, row in df_labels[
        df_labels["label"] == "same"
    ].iterrows()
}


found_same = same_pairs & capped_set

recall = len(found_same) / len(same_pairs)

print("\nLabelled duplicate recall after mitigation:")

print(
    f"True duplicate pairs: {len(same_pairs)}"
)

print(
    f"Duplicates retrieved: {len(found_same)}"
)

print(
    f"Recall: {recall * 100:.2f}%"
)

print(
    f"Recall loss: {(1 - recall) * 100:.2f}%"
)


# ------------------------------------------------------------
# Portal skew information
# ------------------------------------------------------------

print("\nPortal volume information from portal_profiles.md:")

print("P094 = 1,426 notices")
print("P002 = 800")
print("P006 = 792")
print("P001 = 778")
print("P003 = 772")
print("P005 = 768")

print("\nMitigation:")
print(
    f"Buckets containing more than {C_MAX} notices "
    "are excluded from pair generation."
)

print("=" * 70)
# ============================================================
# Q2(e) - SKEW ANALYSIS AND MITIGATION
# ============================================================

print("\n" + "=" * 70)
print("Q2(e) - EMPIRICAL SKEW & MITIGATION")
print("=" * 70)


# ------------------------------------------------------------
# 1. Analyze LSH bucket distribution
# ------------------------------------------------------------

bucket_distribution = cur.execute("""
SELECT
    band_id,
    bucket_hash,
    COUNT(*) AS cnt
FROM lsh_buckets
GROUP BY band_id, bucket_hash
ORDER BY cnt DESC
""").fetchall()

max_bucket_size = bucket_distribution[0][2]

print(
    f"Largest single bucket size: "
    f"{max_bucket_size:,} notices"
)

print(
    "Top 5 largest bucket sizes:",
    [x[2] for x in bucket_distribution[:5]]
)


# ------------------------------------------------------------
# 2. Calculate workload without mitigation
# ------------------------------------------------------------

uncapped_pairs_count = cur.execute("""
SELECT SUM(cnt * (cnt - 1) / 2)
FROM (
    SELECT COUNT(*) AS cnt
    FROM lsh_buckets
    GROUP BY band_id, bucket_hash
)
""").fetchone()[0]

print(
    f"\nUncapped candidate pair comparisons: "
    f"{uncapped_pairs_count:,.0f}"
)


# ------------------------------------------------------------
# 3. Apply bucket-size cap
# ------------------------------------------------------------

C_MAX = 50

capped_pairs_count = cur.execute(f"""
SELECT SUM(cnt * (cnt - 1) / 2)
FROM (
    SELECT COUNT(*) AS cnt
    FROM lsh_buckets
    GROUP BY band_id, bucket_hash
    HAVING COUNT(*) <= {C_MAX}
)
""").fetchone()[0]

print(
    f"Capped candidate comparisons: "
    f"{capped_pairs_count:,.0f}"
)


# ------------------------------------------------------------
# 4. Workload reduction
# ------------------------------------------------------------

reduction = (
    1.0 -
    capped_pairs_count / uncapped_pairs_count
)

print(
    f"Candidate workload reduction: "
    f"{reduction * 100:.2f}%"
)


# ------------------------------------------------------------
# 5. Generate candidates after mitigation
# ------------------------------------------------------------

capped_pairs = cur.execute(f"""
WITH valid_buckets AS (
    SELECT
        band_id,
        bucket_hash
    FROM lsh_buckets
    GROUP BY band_id, bucket_hash
    HAVING COUNT(*) <= {C_MAX}
)

SELECT DISTINCT
    b1.notice_id,
    b2.notice_id

FROM lsh_buckets b1

JOIN valid_buckets vb
    ON b1.band_id = vb.band_id
   AND b1.bucket_hash = vb.bucket_hash

JOIN lsh_buckets b2
    ON b1.band_id = b2.band_id
   AND b1.bucket_hash = b2.bucket_hash

WHERE b1.notice_id < b2.notice_id
""").fetchall()


capped_norm = {
    tuple(sorted(pair))
    for pair in capped_pairs
}


# ------------------------------------------------------------
# 6. Evaluate recall using labelled_pairs.csv
# ------------------------------------------------------------

same_pairs_set = {
    tuple(sorted([
        row["notice_id_a"],
        row["notice_id_b"]
    ]))
    for _, row in df_labels[
        df_labels["label"] == "same"
    ].iterrows()
}

retrieved_same = same_pairs_set & capped_norm

recall = (
    len(retrieved_same) /
    len(same_pairs_set)
)

print(
    "\nRetrieval Quality on labelled_pairs.csv:"
)

print(
    f"True duplicate pairs: "
    f"{len(same_pairs_set)}"
)

print(
    f"Duplicates retrieved: "
    f"{len(retrieved_same)}"
)

print(
    f"Recall after mitigation: "
    f"{recall * 100:.2f}%"
)

print(
    f"Recall loss: "
    f"{(1 - recall) * 100:.2f}%"
)


# ------------------------------------------------------------
# 7. Portal skew information
# ------------------------------------------------------------

print(
    "\nPortal volume information from portal_profiles.md:"
)

print("P094 = 1,426 notices")
print("P002 = 800 notices")
print("P006 = 792 notices")
print("P001 = 778 notices")
print("P003 = 772 notices")
print("P005 = 768 notices")


# ------------------------------------------------------------
# 8. Mitigation summary
# ------------------------------------------------------------

print("\nMitigation:")
print(
    f"Buckets containing more than {C_MAX} notices "
    "are excluded from pair generation."
)

print("=" * 70)

# Close database only AFTER Q2(e)
conn.close()

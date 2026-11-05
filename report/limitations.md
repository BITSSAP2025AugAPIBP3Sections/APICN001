# Limitations — APICN001

## Retrieval
- **Lexical only.** The retriever is BM25, not semantic. A question that uses
  different words from the corpus (e.g. "crypto" when the Act says "virtual
  digital asset") can miss relevant chunks. We mitigate this with a tax-aware
  stopword list, but true synonym matching would need embeddings.
- **No reranking.** We take the top-k BM25 hits directly. A cross-encoder reranker
  would improve precision on the medium/complex questions but adds CPU latency we
  chose not to pay by default.
- **Year scoping is implicit.** The corpus spans FY 2022-23 to 2025-26. Retrieval
  surfaces the best lexical match regardless of year, so a question that pins a
  specific FY can occasionally pull a chunk from a neighbouring budget. The model
  is prompted to state its assumptions, but it does not hard-filter by year.

## Generation
- **Computation is the model's weak spot.** For the complex questions (slab-by-slab
  tax with surcharge and cess), the SLM sometimes makes arithmetic slips even when
  it retrieves the correct rates. Larger cloud providers (Groq 70B) are markedly
  more reliable here than a local 3B-class SLM.
- **Citation fidelity varies.** The model cites the document and page it was given,
  but on long answers it occasionally attributes a claim to the wrong one of the
  retrieved chunks.

## Speech
- **STT on homophones.** faster-whisper `base` mishears rupee figures and section
  numbers ("one fifteen BBH" vs "115BBH"); a larger Whisper size fixes this at a
  latency cost.
- **TTS is not truly streaming.** We chunk by sentence pairs so audio starts early,
  but each chunk is still synthesised in full before it plays; token-level
  streaming would lower first-audio latency further.

## Scope
- The bot answers only from the committed corpus. Questions whose answer is not in
  `data/` are refused by design, not answered from general knowledge.

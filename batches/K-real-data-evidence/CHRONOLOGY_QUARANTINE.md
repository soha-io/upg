# Batch K chronology quarantine

Status: **active; legacy Kossakowski conclusions must not be used**.

The original retrospective script grouped and sorted observations by
`dayno`, a day-of-year integer, across calendar years 2012 and 2013. This
placed January--April 2013 before August--December 2012, merged equal
day-of-year values, created a false April-to-August transition, removed the
real December-to-January transition, and allowed later-calendar observations
to enter earlier rolling histories. It also called every consecutive
depression anchor "next week" although observed gaps include 7, 14, and 21
days.

All existing chronology-dependent files are byte-preserved as an audit
fixture and registered in `chronology_quarantine.json`. They are **not current
evidence**. This includes the legacy ESM summary, forecast, plot, manuscript,
DOCX, self-contained report, and claim ledger wherever they repeat those
numbers. Standalone IPIP tables remain usable, but the mixed
`real_data_summary.json` is quarantined as a whole. One separate measurement
correction also applies: the legacy IPIP table's
`reliability_derived_measurement_sd` is not the conventional observed-score
SEM and must not be used as one; the corrected code computes
`observed_sd * sqrt(1 - alpha)`. Alpha and facet-structure results are
unaffected.

The repaired script:

- parses the source `date` as day/month/year and checks it against `dayno`;
- groups, windows, and sorts on full calendar dates;
- rejects non-monotonic anchor sequences;
- records source date, target date, and exact `horizon_days` on every forecast;
- estimates AR(1) only from finite observed consecutive-day $t-1\rightarrow t$
  pairs, requires at least eight such pairs, and reports the pair count;
- reports 7/14/21-day forecasts by exact horizon rather than calling all of
  them "next week";
- writes to the new versioned namespace
  `results/real_data_corrected/v3_calendar/` by default through a hidden
  temporary run; it hashes inputs and helper code, writes a completion
  manifest last, and atomically publishes only to a nonexistent destination.
  No override can write within frozen `results/real_data/` or
  `evidence/audit/` namespaces.

No corrected scientific result was generated during pre-study hardening. A
future registered rerun must independently verify the corrected artifacts
before any Kossakowski claim is restored.

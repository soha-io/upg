# Transformer Sources — Reading Notes for Phase 2 (Steps 4–6)

46 notes, one per paper in `8-Dimention Model Sources/12. Transformers/`.
Each note gives the paper's core mathematics in project notation, then answers
one question: **what does this buy the UPG estimation pipeline?**

## Shared notation (used in every note)

| Symbol | Meaning |
|---|---|
| $n=7$ | endogenous dimensions (TEM, DEV, PER, NEED, ME, DIS, SYS) |
| $x_t \in \mathbb{R}^n$ | true latent activation at occasion $t$ |
| $y_t$ | noisy, partially missing EMA observation of $x_t$ |
| $B$ | signed weighted coupling matrix, $B[\text{target},\text{source}]$ |
| $\bar B$ | consensus prior (the published skeleton + weights) |
| $M$ | skeleton mask, $M_{ij} = \mathbb{1}[\bar B_{ij} \ne 0]$ (rule W1) |
| $\kappa,\; g,\; b,\; u_t$ | global coupling, treatment gains, standing conditions, treatment input |
| generative map | $x_{t+1} = \tanh\!\big(\kappa(Bx_t + g u_t) + b + \varepsilon_t\big)$ |
| $\rho(J)$ | spectral radius of the Jacobian at the attractor (early-warning quantity) |
| $\kappa^\* = 1/\lambda_{\max}(B)$ | bifurcation threshold |

Attention notation: queries $Q = XW_Q$, keys $K = XW_K$, values $V = XW_V$;
$\mathrm{Attn}(X) = \mathrm{softmax}\!\big(QK^\top/\sqrt{d_k}\big)V$.

## How the 46 papers map onto the three Phase-2 steps

| Family | Papers | Feeds |
|---|---|---|
| Core architecture | 01–07 | background for steps 5–6; what attention *is* |
| Graphs + structured attention | 08–12 | **step 5** (structure-constrained GAT) |
| Time-series transformers | 13–22 | **step 6** forecaster design |
| Efficiency | 23–28 | why we *don't* need them at $n=7$, and when we will |
| Modern components | 29–34 | block choices for the step-6 model |
| Scaling + theory | 35–42 | data budgets, identifiability, "attention as estimator" |
| State-space alternatives | 43–46 | the deep model closest to our generative map |

## The single most important sentence per family

1. **Core (01–07):** attention is a data-dependent weighted average — a
   *learned, time-varying* analogue of our fixed $B$ row.
2. **Graphs (08–12):** attention can be masked to a known graph, so learned
   attention coefficients on the UPG skeleton *are* edge-weight estimates
   $\hat w_{ij}$ — the mathematical license for step 5.
3. **Time series (13–22):** the field converged on our problem shape
   (multivariate, irregular, long-horizon), and the two winning tricks —
   variables-as-tokens (iTransformer) and patching (PatchTST) — both transfer.
4. **Efficiency (23–28):** quadratic attention costs nothing at $n=7$,
   $T \le 200$; these papers matter only at full 253-node resolution.
5. **Components (29–34):** RoPE/ALiBi give principled *relative-time* encoding
   for irregular EMA; RMSNorm/SwiGLU are the stable defaults; LoRA is the
   $\Delta W$ low-rank idea we already use conceptually in W7.
6. **Theory (35–42):** transformers implement regression inside their forward
   pass (von Oswald; Garg), which is exactly the sense in which "AI is the
   statistical instrument" — and rank collapse (37) warns why attention needs
   the other block parts.
7. **SSMs (43–46):** S4/Mamba are *literally* discretized linear dynamical
   systems — the same object as our iterated map — so they are the natural
   deep forecaster if attention underperforms, and paper 46 gives the
   selection criteria.

## Note index

| # | File | Paper | Priority | Step |
|---|---|---|---|---|
| 01 | `01_attention_is_all_you_need.md` | Vaswani et al. 2017 | high | 5,6 |
| 02 | `02_bert.md` | Devlin et al. 2019 | high | 6 (measurement) |
| 03 | `03_gpt_generative_pretraining.md` | Radford et al. 2018 | medium | 6 |
| 04 | `04_gpt3_few_shot.md` | Brown et al. 2020 | high | 6, theory |
| 05 | `05_t5_text_to_text.md` | Raffel et al. 2020 | medium | 6 |
| 06 | `06_roberta.md` | Liu et al. 2019 | medium | 6 (recipe) |
| 07 | `07_transformer_xl.md` | Dai et al. 2019 | high | 6 (long histories) |
| 08 | `08_graph_attention_networks.md` | Veličković et al. 2018 | high | **5 (core)** |
| 09 | `09_graphormer.md` | Ying et al. 2021 | high | 5 |
| 10 | `10_perceiver_io.md` | Jaegle et al. 2021 | medium | 6 (measurement) |
| 11 | `11_vit.md` | Dosovitskiy et al. 2021 | medium | 6 (tokenization) |
| 12 | `12_swin.md` | Liu et al. 2021 | medium | 5,6 (hierarchy) |
| 13 | `13_temporal_fusion_transformer.md` | Lim et al. 2021 | high | **6 (core)** |
| 14 | `14_informer.md` | Zhou et al. 2021 | high | 6 |
| 15 | `15_autoformer.md` | Wu et al. 2021 | high | 6 |
| 16 | `16_patchtst.md` | Nie et al. 2023 | high | 6 |
| 17 | `17_itransformer.md` | Liu et al. 2024 | high | **5+6 bridge** |
| 18 | `18_spacetimeformer.md` | Grigsby et al. 2021 | high | 5+6 rival |
| 19 | `19_sttn_traffic.md` | Xu et al. 2020 | medium | 5+6 analogy |
| 20 | `20_timesformer.md` | Bertasius et al. 2021 | medium | 6 (factorization) |
| 21 | `21_vivit.md` | Arnab et al. 2021 | medium | 6 (factorization) |
| 22 | `22_video_swin.md` | Liu et al. 2022 | medium | 6 (locality) |
| 23 | `23_flashattention.md` | Dao et al. 2022 | high | engineering |
| 24 | `24_longformer.md` | Beltagy et al. 2020 | medium | 6; bridge-node analogy |
| 25 | `25_reformer.md` | Kitaev et al. 2020 | medium | efficiency |
| 26 | `26_linformer.md` | Wang et al. 2020 | medium | low-rank dynamics |
| 27 | `27_performers.md` | Choromanski et al. 2021 | medium | kernel view |
| 28 | `28_switch_transformers.md` | Fedus et al. 2022 | medium | regime experts |
| 29 | `29_roformer_rope.md` | Su et al. 2021 | high | 6 (time encoding) |
| 30 | `30_alibi.md` | Press et al. 2022 | high | 6 (length extrapolation) |
| 31 | `31_rmsnorm.md` | Zhang & Sennrich 2019 | medium | 6 (block choice) |
| 32 | `32_glu_variants.md` | Shazeer 2020 | medium | 6 (block choice) |
| 33 | `33_lora.md` | Hu et al. 2022 | medium | W7 as low-rank ΔW |
| 34 | `34_qlora.md` | Dettmers et al. 2023 | medium | compute constraints |
| 35 | `35_scaling_laws.md` | Kaplan et al. 2020 | high | data budgets |
| 36 | `36_chinchilla.md` | Hoffmann et al. 2022 | high | data budgets |
| 37 | `37_rank_collapse.md` | Dong et al. 2021 | high | theory warning |
| 38 | `38_transformers_are_rnns.md` | Katharopoulos et al. 2020 | high | attention↔dynamics |
| 39 | `39_transformer_circuits.md` | Elhage et al. 2021 | high | no-black-box |
| 40 | `40_induction_heads.md` | Olsson et al. 2022 | high | in-context mechanics |
| 41 | `41_icl_gradient_descent.md` | von Oswald et al. 2023 | high | **AI-as-estimator** |
| 42 | `42_icl_function_classes.md` | Garg et al. 2022 | high | **AI-as-estimator** |
| 43 | `43_s4.md` | Gu, Goel & Ré 2022 | high | SSM alternative |
| 44 | `44_mamba.md` | Gu & Dao 2023 | high | SSM alternative |
| 45 | `45_hidden_attention_mamba.md` | Ali et al. 2024 | medium | SSM↔attention |
| 46 | `46_attention_ssm_rnn.md` | Sieber et al. 2024 | high | estimator selection |

## What Phase 2 actually adopted (summary of verdicts)

- **Step 5** uses the GAT masking principle (08), the Graphormer lesson that
  structure must be *injected, not hoped for* (09), and parameterizes
  $\hat B = \bar B \odot e^{\Delta}$ so sign and support are inherited from
  theory — the LoRA idea (33) applied to a graph: learn a *correction*, not
  the matrix.
- **Step 6** uses a small causal encoder (01) with missingness embeddings
  (BERT's mask token, 02), variables-kept-separate readouts (17), Gaussian
  heteroscedastic heads for calibration (13), and relative-time bias (30).
- **Rejected for now:** efficiency approximations (24–27; exact attention is
  cheap at our scale), mixture-of-experts (28; regimes handled by the
  dynamics, not routing), full spatiotemporal joint attention (18; violates
  rule W1 by learning structure freely).
- **Held in reserve:** S4/Mamba (43–44) as the forecaster if attention
  saturates; scaling laws (35–36) to size models once real EMA data arrive.

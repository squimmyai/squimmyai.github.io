---
title: "Building HumChess - A Transformer based Human-like Chess Opponent"
date: 2025-12-23
category: research
subtitle: ""
excerpt: "I suck at Chess and want experience building mini-LLMs. Let's kill two birds with one stone."
---

# HumChess

It's Christmas 2025 and I, for the first time in many a year, have nearly three weeks off. Three whole weeks! Just think of what I could do with that time! Finally, time to sit back, chill, and ignore the day job in applied AI. 

Anyway, I'm building HumChess. HumChess is a Transformer-based Chess Engine with the following goals:

1. Emulate Human skill effectively enough to be the backbone of a practically useful trainer
2. Be playable on my iPhone, offline, fully functional for my commute (ugh CoreML)
3. Teach me the practicalities of a training small-ish (<<<1b) Transformer model end-to-end 

The key insight here is that predicting Human chess moves is somewhat akin to how next-token-prediction is able to emulate human intelligence. Rather than predicting language though, we're going to predict the likely human move conditioned on the game state and ELO.

## Prior Work

I don't know where you are on the competition-is-good spectrum, but hopefully it's on the YES YOU WANT COMPETITION side.

Because this is _not_ the first such implementation of this idea. I know of at least the following:

* **Maia Chess**: [Basically the same overall idea](https://github.com/CSSLab/maia-chess), but split into multiple models each targetting a given Elo. Uses a slightly different architecture. 
* **Maia Chess 2**: [Recently released improvement on Maia Chess](https://github.com/CSSLab/maia2), single model across all Elo's. Still a different architecture.
* **Allie Chess**: [Another move prediction engine.](https://blog.ml.cmu.edu/2025/04/21/allie-a-human-aligned-chess-bot/). Single model, similar though not identical architecture.
* **Allie Chess 2**: [Version two of the same Chess Bot](https://github.com/y0mingzhang/allie-v2). This actually just re-uses the Qwen 3 architecture, so is effectively a modern LLM trained on Chess notation.

These are all great projects. Especially Maia 2 and Allie 2. 

Other than some light comparisons when discussing the model architecture of HumChess, I will proceed to mostly ignore their existance from this moment onwards. This is as much an educational project as it is a project with a practical aim. 

# Technical Details

## Data + "Tokenization"

All training data is sourced from the [Lichess Open Game database](https://database.lichess.org/). There's millions of games and roughly 90+ million more every month.

As a first pass we won't be attempting to ensure uniform training density across Elo & time controls, nor opening. A human move is a human move. I do suspect that after the first 100M or so games there's limited additional alpha to be had over the next 100M or so games, but I aim to test this.

We'll be encoding each [ply](https://en.wikipedia.org/wiki/Ply_(game_theory)) across each game in the following fixed-length sequence:

```
[CLS,
 SQ_0, SQ_1, ..., SQ_63,
 CASTLING,
 ELO_BUCKET,
 TL_BUCKET]
```

 * Square order: A1→H1, A2→H2, ..., A8→H8 (A1 = 0, H8 = 63)
 * Board vocabulary (13 tokens): EMPTY, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK
 * Castling rights: single token CR_0000..CR_1111 with bit order [WK, WQ, BK, BQ]
 * Elo bucket: <1000, then 100‑point bins up to 2500, then >=2500 (17 buckets)
 * Time‑left bucket: <10s, 10–30s, 30s–1m, then 1‑minute bins up to 14–15m, then >=15m, plus TL_UNKNOWN (19 buckets)

Positions are "white-normalized". Every move is from White's perspective in other words.

Note the critical implied decision here - we're training the model on the realised game state rather than the move history via Chess notation. This steers us away from a more language oriented auto-regressive decoder.

My intuition is that this _could_ save on network depth that would be initially spent translating a move order into a game state (i.e. translate Chess notation into a Chess board before computing move likelihood later on in the network). Rightly or wrongly this is the ultimate motivation behind this encoding and largely behind the architecture, though I do suspect that losing the move history could significantly impair prediction accuracy. It's a potentially _serious_ trade-off and would be the first potential improvement I'd consider.

The other major tradeoff is training density. A standard auto-regressive decoder would predict across each context sub-string and thus get a loss across every ply _in parallel_. Realising the game state into a grid sacrifices that optimization, though I'm ensure if the reduction in context to a fixed-length sequence will make up for that.

## Network Architecture

## 
# Validation Set — Documented Semantic Shifts in Sanskrit

Curated set of semantic changes **documented in prior scholarship** (primarily
Kamboja, *Semantic Change in Sanskrit*; page numbers refer to that book), restricted
to words that are **trackable in the w2v-sandhi embeddings** (present with usable
frequency in ≥3 of the 4 periods). This is the linchpin of the recovery study: for
each word we know the *expected* shift a priori, then ask whether the embeddings
recover it.

**Periodization:** Vedic (V) → Upaniṣadic (U) → Epic (E) → Sūtra/Śāstra (S).
**Freq** columns = token count in each era's w2v-sandhi model (from trackability scan).
**Type** taxonomy: pejoration, amelioration, narrowing/specialization,
widening/generalization, abstraction (concrete→abstract), metaphor, shift
(sense-displacement), divergence (polysemy split), **stable** (control).

> The **verdict** (recovered / partial / failed) is **not** produced by the harness.
> The harness assembles *evidence* (per-era neighbor trajectories + drift scores, in
> SLP1 and IAST); the verdict is a **subjective philological judgment** made by reading
> the neighbors against the documented shift and checking each neighbor's sense in a
> dictionary (WisdomLib / Monier-Williams) after SLP1→IAST conversion.

---

## Tier A — flagship shifts (clean recovery expected; rich neighbor support)

| # | Word (IAST) | SLP1 | Documented shift (from → to) | Type | Key transition | Kamboja pp. | Freq V/U/E/S |
|---|-------------|------|------------------------------|------|----------------|-------------|--------------|
| 1 | **asura** | `asura` | "lord, mighty one; life-giving god" (epithet even of Indra, Varuṇa, Agni, Savitṛ in early RV) → "demon, hostile being" | pejoration (religious; Avestan *ahura* parallel) | V→E | 55–56, 78 | 52/8/294/5 |
| 2 | **ātman** | `Atman` | "breath" (RV) → "life, vital essence; body" → "the Self, Absolute Soul" | abstraction / widening | V→U | 57–59 | 58/422/65/6 |
| 3 | **brahman** | `brahman` | "pious utterance, prayer, sacred formula" (RV) → "sacred knowledge / the Veda / priest" → "the Absolute, World-Soul" | abstraction / widening | V→U | 58–60 | 10/0/418/16 |
| 4 | **varuṇa** | `varuRa` | "supreme all-encompassing sovereign, moral governor of all" → "god of waters / the ocean (Indian Neptune)" | narrowing / demotion (eclipsed by Prajāpati) | V→E | 56–57, 78 | 133/19/32/41 |
| 5 | **go** | `go` | "cow" → metaphorical "earth; rays of light; the senses/eyes; stars; speech" | widening / metaphor | V→E | 72–74, 190–91, 198, 392 | 149/22/480/140 |
| 6 | **hari** | `hari` | "tawny / yellow-green / reddish-brown (color)" → soma, rays, fire; → "horse, lion, monkey"; → **name of Viṣṇu** | specialization (color → divine name) | V→E | 100, 219–229 | 40/0/425/7 |
| 7 | **yoga** | `yoga` | "act of yoking / harnessing" (√yuj) → "union; means, device" → "spiritual discipline, yoga; superhuman power"; also "acquisition; astron. conjunction" | abstraction → technical term | V→E/S | 309–311 | 8/13/318/87 |
| 8 | **guṇa** | `guRa` | "strand, cord (of rope); bowstring" → "quality, attribute" → "virtue, merit" → (Sāṅkhya) "the three constituents (sattva/rajas/tamas)" | abstraction / widening | U→E | 95, 164, 296–97 | 0/79/618/156 |

## Tier B — well-documented, trackable

| # | Word (IAST) | SLP1 | Documented shift (from → to) | Type | Key transition | Kamboja pp. | Freq V/U/E/S |
|---|-------------|------|------------------------------|------|----------------|-------------|--------------|
| 9 | **soma** | `soma` | "the soma plant / its pressed ritual juice" → referent extended to permitted substitute plants; identified with the moon | widening / referential | V→E | 71, 100 | 649/34/172/115 |
| 10 | **prajāpati** | `prajApati` | "lord of creatures" → "the creator, supreme god" (rises in the Brāhmaṇas, absorbing Varuṇa's sovereignty) | elevation / amelioration | V→U | 56, 124 | 15/42/40/8 |
| 11 | **kṣatra** | `kzatra` | "might, dominion, rule" → "the warrior/ruling class (kṣatriya), nobility" | shift (→ social class) | V→E | 60–61, 124 | 25/15/314/13 |
| 12 | **śūdra** | `SUdra` | "(a non-Aryan tribe / section of aboriginals)" → "the servile/labour class, fourth varṇa" | widening | V→E | 60 | 6/8/141/42 |
| 13 | **ari** | `ari` | "non-giver, miser" → "enemy" **and** "master, lord, pious man" | divergence (polysemy split) | V→E | 60–62, 149 | 14/0/267/38 |
| 14 | **uttara** | `uttara` | "upper, higher" (ud) → "later, subsequent; northern; superior" | widening (spatial → temporal/qualitative) | V→S | 272–276 | 28/54/67/155 |
| 15 | **uttama** | `uttama` | "uppermost, highest" (superl. of ud) → "best, most excellent; last" | abstraction (spatial → evaluative) | V→E | 269–271 | 6/9/371/21 |
| 16 | **pāda** | `pAda` | "foot" → "quarter (¼); a foot/line of verse; foot of a mountain; ray" | widening / metaphor | V→E | 255–259 | 10/24/195/185 |
| 17 | **tejas** | `tejas` | "sharpness, edge; fire, flame, brilliance" → "splendour, glory; vital energy, spiritual power, majesty" | abstraction | U→E | 183 | 0/29/199/11 |
| 18 | **setu** | `setu` | "that which binds, bond, fetter" (√si) → "causeway, dam, dyke, bridge"; fig. "boundary; protection" | concretization / shift | U→S | 239–243 | 0/11/15/31 |
| 19 | **bhṛtya** | `Bftya` | "one to be supported/maintained, a dependent" (√bhṛ) → "servant, slave" | shift / pejoration | U→E | 365–368 | 0/5/77/13 |
| 20 | **arka** | `arka` | "ray, flash; song/hymn of praise" → "the sun"; also "the arka plant" | shift | V→E | 386 | 9/10/205/10 |
| 21 | **aṃśu** | `aMśu` | "filament/stalk of the soma plant; soma juice" → "ray of light, sunbeam" | metaphor / shift (soma → ray) | V→E | 101, 223 | 19/0/50/5 |
| 22 | **preta** | `preta` | "departed, deceased one" → "ghost, spirit of the dead, hungry ghost" | specialization / pejoration | V→E | 81 | 7/6/53/32 |
| 23 | **vrata** | `vrata` | "divine ordinance, law, command of the gods; sacred rite" → "(self-imposed) vow, religious observance, fast" | shift | V→E | (general) | 27/9/249/59 |
| 24 | **rājan** | `rAjA` / `rAja` | sacral kingship (divine/ritual associations) → heroic/epic sovereign → administrative statecraft register | shift (register drift) | V→E/S | 208 *(verify)* | 251+24 / 74+29 / 2947+4394 / 201+198 |

## Controls (expected STABLE in Sanskrit — sanity checks)

| # | Word (IAST) | SLP1 | Note | Type | Kamboja pp. | Freq V/U/E/S |
|---|-------------|------|------|------|-------------|--------------|
| C1 | **deva** | `deva` | "celestial god, deity" — remains divine in Sanskrit; pejoration occurs only on the **Iranian** side (Av. *daēva* "devil"). Should show LOW drift / stable divine neighbors. | stable (control) | 55 | 740/183/2238/202 |
| C2 | **veda** | `veda` | "knowledge" → specialized to "the Veda (corpus)"; relatively stable referent. Mild drift expected. | near-stable | 160 | 488/527/949/135 |

---

### Notes / caveats to weigh in the subjective verdict

- **Accent collapses.** Vedic distinguished *bráhman* (n., "prayer/Absolute") from *brahmán* (m., "priest"); the corpus is unaccented, so the embedding sees one token. Same for *deva*. Read accordingly.
- **Early sense is sparse.** Pejorative/elevated shifts often hinge on *early* Vedic usage that is thin at our bin resolution (e.g. `asura` V=52, `brahman` V=10). A weak Vedic neighbor set is a *data* limit, not necessarily a method failure — note it.
- **Sense imbalance ≠ failure.** When a later sense dominates the corpus (e.g. `hari`=Viṣṇu in the Epics), the embedding will rightly center on it; the question is whether the *earlier* era still shows the *earlier* sense.
- **Direction matters.** For each word the "Key transition" column flags the era-pair where the documented change should be most visible — focus the neighbor comparison there.
- **Kamboja non-entries (excluded from this validation set, kept only as in-house case studies):** `dharma`, `karman`, `ṛta`, `yajña`, `agni`, `maṇḍala`, `nṛpa`, `indra` — these are NOT documented shifts in Kamboja, so using them as *recovery* targets would be circular. They appear in `results/case_studies.md` for illustration only.
- `rājan` (#24): the V→administrative drift is standard Indology and shows clearly in the embeddings, but confirm Kamboja p. 208 actually treats it before citing K. for it; otherwise cite Monier-Williams + the kingship literature.

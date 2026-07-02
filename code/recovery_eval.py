"""
recovery_eval.py — assemble RECOVERY EVIDENCE for the validation set.

For each documented shift (paper/validation_set.md) this emits, per era:
  - token frequency (n)
  - the top-K full-vocabulary nearest neighbors, in IAST (SLP1)
and the precomputed drift scores (second-order + Procrustes, per era-pair and
full span) from analysis/<model>/drift_scores.csv.

It does NOT decide recovered/partial/failed. The verdict is a *subjective*
philological judgment: read the neighbor trajectory against the documented shift,
check each neighbor's sense in a dictionary (WisdomLib / Monier-Williams), and
write the verdict in the blank field. The script only lays out the evidence.

Usage:
    python recovery_eval.py \
        --models_dir ../models/w2v-sandhi \
        --scores ../analysis/w2v-sandhi/drift_scores.csv \
        --out ../results/recovery_evidence.md
"""
import argparse
import csv
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from drift import load_wv, PERIODS  # PERIODS = vedic, upanisadic, epics, sutras

ERA_LABEL = {"vedic": "Vedic", "upanisadic": "Upaniṣadic", "epics": "Epic", "sutras": "Sūtra"}


def iast(slp1):
    return transliterate(slp1, sanscript.SLP1, sanscript.IAST)


# --- the validation set (documented shifts grounded in Kamboja; see paper/validation_set.md) ---
# forms: probe these surface forms per era, use the highest-count present one for neighbors.
VALIDATION = [
    # ---------- Tier A ----------
    dict(iast="asura", forms=["asura", "asurAH", "asurAn", "asurasya", "asurANAm"],
         shift="'lord, mighty / life-giving god' (epithet even of Indra, Varuṇa, Agni) → 'demon'",
         type="pejoration (religious)", transition="V→E", pp="55–56, 78", tier="A"),
    dict(iast="ātman", forms=["AtmA", "Atman", "AtmAnam", "AtmanaH", "Atmani", "Atmane"],
         shift="'breath' → 'life, vital essence; body' → 'the Self, Absolute Soul'",
         type="abstraction / widening", transition="V→U", pp="57–59", tier="A"),
    dict(iast="brahman", forms=["brahma", "brahman", "brahmaRaH", "brahmaRA", "brahmaRi"],
         shift="'prayer, sacred utterance' → 'sacred knowledge / Veda / priest' → 'the Absolute'",
         type="abstraction / widening", transition="V→U", pp="58–60", tier="A"),
    dict(iast="varuṇa", forms=["varuRa", "varuRaH", "varuRam", "varuRasya"],
         shift="'supreme all-encompassing sovereign, moral governor' → 'god of waters / ocean'",
         type="narrowing / demotion", transition="V→E", pp="56–57, 78", tier="A"),
    dict(iast="go", forms=["go", "gAm", "gAvaH", "gavi", "gavAm", "gObiH"],
         shift="'cow' → metaph. 'earth; rays of light; the senses/eyes; stars; speech'",
         type="widening / metaphor", transition="V→E", pp="72–74, 190–91, 198, 392", tier="A"),
    dict(iast="hari", forms=["hari", "hariH", "harim", "hareH", "harayaH"],
         shift="'tawny / yellow-green (color)' → soma, rays, fire; → 'horse, lion'; → name of Viṣṇu",
         type="specialization (color → divine name)", transition="V→E", pp="100, 219–229", tier="A"),
    dict(iast="yoga", forms=["yoga", "yogaH", "yogam", "yogasya", "yogena"],
         shift="'act of yoking/harnessing' → 'union; means' → 'spiritual discipline; superhuman power'",
         type="abstraction → technical term", transition="V→E/S", pp="309–311", tier="A"),
    dict(iast="guṇa", forms=["guRa", "guRaH", "guRam", "guRAH", "guREH", "guRAn"],
         shift="'strand, cord; bowstring' → 'quality, attribute' → 'virtue' → (Sāṅkhya) the three guṇas",
         type="abstraction / widening", transition="U→E", pp="95, 164, 296–97", tier="A"),
    # ---------- Tier B ----------
    dict(iast="soma", forms=["soma", "somaH", "somam", "somasya", "somena"],
         shift="'the soma plant / its ritual juice' → substitute plants; identified with the moon",
         type="widening / referential", transition="V→E", pp="71, 100", tier="B"),
    dict(iast="prajāpati", forms=["prajApati", "prajApatiH", "prajApatim", "prajApateH"],
         shift="'lord of creatures' → 'the creator, supreme god' (rises in the Brāhmaṇas)",
         type="elevation / amelioration", transition="V→U", pp="56, 124", tier="B"),
    dict(iast="kṣatra", forms=["kzatra", "kzatram", "kzatrasya", "kzatriya", "kzatriyaH"],
         shift="'might, dominion, rule' → 'the warrior/ruling class (kṣatriya)'",
         type="shift (→ social class)", transition="V→E", pp="60–61, 124", tier="B"),
    dict(iast="śūdra", forms=["SUdra", "SUdraH", "SUdram", "SUdrasya", "SUdrAH"],
         shift="'(a non-Aryan tribe / aboriginal section)' → 'the servile/labour class, 4th varṇa'",
         type="widening", transition="V→E", pp="60", tier="B"),
    dict(iast="ari", forms=["ari", "ariH", "arim", "areH", "arayaH", "arIn"],
         shift="'non-giver, miser' → 'enemy' AND 'master, lord, pious man'",
         type="divergence (polysemy split)", transition="V→E", pp="60–62, 149", tier="B"),
    dict(iast="uttara", forms=["uttara", "uttaram", "uttarA", "uttaraH"],
         shift="'upper, higher' → 'later, subsequent; northern; superior'",
         type="widening (spatial → temporal/qual.)", transition="V→S", pp="272–276", tier="B"),
    dict(iast="uttama", forms=["uttama", "uttamaH", "uttamam", "uttamA"],
         shift="'uppermost, highest' → 'best, most excellent; last'",
         type="abstraction (spatial → evaluative)", transition="V→E", pp="269–271", tier="B"),
    dict(iast="pāda", forms=["pAda", "pAdaH", "pAdam", "pAdEH", "pAdayoH"],
         shift="'foot' → 'quarter (¼); foot/line of verse; foot of mountain; ray'",
         type="widening / metaphor", transition="V→E", pp="255–259", tier="B"),
    dict(iast="tejas", forms=["tejas", "tejaH", "tejasA", "tejasaH"],
         shift="'sharpness, edge; fire, brilliance' → 'splendour; vital energy, spiritual power, majesty'",
         type="abstraction", transition="U→E", pp="183", tier="B"),
    dict(iast="setu", forms=["setu", "setuH", "setum", "setoH", "setavaH"],
         shift="'bond, fetter (that binds)' → 'causeway, dam, bridge'; fig. 'boundary; protection'",
         type="concretization / shift", transition="U→S", pp="239–243", tier="B"),
    dict(iast="bhṛtya", forms=["Bftya", "BftyaH", "Bftyam", "BftyAH", "BftyAnAm"],
         shift="'one to be supported, a dependent' → 'servant, slave'",
         type="shift / pejoration", transition="U→E", pp="365–368", tier="B"),
    dict(iast="arka", forms=["arka", "arkaH", "arkam", "arkasya"],
         shift="'ray, flash; hymn of praise' → 'the sun'; also 'the arka plant'",
         type="shift", transition="V→E", pp="386", tier="B"),
    dict(iast="aṃśu", forms=["aMSu", "aMSuH", "aMSum", "aMSavaH"],
         shift="'soma filament/stalk; soma juice' → 'ray of light, sunbeam'",
         type="metaphor / shift", transition="V→E", pp="101, 223", tier="B"),
    dict(iast="preta", forms=["preta", "pretaH", "pretam", "pretasya", "pretAH"],
         shift="'departed, deceased one' → 'ghost, spirit of the dead'",
         type="specialization / pejoration", transition="V→E", pp="81", tier="B"),
    dict(iast="vrata", forms=["vrata", "vratam", "vratasya", "vratAni", "vrate"],
         shift="'divine ordinance, command of the gods; sacred rite' → '(self-imposed) vow, observance, fast'",
         type="shift", transition="V→E", pp="(general)", tier="B"),
    dict(iast="rājan", forms=["rAjA", "rAja", "rAjan", "rAjAnam", "rAjYaH"],
         shift="sacral kingship → heroic/epic sovereign → administrative statecraft register",
         type="shift (register drift)", transition="V→E/S", pp="208 (verify)", tier="B"),
    # ---------- Controls ----------
    dict(iast="deva", forms=["deva", "devAH", "devAn", "devasya", "devAnAm", "devaH"],
         shift="'celestial god' — STABLE in Sanskrit (pejoration only on Iranian side, Av. daēva)",
         type="stable (control)", transition="—", pp="55", tier="C"),
    dict(iast="veda", forms=["veda", "vedaH", "vedam", "vedasya", "vedAH"],
         shift="'knowledge' → specialized 'the Veda (corpus)'; relatively stable",
         type="near-stable (control)", transition="—", pp="160", tier="C"),
]

TIER_TITLE = {"A": "Tier A — flagship shifts", "B": "Tier B — well-documented",
              "C": "Controls — expected stable"}

# --- DRAFT analytical verdicts (Claude's read of the neighbor trajectories vs the
#     documented shift). These are a STARTING POINT to confirm/overturn against
#     WisdomLib/Monier-Williams — NOT a script computation. Labels: recovered /
#     partial / failed / stable. Edit freely; they regenerate into the report. ---
VERDICTS = {
    # ---------- Tier A ----------
    "asura": ("recovered (V→E)",
        "Vedic company is divine/cosmic (mahat 'great', devānām 'of the gods', viṣṇoḥ, ṛtam, "
        "sāvitram); by the Epic every neighbor is a demon class — dānava, daitya, yakṣa, piśāca, "
        "kiṃnara, uraga — with sura/vibudha 'gods' appearing only as the contrast term. The "
        "documented pejoration 'mighty god → demon' is unambiguous in the neighbor shift. "
        "CAVEAT: the full-span scalar is LOW (proc 0.130 ≈ deva control) because Sūtra asura "
        "reverts to archaic ritual context (purohitam, bṛhaspatim, kratum, yajña) — read the "
        "V→E neighbors, not the end-to-end number. Upaniṣadic (n=8/40) thin/noisy."),
    "ātman": ("recovered (V→U)",
        "Vedic neighbors carry the bodily/breath sense — apānaḥ 'out-breath', śarīram 'body', "
        "annasya 'of food', vāyau 'in the air'; the Upaniṣadic set turns abstract/absolute — "
        "pūrṇaḥ 'full', paraḥ 'supreme', puruṣavidhaḥ 'person-formed', sākṣāt. The documented "
        "'breath → Self/Absolute' abstraction recovers exactly at the V→U transition. Epic = "
        "self/mind/disciplined-self (yogī, prajñaḥ, kṛtātmā). Sūtra probe falls to ritual-object "
        "context (oblique 'ātmani'), less informative."),
    "brahman": ("recovered (V→U)",
        "Accent-collapse caveat applies (bráhman vs brahmán merged), yet the trajectory is clean: "
        "Vedic = liturgy/utterance (sāma 'chant', yajuḥ 'Yajus formula', svareṇa 'with tone', "
        "upāsīta 'should worship'); Upaniṣadic = the Absolute (param 'supreme', anantam 'infinite', "
        "ānandam 'bliss', satyena 'truth', vijñānam). The documented 'prayer → Universal Absolute' "
        "recovers across V→U. Sūtra returns to ritual (prajāpatiḥ, yajamānaḥ, ṛṣayaḥ)."),
    "varuṇa": ("recovered (V→E)",
        "Vedic = supreme-Āditya company (mitraḥ, aryamā, bhagaḥ, aditiḥ, savitā, tvaṣṭā); by the "
        "Epic he sits among the lokapālas with explicit water terms — jaleśvaraḥ 'lord of waters', "
        "yādasām 'of sea-creatures', plus kuberaḥ, yamaḥ, vaiśravaṇaḥ. The documented demotion "
        "'supreme sovereign → god of the ocean' is recovered. Sūtra reverts to Vedic-style "
        "invocation (n=46)."),
    "go": ("partial (literal stable; metaphors NOT recovered)",
        "HONEST LIMIT: neighbors stay literal cattle/wealth throughout — Vedic dhenavaḥ 'milch-cows', "
        "vatsam 'calf', mātaraḥ; Epic vṛṣa 'bull', kṣīra 'milk', goṣṭha 'cowpen', ajāvika "
        "'goats-and-sheep'; Sūtra livestock/commodity (uṣṭra, mṛga, carma 'hide', suvarṇa). The "
        "documented metaphorical extensions (earth, rays, senses, stars) are diffuse usages, not a "
        "coherent neighbor cluster, so they do NOT surface distributionally — only faint hints in "
        "Vedic (matayaḥ/dhītayaḥ 'thoughts/hymns', the cow=hymn metaphor). Good failure-mode case."),
    "hari": ("recovered (V→E; via the monkey sense, not Viṣṇu)",
        "Vedic neighbors are soma-pressing verbs (pavate/punānaḥ/arṣati 'flows/purifies', induḥ "
        "'soma-drop', pavitre 'in the filter') + the bay steed (vājī, atyaḥ) — exactly the documented "
        "'tawny → soma, horse'. Epic collapses onto the Rāmāyaṇa monkey-host: vānara, kapi, plavaga, "
        "ṛkṣa, hanūmān, jāmbavān, yūthapa. The color→animal specialization recovers; the '→Viṣṇu' "
        "endpoint is documented but SUBDOMINANT here (monkeys dominate). Upaniṣadic n=5 noise."),
    "yoga": ("recovered (E + S, two senses)",
        "Vedic 'yoking' too sparse (n=8) to read. Epic recovers the spiritual-discipline technical "
        "cluster — sāṃkhya, dhyāna 'meditation', samādhi, saṃnyāsa, adhyātma, jñāna; Sūtra recovers "
        "the *other* documented later sense, Arthaśāstra 'acquisition/securing of property': vetana "
        "'wages', śulka 'toll', paṇya 'goods', argha 'price', dravya 'property'. Both documented "
        "later senses recovered, each in the corpus where it lives. Strong."),
    "guṇa": ("recovered (abstract senses; origin not trackable)",
        "Correctly ABSENT in Vedic (post-Vedic word). Upaniṣadic = quality/attribute (guṇavat, "
        "viśiṣṭasya, jñānāt); Epic = virtue + Sāṅkhya (svabhāva, prakṛti, nirguṇa, ṣāḍguṇya, śīla, "
        "mādhurya); Sūtra = the Vaiśeṣika category, paired with dravya 'substance' (rūpa, varṇa, "
        "lakṣaṇa, doṣa, hetu). The 'quality → virtue → philosophical-category' arc recovers; the "
        "original 'cord/strand' sense isn't trackable (word absent where it would appear)."),
    # ---------- Tier B ----------
    "soma": ("recovered (V→E, plant→moon)",
        "Vedic = the Pavamāna ritual drink being pressed/purified (pavasva, pavamāna, pūyamānaḥ, "
        "indo, kratu); Epic groups soma with the luminaries — indu 'moon', arka, sūrya, candra-context "
        "(viṣuve), viṣṇu, rudra — recovering the documented plant→moon identification. The "
        "'substitute-plants' sense is harder to see. Sūtra reverts to soma-ritual (vaiśvadeve, juṣasva)."),
    "prajāpati": ("recovered (intensification; Vedic baseline already elevated)",
        "Creator role is present already in Vedic (asṛjata 'emitted/created', prajāḥ 'creatures', "
        "śraiṣṭhyāya 'for supremacy'), so the documented 'rise' is an INTENSIFICATION rather than an "
        "origination: by the Epic he is explicitly the supreme self-existent creator — svayaṃbhūḥ, "
        "lokapitāmahaḥ 'world-grandfather', parameṣṭhī, devadevaḥ. Recovered, but note the gradient "
        "(not a sharp V→U jump); Upaniṣadic neighbors are mixed/noisy."),
    "kṣatra": ("recovered (V→E)",
        "Vedic = abstract might/dominion (balam, vīryam 'valor', ojas 'strength', rāṣṭram 'realm', "
        "indriyam 'power'); Epic = the warrior class and its duty (kṣātra 'martial', sāṃgrāmikaḥ, "
        "jīvikā 'livelihood', dharmeṇa/dharme — kṣatra-dharma, anuvrata). The 'might → warrior class' "
        "shift recovers cleanly. Sūtra reverts to ritual benediction (savitar, bṛhaspatiḥ)."),
    "śūdra": ("partial (destination clear; origin too sparse)",
        "Vedic n=6 is too sparse to confirm the documented tribal origin. But the destination "
        "recovers in the Epic — the four-varṇa system and its occupations: vaiśya, caṇḍāla, viś, plus "
        "kṛṣi 'agriculture', vāṇijya 'trade', gorakṣa 'cattle-keeping'; Sūtra similar (vaiśya, "
        "rakṣet). The widening to 'servile/labour class' is confirmed at its endpoint, not its start."),
    "ari": ("recovered (enemy branch only; 'master' branch NOT recovered)",
        "Epic and Sūtra are unambiguously 'enemy' — amitra, ripu, śatru, plus the 'foe-crusher' "
        "compound second-members ari-mardana/-sūdana/-niṣūdana/-karśana — and in Sūtra the "
        "Arthaśāstra ally-enemy maṇḍala (śatru, saṃdhi 'treaty', mitreṇa). The documented OTHER branch "
        "('master, lord, pious man') does NOT surface — honest partial recovery of a polysemy split. "
        "Absent in Upaniṣadic; Vedic n=14 is mixed/ambiguous."),
    "uttara": ("recovered (multi-sense widening)",
        "Vedic = spatial/ordinal 'next, upper' (pūrvam pairing, ordinals ṣaṣṭha/caturtha/dvitīya); "
        "Upaniṣadic = the directional 'northern' sense via the dakṣiṇa 'south' pair; Epic adds "
        "'reply/subsequent' (prativaktum 'to answer', adhara 'lower' pairing, paścima 'western'). The "
        "documented 'upper → later/northern/superior' widening tracks across eras. Sūtra = geometric/"
        "ritual directions."),
    "uttama": ("recovered (V→E, spatial→evaluative)",
        "Vedic = positional 'topmost in a series' (madhyamam 'middle', ordinals saptama, metrical "
        "positions); Epic = the evaluative 'best/supreme' (anuttamam 'unsurpassed', agryam 'foremost', "
        "mukhyam 'chief', paramam, aprameyam). The documented spatial→evaluative abstraction recovers. "
        "Sūtra reverts to metrical/positional (prathama, gāyatrī, pāda)."),
    "pāda": ("recovered (V→U, foot→quarter)",
        "Vedic = literal foot (dvipādaḥ 'two-footed', body/leg context); Upaniṣadic recovers the "
        "'quarter (¼)' sense — catuṣpād 'four-quartered', caturthaḥ 'fourth', the cosmic pādas of "
        "Brahman (sūrya/candra/āditya context, cf. Māṇḍūkya's four pādas); Sūtra = measure/fraction "
        "(numerals, aṅgula). Epic returns to the body-part list (caraṇa, pāṇi, jaṅghā). Foot→quarter "
        "clearly recovered."),
    "tejas": ("recovered (abstraction to splendour/energy)",
        "Vedic = fire/brilliance + incipient power (dīpyate 'shines', balam, indriyam, brahmavarcasa "
        "'spiritual lustre'); Epic = majesty/glory/energy (yaśasā 'glory', śriyā 'splendour', vīryeṇa "
        "'valor', bhāsā 'radiance', raśmivān 'rayed'); Upaniṣadic shows the element + spiritual sense "
        "(adhyātmam, apaḥ). The documented 'fire/edge → vital energy, majesty' abstraction recovers."),
    "setu": ("recovered (U→S, bond→bridge)",
        "Absent Vedic. Upaniṣadic = the figurative cosmic bond/world-boundary and protector "
        "(bhuvanasya 'of the world', pālayitā 'protector', saṃbhedāya 'for separation', adhipaḥ "
        "'overlord' — the ātman/brahman-as-dyke image); Epic = the literal causeway/bridge (tīra "
        "'shore', anūpa 'watery land', the crossing to Laṅkā); Sūtra = embankment/dam in irrigation/"
        "toll context (bandha, śulka, vaṇij). The 'bond → causeway/dam' concretization recovers."),
    "bhṛtya": ("recovered (E; dependent→retainer/servant)",
        "Absent Vedic (post-Vedic). Upaniṣadic n=5 noisy (faint maintenance/origination sense). Epic "
        "groups bhṛtya with the household's dependents and retainers — amātya 'minister', bāndhava/"
        "bandhu 'kin', atithi 'guest', svānām 'one's own people', saṃbandhi; Sūtra = servant in legal/"
        "household affairs (sahāya 'helper', dāra 'wife', vyavahāra). 'Supported dependent → servant' "
        "recovers at the Epic."),
    "arka": ("recovered (V→E, hymn→sun)",
        "Vedic carries the √arc 'praise' sense — arcanti 'they sing', stomāsaḥ 'hymns', ukthebhiḥ "
        "'recitations', gṛṇānāḥ 'praising', dhītibhiḥ 'with hymns'; Epic is unambiguously the SUN — "
        "sūrya, ravi, bhāskara, divākara 'day-maker', raśmi 'ray', aṃśu. The documented 'song of "
        "praise/ray → the sun' shift recovers cleanly. Sūtra n=10 noisy."),
    "aṃśu": ("recovered (V→E, soma-filament→ray)",
        "Vedic = the bright soma-stalk/plant (śobhate/dyutānaḥ 'shines', vīrudhām 'of plants', "
        "svādiṣṭhayā 'sweetest', pūtaḥ 'purified'); Epic = ray of light (raśmi, kiraṇa 'ray', kānti "
        "'radiance', sūrya, prabhā), with the filament sense lingering in mṛṇāla 'lotus-fibre'. The "
        "documented soma→ray metaphor recovers. Absent Upaniṣadic; Sūtra n=5 reverts to soma-ritual."),
    "preta": ("recovered (pejoration)",
        "Vedic/Upaniṣadic = the deceased and the afterlife journey (punarmṛtyum 're-death', "
        "candramasam 'the moon' as destination of the dead, kimīdinaḥ 'sorcerers'); Epic groups preta "
        "with low/cursed states — kāladharma 'death', dasyu 'robber', mleccha, tiryagyoni "
        "'animal-rebirth', kāpatha 'evil path'; Sūtra = inauspicious (bhaya 'fear', kleśa 'affliction', "
        "vyādhita 'diseased'). The 'departed → ill-omened ghost' pejoration recovers."),
    "vrata": ("recovered (V→E, ordinance→vow)",
        "Vedic = cosmic ordinance / fixed rule (pratiṣṭhita 'established', saṃvatsarāt 'from the year', "
        "vairāja/pāṅkta metrical structures); Epic = the self-imposed vow/austerity — upavāsa "
        "'fasting', kaumāra 'chastity-vow', tāpasa 'ascetic', duścara 'hard-to-perform', cīrṇa "
        "'observed', tyāga 'renunciation'. The documented 'divine ordinance → personal vow/observance' "
        "shift recovers. Sūtra = named soma-rites (viśvajit, atirātra)."),
    "rājan": ("recovered (showcase; 3-stage register drift)",
        "The cleanest trajectory: Vedic king sits among DEITIES — soma, agni, bṛhaspati, vaiśvānara, "
        "pāvaka (sacral kingship; 'Soma the king'); Epic = named epic sovereigns + narrative address "
        "(proper names dāśārha/vāhlīka/ṛṣyaśṛṅga, tāta 'dear', janeśvara 'lord of people'); Sūtra = "
        "Arthaśāstra statecraft/espionage register — śatru 'enemy', preṣayet 'should dispatch', "
        "atisaṃdhatte 'out-maneuvers', pārṣṇi 'flank', rājya 'realm'. Sacral→heroic→administrative "
        "fully recovered. (Confirm Kamboja p.208 actually treats rājan; else cite MW + kingship lit.)"),
    # ---------- Controls ----------
    "deva": ("STABLE — control passes",
        "Lowest full-span drift (proc 0.126). Stays 'god / celestial being' in every era — Vedic "
        "divine collective (pitaraḥ, viśve, aṅgirasaḥ, the deva/asura contest), Epic broadens to "
        "'celestial beings' generally (gandharva, apsaras, yakṣa, kiṃnara, daitya, dānava) but remains "
        "supernatural/divine, Sūtra Vedic-style invocation. NO pejoration — confirming the documented "
        "asymmetry that only Iranian daēva degrades. Good null result."),
    "veda": ("near-stable → mild specialization (control)",
        "Behaves as a soft control: Vedic = knowledge/recitation (saṃhitām 'collection', upāste "
        "'recites', vidvān 'learned'); by the Epic it specializes to the textual canon and its "
        "curriculum — vedāṅga, vedānta, ṣaḍaṅga, itihāsa, purāṇa, chandas, adhyayana. The documented "
        "'knowledge → the Veda (corpus)' narrowing is visible but mild; low drift overall."),
}


def best_form(wv, forms):
    """Highest-count present form, with its count."""
    best, bestc = None, -1
    for f in forms:
        if f in wv.key_to_index:
            c = wv.get_vecattr(f, "count")
            if c > bestc:
                best, bestc = f, c
    return best, (bestc if bestc >= 0 else 0)


def neighbors(wv, form, k):
    if form is None or form not in wv.key_to_index:
        return []
    return [(t, s) for t, s in wv.most_similar(form, topn=k)]


def load_scores(path):
    rows = {}
    if Path(path).exists():
        for r in csv.DictReader(open(path)):
            rows[r["word"]] = r
    return rows


def score_line(entry, scores):
    """Return a one-line drift summary pulled from drift_scores.csv, or '—'."""
    # use whichever probe form is present in the scores table
    row = None
    for f in entry["forms"]:
        if f in scores:
            row = scores[f]
            key = f
            break
    if row is None:
        return "_drift scores: — (word not in shared 4-era vocab; rely on neighbor trajectory)_"

    def g(k):
        try:
            return f"{float(row[k]):.3f}"
        except (KeyError, ValueError):
            return "—"
    return (f"_drift ({key}):_ "
            f"**second-order** V→U {g('so_ved_upa')} · U→E {g('so_upa_epi')} · "
            f"E→S {g('so_epi_sut')} · **full V→S {g('so_ved_sut')}**  ||  "
            f"**Procrustes** V→U {g('proc_ved_upa')} · U→E {g('proc_upa_epi')} · "
            f"E→S {g('proc_epi_sut')} · full {g('proc_ved_sut')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models_dir", required=True)
    ap.add_argument("--scores", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--topk", type=int, default=15)
    args = ap.parse_args()

    wvs = {e: load_wv(args.models_dir, e) for e in PERIODS}
    scores = load_scores(args.scores)

    out = []
    out.append("# Recovery Evidence — w2v-sandhi\n")
    out.append("Per documented shift: full-vocabulary nearest neighbors by era (IAST, SLP1 in "
               "parentheses) + precomputed drift scores. **The verdict is yours to fill in** — "
               "read each trajectory against the documented shift, verify neighbor senses in "
               "WisdomLib/Monier-Williams, then write recovered / partial / failed with a reason.\n")
    out.append(f"Model: `{args.models_dir}` · neighbors: top-{args.topk} (full vocab) · "
               f"periods: Vedic → Upaniṣadic → Epic → Sūtra.\n")

    # headline tally from the DRAFT verdicts (documented shifts only, excluding the 2 controls)
    docs = [e for e in VALIDATION if e["tier"] != "C"]
    def bucket(iast):
        lab = VERDICTS.get(iast, ("", ""))[0].lower()
        if lab.startswith("recovered"):
            return "recovered"
        if lab.startswith("partial"):
            return "partial"
        if lab.startswith("failed"):
            return "failed"
        return "unjudged"
    n_rec = sum(bucket(e["iast"]) == "recovered" for e in docs)
    n_par = sum(bucket(e["iast"]) == "partial" for e in docs)
    n_fai = sum(bucket(e["iast"]) == "failed" for e in docs)
    out.append(f"**DRAFT tally (Claude's read, to confirm):** of {len(docs)} documented shifts — "
               f"**{n_rec} recovered, {n_par} partial, {n_fai} failed**; "
               f"+2 controls (deva stable, veda near-stable). "
               f"Headline candidate: *“embeddings recover {n_rec} of {len(docs)} documented shifts.”* "
               f"Treat partials/limits (go-metaphor, ari-‘master’ branch, śūdra-origin) as honest "
               f"method-boundary cases, not failures to hide.\n")
    out.append("---\n")

    current_tier = None
    for e in VALIDATION:
        if e["tier"] != current_tier:
            current_tier = e["tier"]
            out.append(f"\n# {TIER_TITLE[current_tier]}\n")

        out.append(f"## {e['iast']}  (Kamboja pp. {e['pp']})")
        out.append(f"- **Documented shift:** {e['shift']}")
        out.append(f"- **Type:** {e['type']}  ·  **expected transition:** {e['transition']}")
        out.append(f"- {score_line(e, scores)}\n")
        out.append("| Era | n | Top neighbors — IAST (SLP1) |")
        out.append("|-----|---|------------------------------|")
        for era in PERIODS:
            wv = wvs[era]
            form, n = best_form(wv, e["forms"])
            nbrs = neighbors(wv, form, args.topk)
            if not nbrs:
                cell = "_absent / not in vocab_"
            else:
                cell = ", ".join(f"{iast(t)} ({t})" for t, _ in nbrs)
            probe = f" _[{iast(form)}]_" if form else ""
            out.append(f"| {ERA_LABEL[era]}{probe} | {n} | {cell} |")
        out.append("")
        v = VERDICTS.get(e["iast"])
        if v:
            out.append(f"**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** {v[0]}  ")
            out.append(f"**Notes:** {v[1]}\n")
        else:
            out.append("**Verdict (subjective):** ______  ·  **Notes:** ______\n")
        out.append("---\n")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {args.out}  ({len(VALIDATION)} validation words)")


if __name__ == "__main__":
    main()

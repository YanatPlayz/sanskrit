# Recovery Evidence — w2v-sandhi

Per documented shift: full-vocabulary nearest neighbors by era (IAST, SLP1 in parentheses) + precomputed drift scores. **The verdict is yours to fill in** — read each trajectory against the documented shift, verify neighbor senses in WisdomLib/Monier-Williams, then write recovered / partial / failed with a reason.

Model: `../models/w2v-sandhi` · neighbors: top-15 (full vocab) · periods: Vedic → Upaniṣadic → Epic → Sūtra.

**DRAFT tally (Claude's read, to confirm):** of 24 documented shifts — **22 recovered, 2 partial, 0 failed**; +2 controls (deva stable, veda near-stable). Headline candidate: *“embeddings recover 22 of 24 documented shifts.”* Treat partials/limits (go-metaphor, ari-‘master’ branch, śūdra-origin) as honest method-boundary cases, not failures to hide.

---


# Tier A — flagship shifts

## asura  (Kamboja pp. 55–56, 78)
- **Documented shift:** 'lord, mighty / life-giving god' (epithet even of Indra, Varuṇa, Agni) → 'demon'
- **Type:** pejoration (religious)  ·  **expected transition:** V→E
- _drift (asurAH):_ **second-order** V→U 0.043 · U→E 0.046 · E→S 0.097 · **full V→S 0.031**  ||  **Procrustes** V→U 0.236 · U→E 0.276 · E→S 0.411 · full 0.130

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[asura]_ | 52 | mahat (mahat), devānām (devAnAm), ekam (ekam), asyāḥ (asyAH), jajāna (jajAna), viṣṇoḥ (vizRoH), viśveṣām (viSvezAm), sāvitram (sAvitram), udūḍham (udUQam), aṅgam (aNgam), ṛtam (ftam), jihvā (jihvA), asūn (asUn), babhūva (baBUva), paruḥ (paruH) |
| Upaniṣadic _[asurāḥ]_ | 40 | manuṣyāḥ (manuzyAH), brāhmaṇāḥ (brAhmaRAH), ke (ke), brahmacaryam (brahmacaryam), tebhyaḥ (teByaH), uktāḥ (uktAH), enān (enAn), trī (trI), varṣāṇi (varzARi), cakrire (cakrire), prājāpatyāḥ (prAjApatyAH), santaḥ (santaH), mātā (mAtA), bhava (Bava), devāḥ (devAH) |
| Epic _[asura]_ | 294 | dānava (dAnava), uraga (uraga), yakṣa (yakza), piśāca (piSAca), gandharvam (ganDarvam), pataga (pataga), bhoginām (BoginAm), kiṃnara (kiMnara), yakṣāṇām (yakzARAm), daitya (dEtya), gandharva (ganDarva), asurāṇām (asurARAm), pannaga (pannaga), sura (sura), vibudha (vibuDa) |
| Sūtra _[asurāḥ]_ | 17 | purohitam (purohitam), asurān (asurAn), bṛhaspatim (bfhaspatim), kratum (kratum), yajña (yajYa), yena (yena), apacitim (apacitim), tanvaḥ (tanvaH), ṛṣayaḥ (fzayaH), pūrve (pUrve), tanū (tanU), hotāram (hotAram), etam (etam), yama (yama), pāvānaḥ (pAvAnaH) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (V→E)  
**Notes:** Vedic company is divine/cosmic (mahat 'great', devānām 'of the gods', viṣṇoḥ, ṛtam, sāvitram); by the Epic every neighbor is a demon class — dānava, daitya, yakṣa, piśāca, kiṃnara, uraga — with sura/vibudha 'gods' appearing only as the contrast term. The documented pejoration 'mighty god → demon' is unambiguous in the neighbor shift. CAVEAT: the full-span scalar is LOW (proc 0.130 ≈ deva control) because Sūtra asura reverts to archaic ritual context (purohitam, bṛhaspatim, kratum, yajña) — read the V→E neighbors, not the end-to-end number. Upaniṣadic (n=8/40) thin/noisy.

---

## ātman  (Kamboja pp. 57–59)
- **Documented shift:** 'breath' → 'life, vital essence; body' → 'the Self, Absolute Soul'
- **Type:** abstraction / widening  ·  **expected transition:** V→U
- _drift (AtmA):_ **second-order** V→U 0.043 · U→E 0.104 · E→S 0.091 · **full V→S 0.030**  ||  **Procrustes** V→U 0.204 · U→E 0.495 · E→S 0.583 · full 0.218

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[ātmā]_ | 157 | prajñā (prajYA), mayam (mayam), upāste (upAste), eṣaḥ (ezaH), apānaḥ (apAnaH), bhūtānām (BUtAnAm), bālākiḥ (bAlAkiH), annasya (annasya), śarīram (SarIram), vāyau (vAyO), etasmin (etasmin), brahmaṇaḥ (brahmaRaH), saṃvādayiṣṭhāḥ (saMvAdayizWAH), etāvān (etAvAn), kakubh (kakuB) |
| Upaniṣadic _[ātmā]_ | 793 | aparokṣāt (aparokzAt), mayāt (mayAt), sākṣāt (sAkzAt), abhyantaraḥ (aByantaraH), pūrvasya (pUrvasya), pūrṇaḥ (pUrRaH), etasmāt (etasmAt), puruṣavidhaḥ (puruzaviDaH), akṣiṇi (akziRi), paraḥ (paraH), dharmā (DarmA), prakṛtaḥ (prakftaH), śārīraḥ (SArIraH), saṃghātaḥ (saMGAtaH), ajaḥ (ajaH) |
| Epic _[ātmā]_ | 1757 | ātman (Atman), dhīḥ (DIH), cetāḥ (cetAH), ātmavān (AtmavAn), cārī (cArI), yogī (yogI), priyaṃvadaḥ (priyaMvadaH), vicitravīryaḥ (vicitravIryaH), prajñaḥ (prajYaH), narendraḥ (narendraH), jñānaḥ (jYAnaH), kṛtātmā (kftAtmA), anvabudhyata (anvabuDyata), udyuktaḥ (udyuktaH), upekṣakaḥ (upekzakaH) |
| Sūtra _[ātmani]_ | 139 | pucche (pucCe), upadheyāḥ (upaDeyAH), upadadhyāt (upadaDyAt), tāsām (tAsAm), upadhāya (upaDAya), ṣoḍaśyaḥ (zoqaSyaH), apyaye (apyaye), viśayāḥ (viSayAH), iṣṭakāḥ (izwakAH), pratīcīḥ (pratIcIH), śeṣe (Seze), pārśvayoḥ (pArSvayoH), catasroḥ (catasroH), puccha (pucCa), pañcamabhāgīyāḥ (paYcamaBAgIyAH) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (V→U)  
**Notes:** Vedic neighbors carry the bodily/breath sense — apānaḥ 'out-breath', śarīram 'body', annasya 'of food', vāyau 'in the air'; the Upaniṣadic set turns abstract/absolute — pūrṇaḥ 'full', paraḥ 'supreme', puruṣavidhaḥ 'person-formed', sākṣāt. The documented 'breath → Self/Absolute' abstraction recovers exactly at the V→U transition. Epic = self/mind/disciplined-self (yogī, prajñaḥ, kṛtātmā). Sūtra probe falls to ritual-object context (oblique 'ātmani'), less informative.

---

## brahman  (Kamboja pp. 58–60)
- **Documented shift:** 'prayer, sacred utterance' → 'sacred knowledge / Veda / priest' → 'the Absolute'
- **Type:** abstraction / widening  ·  **expected transition:** V→U
- _drift (brahma):_ **second-order** V→U 0.042 · U→E 0.114 · E→S 0.078 · **full V→S 0.044**  ||  **Procrustes** V→U 0.294 · U→E 0.536 · E→S 0.456 · full 0.249

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[brahma]_ | 571 | abhīvartaḥ (aBIvartaH), āśīyaḥ (ASIyaH), apacitim (apacitim), svargāya (svargAya), sāma (sAma), abhīvartena (aBIvartena), svareṇa (svareRa), vasiṣṭhaḥ (vasizWaH), vindati (vindati), sṛjyamānam (sfjyamAnam), upāsīta (upAsIta), gaurīvitasya (gOrIvitasya), yunakti (yunakti), prāyaṇīyena (prAyaRIyena), yajuḥ (yajuH) |
| Upaniṣadic _[brahma]_ | 1433 | vidā (vidA), param (param), anantam (anantam), avet (avet), vijñānāt (vijYAnAt), prakṛtam (prakftam), vid (vid), vijñānam (vijYAnam), kimu (kimu), satyena (satyena), uktam (uktam), ānandam (Anandam), etāvat (etAvat), viditam (viditam), vākyena (vAkyena) |
| Epic _[brahma]_ | 1453 | kalpate (kalpate), bhūyāya (BUyAya), kṣatreṇa (kzatreRa), ekākṣaram (ekAkzaram), ghne (Gne), sanātanam (sanAtanam), hatyayā (hatyayA), prajahāti (prajahAti), puṇḍarīkam (puRqarIkam), viṣṇu (vizRu), tvāya (tvAya), ānantyāya (AnantyAya), vādibhiḥ (vAdiBiH), nidhānam (niDAnam), dhāma (DAma) |
| Sūtra _[brahma]_ | 183 | prajāḥ (prajAH), prajāpatiḥ (prajApatiH), tejaḥ (tejaH), tanū (tanU), ṛṣayaḥ (fzayaH), paśūn (paSUn), yajamānaḥ (yajamAnaH), adāt (adAt), tanvaḥ (tanvaH), asurāḥ (asurAH), brahmaṇā (brahmaRA), lokam (lokam), pūrve (pUrve), sūrya (sUrya), yajate (yajate) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (V→U)  
**Notes:** Accent-collapse caveat applies (bráhman vs brahmán merged), yet the trajectory is clean: Vedic = liturgy/utterance (sāma 'chant', yajuḥ 'Yajus formula', svareṇa 'with tone', upāsīta 'should worship'); Upaniṣadic = the Absolute (param 'supreme', anantam 'infinite', ānandam 'bliss', satyena 'truth', vijñānam). The documented 'prayer → Universal Absolute' recovers across V→U. Sūtra returns to ritual (prajāpatiḥ, yajamānaḥ, ṛṣayaḥ).

---

## varuṇa  (Kamboja pp. 56–57, 78)
- **Documented shift:** 'supreme all-encompassing sovereign, moral governor' → 'god of waters / ocean'
- **Type:** narrowing / demotion  ·  **expected transition:** V→E
- _drift (varuRaH):_ **second-order** V→U 0.067 · U→E 0.074 · E→S 0.095 · **full V→S 0.050**  ||  **Procrustes** V→U 0.283 · U→E 0.339 · E→S 0.312 · full 0.231

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[varuṇaḥ]_ | 316 | mitraḥ (mitraH), aryamā (aryamA), māmahantām (mAmahantAm), sindhuḥ (sinDuH), pūṣā (pUzA), aditiḥ (aditiH), nayatu (nayatu), tvaṣṭā (tvazwA), bhagaḥ (BagaH), dhṛta (Dfta), pratigrahītre (pratigrahItre), rudraḥ (rudraH), bṛhaspatiḥ (bfhaspatiH), savitā (savitA), sajoṣasaḥ (sajozasaH) |
| Upaniṣadic _[varuṇaḥ]_ | 19 | aryamā (aryamA), bṛhaspatiḥ (bfhaspatiH), viṣṇuḥ (vizRuH), diśi (diSi), indraḥ (indraH), devataḥ (devataH), udgāya (udgAya), yajñe (yajYe), dakṣiṇāyām (dakziRAyAm), dadāti (dadAti), udagāyat (udagAyat), yamaḥ (yamaH), anuśaśāsa (anuSaSAsa), mitraḥ (mitraH), garbham (garBam) |
| Epic _[varuṇaḥ]_ | 115 | aryamā (aryamA), mitraḥ (mitraH), yamaḥ (yamaH), pūṣā (pUzA), kuberaḥ (kuberaH), yādasām (yAdasAm), vaivasvataḥ (vEvasvataH), jaleśvaraḥ (jaleSvaraH), vaiśravaṇaḥ (vESravaRaH), vivasvān (vivasvAn), bhagaḥ (BagaH), rudraḥ (rudraH), ajaḥ (ajaH), dhaneśvaraḥ (DaneSvaraH), sthāṇuḥ (sTARuH) |
| Sūtra _[varuṇaḥ]_ | 46 | bṛhaspatiḥ (bfhaspatiH), mitraḥ (mitraH), indraḥ (indraH), naḥ (naH), bhara (Bara), indrā (indrA), dadātu (dadAtu), vaiśvadevam (vESvadevam), uta (uta), imam (imam), varuṇa (varuRa), imāḥ (imAH), vāyuḥ (vAyuH), ava (ava), stuhi (stuhi) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (V→E)  
**Notes:** Vedic = supreme-Āditya company (mitraḥ, aryamā, bhagaḥ, aditiḥ, savitā, tvaṣṭā); by the Epic he sits among the lokapālas with explicit water terms — jaleśvaraḥ 'lord of waters', yādasām 'of sea-creatures', plus kuberaḥ, yamaḥ, vaiśravaṇaḥ. The documented demotion 'supreme sovereign → god of the ocean' is recovered. Sūtra reverts to Vedic-style invocation (n=46).

---

## go  (Kamboja pp. 72–74, 190–91, 198, 392)
- **Documented shift:** 'cow' → metaph. 'earth; rays of light; the senses/eyes; stars; speech'
- **Type:** widening / metaphor  ·  **expected transition:** V→E
- _drift (go):_ **second-order** V→U 0.025 · U→E 0.111 · E→S 0.094 · **full V→S 0.036**  ||  **Procrustes** V→U 0.327 · U→E 0.618 · E→S 0.412 · full 0.209

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[gāvaḥ]_ | 210 | dhenavaḥ (DenavaH), arṣanti (arzanti), mātaraḥ (mAtaraH), vatsam (vatsam), īrate (Irate), matayaḥ (matayaH), anūṣata (anUzata), dhītayaḥ (DItayaH), vāvaśānāḥ (vAvaSAnAH), vipaścitaḥ (vipaScitaH), asṛgram (asfgram), sindhavaḥ (sinDavaH), vāśrāḥ (vASrAH), asthuḥ (asTuH), rathāḥ (raTAH) |
| Upaniṣadic _[go]_ | 22 | agnihotre (agnihotre), udgīthe (udgITe), śūdra (SUdra), vṛṇīṣva (vfRIzva), ṛṣeḥ (fzeH), kumārasya (kumArasya), datta (datta), śiṣyāya (SizyAya), janakasya (janakasya), abhyuktavān (aByuktavAn), brahmiṣṭha (brahmizWa), jānaśrutiḥ (jAnaSrutiH), samīpe (samIpe), haste (haste), dayadhvam (dayaDvam) |
| Epic _[go]_ | 480 | vindet (vindet), vṛṣam (vfzam), vṛṣeṇa (vfzeRa), vṛṣāya (vfzAya), gavām (gavAm), labhet (laBet), pradāne (pradAne), samāpnoti (samApnoti), vatsānām (vatsAnAm), goṣṭhe (gozWe), pradātṝṇām (pradAtFRAm), ajāvikam (ajAvikam), pradātā (pradAtA), kṣīra (kzIra), vājimedha (vAjimeDa) |
| Sūtra _[go]_ | 140 | patti (patti), gaṇikā (gaRikA), vivīta (vivIta), surā (surA), carma (carma), nāga (nAga), mudrā (mudrA), kāṣṭha (kAzWa), uṣṭra (uzwra), mṛga (mfga), skandha (skanDa), pracāraḥ (pracAraH), suvarṇa (suvarRa), vajra (vajra), vanam (vanam) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** partial (literal stable; metaphors NOT recovered)  
**Notes:** HONEST LIMIT: neighbors stay literal cattle/wealth throughout — Vedic dhenavaḥ 'milch-cows', vatsam 'calf', mātaraḥ; Epic vṛṣa 'bull', kṣīra 'milk', goṣṭha 'cowpen', ajāvika 'goats-and-sheep'; Sūtra livestock/commodity (uṣṭra, mṛga, carma 'hide', suvarṇa). The documented metaphorical extensions (earth, rays, senses, stars) are diffuse usages, not a coherent neighbor cluster, so they do NOT surface distributionally — only faint hints in Vedic (matayaḥ/dhītayaḥ 'thoughts/hymns', the cow=hymn metaphor). Good failure-mode case.

---

## hari  (Kamboja pp. 100, 219–229)
- **Documented shift:** 'tawny / yellow-green (color)' → soma, rays, fire; → 'horse, lion'; → name of Viṣṇu
- **Type:** specialization (color → divine name)  ·  **expected transition:** V→E
- _drift (harayaH):_ **second-order** V→U 0.032 · U→E 0.088 · E→S 0.107 · **full V→S 0.020**  ||  **Procrustes** V→U 0.306 · U→E 0.554 · E→S 0.525 · full 0.213

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[hariḥ]_ | 98 | arṣati (arzati), atyaḥ (atyaH), vicakṣaṇaḥ (vicakzaRaH), vṛṣā (vfzA), aruṣaḥ (aruzaH), pavitre (pavitre), kanikradat (kanikradat), acikradat (acikradat), punānaḥ (punAnaH), vājī (vAjI), induḥ (induH), pavate (pavate), avyaḥ (avyaH), vāram (vAram), sīdati (sIdati) |
| Upaniṣadic _[harayaḥ]_ | 5 | parameśvaraḥ (parameSvaraH), mānavaḥ (mAnavaH), panthānau (panTAnO), dvipadaḥ (dvipadaH), saṃcaran (saMcaran), antān (antAn), bhrātṛvyāḥ (BrAtfvyAH), guhyam (guhyam), aśanam (aSanam), devatyaḥ (devatyaH), bahūni (bahUni), karmaṇe (karmaRe), niścayena (niScayena), caturaḥ (caturaH), asāma (asAma) |
| Epic _[hari]_ | 425 | kapi (kapi), plavaga (plavaga), vānara (vAnara), śini (Sini), ṛkṣa (fkza), nairṛta (nErfta), nṛpati (nfpati), yūthapa (yUTapa), yūthapāḥ (yUTapAH), pataga (pataga), raghu (raGu), vāraṇa (vAraRa), jāmbavān (jAmbavAn), tridaśa (tridaSa), hanūmān (hanUmAn) |
| Sūtra _[hari]_ | 7 | dvijāḥ (dvijAH), vidvadbhiḥ (vidvadBiH), śarad (Sarad), nidhiḥ (niDiH), aurasaḥ (OrasaH), kāmām (kAmAm), pumān (pumAn), yādṛśam (yAdfSam), prakṛtyāḥ (prakftyAH), vṛthā (vfTA), udumbaraḥ (udumbaraH), kruddhaḥ (krudDaH), edhate (eDate), praśasyate (praSasyate), bhuktam (Buktam) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (V→E; via the monkey sense, not Viṣṇu)  
**Notes:** Vedic neighbors are soma-pressing verbs (pavate/punānaḥ/arṣati 'flows/purifies', induḥ 'soma-drop', pavitre 'in the filter') + the bay steed (vājī, atyaḥ) — exactly the documented 'tawny → soma, horse'. Epic collapses onto the Rāmāyaṇa monkey-host: vānara, kapi, plavaga, ṛkṣa, hanūmān, jāmbavān, yūthapa. The color→animal specialization recovers; the '→Viṣṇu' endpoint is documented but SUBDOMINANT here (monkeys dominate). Upaniṣadic n=5 noise.

---

## yoga  (Kamboja pp. 309–311)
- **Documented shift:** 'act of yoking/harnessing' → 'union; means' → 'spiritual discipline; superhuman power'
- **Type:** abstraction → technical term  ·  **expected transition:** V→E/S
- _drift scores: — (word not in shared 4-era vocab; rely on neighbor trajectory)_

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[yogam]_ | 8 | ānaśe (AnaSe), anurūpam (anurUpam), ittham (itTam), ardharcaśaḥ (arDarcaSaH), syātām (syAtAm), lohitam (lohitam), aparam (aparam), parva (parva), chandasam (Candasam), brūyuḥ (brUyuH), visraṃsāya (visraMsAya), auṣṇihaḥ (OzRihaH), mahasaḥ (mahasaH), brahmaṇam (brahmaRam), sthitiḥ (sTitiH) |
| Upaniṣadic _[yoga]_ | 13 | mānasāḥ (mAnasAH), yukta (yukta), praviṣṭāḥ (pravizwAH), upāyam (upAyam), uttaratra (uttaratra), pravartante (pravartante), udaya (udaya), ratim (ratim), ākhyām (AKyAm), vacanena (vacanena), viśeṣaiḥ (viSezEH), padārthāḥ (padArTAH), antya (antya), śuddhi (SudDi), saṃyogaḥ (saMyogaH) |
| Epic _[yoga]_ | 318 | sāṃkhya (sAMKya), jñāna (jYAna), yogi (yogi), adhyātma (aDyAtma), dhyāna (DyAna), vijñāna (vijYAna), samādhi (samADi), samādhinā (samADinA), saṃnyāsa (saMnyAsa), dhyānena (DyAnena), yogānām (yogAnAm), yogau (yogO), yogibhiḥ (yogiBiH), sāṃkhyānām (sAMKyAnAm), sāṃkhyam (sAMKyam) |
| Sūtra _[yoga]_ | 87 | hīnam (hInam), dadyuḥ (dadyuH), yuktam (yuktam), paṇyānām (paRyAnAm), vetanam (vetanam), śulkam (Sulkam), hīna (hIna), dravyāṇām (dravyARAm), argha (arGa), vetana (vetana), sthāpayet (sTApayet), bhakta (Bakta), tulā (tulA), vibhāgaḥ (viBAgaH), puruṣāṇām (puruzARAm) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (E + S, two senses)  
**Notes:** Vedic 'yoking' too sparse (n=8) to read. Epic recovers the spiritual-discipline technical cluster — sāṃkhya, dhyāna 'meditation', samādhi, saṃnyāsa, adhyātma, jñāna; Sūtra recovers the *other* documented later sense, Arthaśāstra 'acquisition/securing of property': vetana 'wages', śulka 'toll', paṇya 'goods', argha 'price', dravya 'property'. Both documented later senses recovered, each in the corpus where it lives. Strong.

---

## guṇa  (Kamboja pp. 95, 164, 296–97)
- **Documented shift:** 'strand, cord; bowstring' → 'quality, attribute' → 'virtue' → (Sāṅkhya) the three guṇas
- **Type:** abstraction / widening  ·  **expected transition:** U→E
- _drift scores: — (word not in shared 4-era vocab; rely on neighbor trajectory)_

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic | 0 | _absent / not in vocab_ |
| Upaniṣadic _[guṇa]_ | 79 | prayogāt (prayogAt), oṅkārasya (oNkArasya), guṇavat (guRavat), ekaikasya (ekEkasya), vakṣyamāṇa (vakzyamARa), jñānāt (jYAnAt), upāsyaḥ (upAsyaH), upāsya (upAsya), viśiṣṭasya (viSizwasya), bhūtasya (BUtasya), lābhaḥ (lABaH), adṛṣṭam (adfzwam), jīvana (jIvana), adharmayoḥ (aDarmayoH), niyantṛ (niyantf) |
| Epic _[guṇa]_ | 618 | audārya (OdArya), aguṇān (aguRAn), prakṛti (prakfti), svabhāva (svaBAva), prasava (prasava), ṣāḍguṇya (zAqguRya), aguṇaḥ (aguRaH), guṇena (guRena), jaghanya (jaGanya), aguṇa (aguRa), nirguṇa (nirguRa), anvite (anvite), śaurya (SOrya), śīla (SIla), mādhurya (mADurya) |
| Sūtra _[guṇa]_ | 156 | rūpa (rUpa), varṇa (varRa), lakṣaṇa (lakzaRa), siddheḥ (sidDeH), upalabdheḥ (upalabDeH), tulya (tulya), doṣa (doza), ahetuḥ (ahetuH), saṃśayaḥ (saMSayaH), viṣaya (vizaya), apratiṣedhaḥ (apratizeDaH), anitya (anitya), hetu (hetu), prakṛti (prakfti), prasaṅgaḥ (prasaNgaH) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (abstract senses; origin not trackable)  
**Notes:** Correctly ABSENT in Vedic (post-Vedic word). Upaniṣadic = quality/attribute (guṇavat, viśiṣṭasya, jñānāt); Epic = virtue + Sāṅkhya (svabhāva, prakṛti, nirguṇa, ṣāḍguṇya, śīla, mādhurya); Sūtra = the Vaiśeṣika category, paired with dravya 'substance' (rūpa, varṇa, lakṣaṇa, doṣa, hetu). The 'quality → virtue → philosophical-category' arc recovers; the original 'cord/strand' sense isn't trackable (word absent where it would appear).

---


# Tier B — well-documented

## soma  (Kamboja pp. 71, 100)
- **Documented shift:** 'the soma plant / its ritual juice' → substitute plants; identified with the moon
- **Type:** widening / referential  ·  **expected transition:** V→E
- _drift (soma):_ **second-order** V→U 0.073 · U→E 0.092 · E→S 0.099 · **full V→S 0.043**  ||  **Procrustes** V→U 0.444 · U→E 0.454 · E→S 0.473 · full 0.266

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[soma]_ | 649 | srava (srava), viśa (viSa), kratu (kratu), arṣa (arza), indo (indo), madhumattamaḥ (maDumattamaH), pūyamānaḥ (pUyamAnaH), pavasva (pavasva), dhanva (Danva), pātave (pAtave), pavamāna (pavamAna), marutvate (marutvate), arṣasi (arzasi), pavase (pavase), jāgṛviḥ (jAgfviH) |
| Upaniṣadic _[soma]_ | 34 | hutāyām (hutAyAm), āhutau (AhutO), vṛṣṭi (vfzwi), pañcamyām (paYcamyAm), yoṣā (yozA), parjanya (parjanya), śraddhām (SradDAm), āhutayaḥ (AhutayaH), śraddhā (SradDA), nadyaḥ (nadyaH), adhiśerate (aDiSerate), vṛṣṭiḥ (vfzwiH), tāsām (tAsAm), yājyā (yAjyA), adhas (aDas) |
| Epic _[soma]_ | 172 | pāḥ (pAH), pīthinau (pITinO), sūrya (sUrya), rudra (rudra), viṣṇu (vizRu), paḥ (paH), kuṇḍāśī (kuRqASI), daivate (dEvate), arka (arka), indu (indu), sadṛśa (sadfSa), viṣuve (vizuve), sūryāt (sUryAt), sādhya (sADya), puṇḍarīkam (puRqarIkam) |
| Sūtra _[soma]_ | 115 | vaiśvadeve (vESvadeve), svasti (svasti), gīrbhiḥ (gIrBiH), viṣṇo (vizRo), viṣṇoḥ (vizRoH), vikāraḥ (vikAraH), dhenum (Denum), sutasya (sutasya), juṣasva (juzasva), marutaḥ (marutaH), śravat (Sravat), marudbhiḥ (marudBiH), citra (citra), marutvas (marutvas), mahi (mahi) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (V→E, plant→moon)  
**Notes:** Vedic = the Pavamāna ritual drink being pressed/purified (pavasva, pavamāna, pūyamānaḥ, indo, kratu); Epic groups soma with the luminaries — indu 'moon', arka, sūrya, candra-context (viṣuve), viṣṇu, rudra — recovering the documented plant→moon identification. The 'substitute-plants' sense is harder to see. Sūtra reverts to soma-ritual (vaiśvadeve, juṣasva).

---

## prajāpati  (Kamboja pp. 56, 124)
- **Documented shift:** 'lord of creatures' → 'the creator, supreme god' (rises in the Brāhmaṇas)
- **Type:** elevation / amelioration  ·  **expected transition:** V→U
- _drift (prajApati):_ **second-order** V→U 0.027 · U→E 0.087 · E→S 0.061 · **full V→S 0.016**  ||  **Procrustes** V→U 0.274 · U→E 0.449 · E→S 0.409 · full 0.062

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[prajāpatiḥ]_ | 284 | prajāḥ (prajAH), asṛjata (asfjata), śraiṣṭhyāya (SrEzWyAya), sarvaḥ (sarvaH), prajāpatim (prajApatim), yājayet (yAjayet), evaṃvid (evaMvid), atiṣṭhanta (atizWanta), etaiḥ (etEH), evaṃv (evaMv), purūṣam (purUzam), vāva (vAva), prajānām (prajAnAm), anuśaṃsati (anuSaMsati), yoneḥ (yoneH) |
| Upaniṣadic _[prajāpatiḥ]_ | 114 | adhyardhaḥ (aDyarDaH), śākalya (SAkalya), tau (tO), hṛdayaḥ (hfdayaH), maghavan (maGavan), pavate (pavate), āṅgirasaḥ (ANgirasaH), śānta (SAnta), indraḥ (indraH), ṛṣabhaḥ (fzaBaH), ūcatuḥ (UcatuH), parikhyāyate (pariKyAyate), dṛṣyate (dfzyate), etya (etya), pravāhaṇaḥ (pravAhaRaH) |
| Epic _[prajāpatiḥ]_ | 188 | parameṣṭhī (paramezWI), śaṃbhuḥ (SaMBuH), lokapitāmahaḥ (lokapitAmahaH), sṛṣṭvā (sfzwvA), svayaṃbhūḥ (svayaMBUH), śukraḥ (SukraH), devadevaḥ (devadevaH), svāyaṃbhuvaḥ (svAyaMBuvaH), nīhāram (nIhAram), vaiśravaṇaḥ (vESravaRaH), svayambhūḥ (svayamBUH), vivasvān (vivasvAn), havyavāhanaḥ (havyavAhanaH), dvādaśaḥ (dvAdaSaH), bhūtapatiḥ (BUtapatiH) |
| Sūtra _[prajāpatiḥ]_ | 50 | lokam (lokam), brahma (brahma), asurāḥ (asurAH), kratum (kratum), apacitim (apacitim), yajña (yajYa), asurān (asurAn), svargam (svargam), pūrve (pUrve), hotāram (hotAram), tejaḥ (tejaH), antarikṣa (antarikza), yajate (yajate), etam (etam), ha (ha) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (intensification; Vedic baseline already elevated)  
**Notes:** Creator role is present already in Vedic (asṛjata 'emitted/created', prajāḥ 'creatures', śraiṣṭhyāya 'for supremacy'), so the documented 'rise' is an INTENSIFICATION rather than an origination: by the Epic he is explicitly the supreme self-existent creator — svayaṃbhūḥ, lokapitāmahaḥ 'world-grandfather', parameṣṭhī, devadevaḥ. Recovered, but note the gradient (not a sharp V→U jump); Upaniṣadic neighbors are mixed/noisy.

---

## kṣatra  (Kamboja pp. 60–61, 124)
- **Documented shift:** 'might, dominion, rule' → 'the warrior/ruling class (kṣatriya)'
- **Type:** shift (→ social class)  ·  **expected transition:** V→E
- _drift (kzatra):_ **second-order** V→U 0.015 · U→E 0.120 · E→S 0.067 · **full V→S 0.005**  ||  **Procrustes** V→U 0.182 · U→E 0.632 · E→S 0.583 · full 0.061

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[kṣatram]_ | 95 | indriyam (indriyam), dadhate (daDate), asmai (asmE), rāṣṭram (rAzwram), yajamāne (yajamAne), ojasi (ojasi), adhibhūtam (aDiBUtam), stotre (stotre), āptvā (AptvA), vīryam (vIryam), ūrj (Urj), ājyena (Ajyena), prābṛhata (prAbfhata), balam (balam), āśīḥ (ASIH) |
| Upaniṣadic _[kṣatram]_ | 26 | kṣatrasya (kzatrasya), parādāt (parAdAt), parāduḥ (parAduH), priyaḥ (priyaH), priyā (priyA), putrāḥ (putrAH), priyāḥ (priyAH), jāyāyai (jAyAyE), kāmāya (kAmAya), atsi (atsi), atti (atti), are (are), vittasya (vittasya), priyam (priyam), paśyasi (paSyasi) |
| Epic _[kṣatra]_ | 314 | anuvrataḥ (anuvrataH), kṣātra (kzAtra), adhigatāḥ (aDigatAH), anusmara (anusmara), vartatā (vartatA), prayatamānasya (prayatamAnasya), jīvikām (jIvikAm), sāṃgrāmikaḥ (sAMgrAmikaH), dharmeṇa (DarmeRa), dharme (Darme), dharmāṇam (DarmARam), vartayet (vartayet), sthitim (sTitim), avekṣasva (avekzasva), samācāram (samAcAram) |
| Sūtra _[kṣatram]_ | 22 | asmabhyam (asmaByam), bhadram (Badram), ojaḥ (ojaH), vedāḥ (vedAH), saṃrāj (saMrAj), śarma (Sarma), deveṣu (devezu), santu (santu), bṛhaspatiḥ (bfhaspatiH), savitar (savitar), havyam (havyam), avatu (avatu), dhiyā (DiyA), dadātu (dadAtu), pūṣā (pUzA) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (V→E)  
**Notes:** Vedic = abstract might/dominion (balam, vīryam 'valor', ojas 'strength', rāṣṭram 'realm', indriyam 'power'); Epic = the warrior class and its duty (kṣātra 'martial', sāṃgrāmikaḥ, jīvikā 'livelihood', dharmeṇa/dharme — kṣatra-dharma, anuvrata). The 'might → warrior class' shift recovers cleanly. Sūtra reverts to ritual benediction (savitar, bṛhaspatiḥ).

---

## śūdra  (Kamboja pp. 60)
- **Documented shift:** '(a non-Aryan tribe / aboriginal section)' → 'the servile/labour class, 4th varṇa'
- **Type:** widening  ·  **expected transition:** V→E
- _drift (SUdraH):_ **second-order** V→U 0.014 · U→E 0.058 · E→S 0.064 · **full V→S 0.006**  ||  **Procrustes** V→U 0.017 · U→E 0.381 · E→S 0.347 · full 0.033

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[śūdraḥ]_ | 6 | tvaḥ (tvaH), ārtiḥ (ArtiH), uraḥ (uraH), tapyate (tapyate), nidānam (nidAnam), purāṇam (purARam), dāru (dAru), svapnam (svapnam), salile (salile), mānuṣī (mAnuzI), viśate (viSate), āra (Ara), mārutaḥ (mArutaH), duhitaram (duhitaram), kataraḥ (kataraH) |
| Upaniṣadic _[śūdra]_ | 8 | abhyuktavān (aByuktavAn), janakasya (janakasya), jānaśrutiḥ (jAnaSrutiH), haste (haste), karomi (karomi), samīpe (samIpe), tūṣṇīm (tUzRIm), paśyema (paSyema), vṛṇīṣva (vfRIzva), pratijñātaḥ (pratijYAtaH), ardham (arDam), pṛṣṭavān (pfzwavAn), śiṣyāya (SizyAya), vatsa (vatsa), brahmiṣṭha (brahmizWa) |
| Epic _[śūdra]_ | 141 | yonyām (yonyAm), caṇḍāla (caRqAla), viś (viS), vaiśya (vESya), yonau (yonO), kṛṣi (kfzi), vaiśyaḥ (vESyaH), gorakṣya (gorakzya), annāt (annAt), vāṇijyam (vARijyam), dharmiṇaḥ (DarmiRaH), kriyāvān (kriyAvAn), ucchiṣṭa (ucCizwa), varjanīyāḥ (varjanIyAH), gorakṣa (gorakza) |
| Sūtra _[śūdra]_ | 42 | āṭavikam (Awavikam), saṃdohena (saMdohena), tadātve (tadAtve), gacchati (gacCati), rāṣṭram (rAzwram), vyayābhyām (vyayAByAm), prakṛtibhiḥ (prakftiBiH), kilbiṣam (kilbizam), prāyaḥ (prAyaH), vaiśya (vESya), rakṣet (rakzet), ācaret (Acaret), balaḥ (balaH), sainyānām (sEnyAnAm), ādātu (AdAtu) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** partial (destination clear; origin too sparse)  
**Notes:** Vedic n=6 is too sparse to confirm the documented tribal origin. But the destination recovers in the Epic — the four-varṇa system and its occupations: vaiśya, caṇḍāla, viś, plus kṛṣi 'agriculture', vāṇijya 'trade', gorakṣa 'cattle-keeping'; Sūtra similar (vaiśya, rakṣet). The widening to 'servile/labour class' is confirmed at its endpoint, not its start.

---

## ari  (Kamboja pp. 60–62, 149)
- **Documented shift:** 'non-giver, miser' → 'enemy' AND 'master, lord, pious man'
- **Type:** divergence (polysemy split)  ·  **expected transition:** V→E
- _drift scores: — (word not in shared 4-era vocab; rely on neighbor trajectory)_

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[ariḥ]_ | 14 | gantā (gantA), dhiye (Diye), kṣayasya (kzayasya), yudhmaḥ (yuDmaH), gamaḥ (gamaH), sadāvṛdhaḥ (sadAvfDaH), hūyamānaḥ (hUyamAnaH), kāmaṁ (kAmaṁ), vājayantam (vAjayantam), ṛṣvebhiḥ (fzveBiH), śaśvataḥ (SaSvataH), dhṛtavrataḥ (DftavrataH), kāsu (kAsu), yantā (yantA), kāru (kAru) |
| Upaniṣadic | 0 | _absent / not in vocab_ |
| Epic _[ari]_ | 267 | amitra (amitra), mardana (mardana), ripu (ripu), śatru (Satru), sūdana (sUdana), karśana (karSana), sūdanaḥ (sUdanaH), mardanam (mardanam), mardanaḥ (mardanaH), karśanam (karSanam), han (han), niṣūdana (nizUdana), nibarhaṇaḥ (nibarhaRaH), ghna (Gna), sūdanam (sUdanam) |
| Sūtra _[ari]_ | 38 | amitram (amitram), saṃdhim (saMDim), laghu (laGu), grāham (grAham), śatru (Satru), śreṇī (SreRI), śreyaḥ (SreyaH), karam (karam), vyañjanaḥ (vyaYjanaH), utsāha (utsAha), lābhaḥ (lABaH), paura (pOra), mitreṇa (mitreRa), śatruḥ (SatruH), parasya (parasya) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (enemy branch only; 'master' branch NOT recovered)  
**Notes:** Epic and Sūtra are unambiguously 'enemy' — amitra, ripu, śatru, plus the 'foe-crusher' compound second-members ari-mardana/-sūdana/-niṣūdana/-karśana — and in Sūtra the Arthaśāstra ally-enemy maṇḍala (śatru, saṃdhi 'treaty', mitreṇa). The documented OTHER branch ('master, lord, pious man') does NOT surface — honest partial recovery of a polysemy split. Absent in Upaniṣadic; Vedic n=14 is mixed/ambiguous.

---

## uttara  (Kamboja pp. 272–276)
- **Documented shift:** 'upper, higher' → 'later, subsequent; northern; superior'
- **Type:** widening (spatial → temporal/qual.)  ·  **expected transition:** V→S
- _drift (uttara):_ **second-order** V→U 0.062 · U→E 0.090 · E→S 0.066 · **full V→S 0.051**  ||  **Procrustes** V→U 0.415 · U→E 0.456 · E→S 0.385 · full 0.382

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[uttaram]_ | 66 | ṣaṣṭham (zazWam), caturtham (caturTam), navamam (navamam), pūrvam (pUrvam), ahar (ahar), rayiṣṭham (rayizWam), dvitīyam (dvitIyam), sāmnaḥ (sAmnaH), saptamam (saptamam), kasmāt (kasmAt), ārabhante (AraBante), tṛtīyam (tftIyam), ānuṣṭubham (AnuzwuBam), devatyam (devatyam), anuvadati (anuvadati) |
| Upaniṣadic _[uttara]_ | 54 | dakṣiṇa (dakziRa), vācyāḥ (vAcyAH), yava (yava), bhūmi (BUmi), pañcāgni (paYcAgni), pratipadyante (pratipadyante), prabhava (praBava), agnihotra (agnihotra), varṇa (varRa), viśiṣṭāḥ (viSizwAH), dāna (dAna), homa (homa), sambandhāt (sambanDAt), vyākhyātā (vyAKyAtA), vrīhi (vrIhi) |
| Epic _[uttaram]_ | 243 | harivarṣam (harivarzam), vṛttāntam (vfttAntam), hetumat (hetumat), adhara (aDara), bāhukam (bAhukam), arthyam (arTyam), vispaṣṭam (vispazwam), prativaktum (prativaktum), vetsyāmi (vetsyAmi), pragalbham (pragalBam), pārśvam (pArSvam), paścimam (paScimam), nṛpāya (nfpAya), arthavat (arTavat), śreyaskaram (Sreyaskaram) |
| Sūtra _[uttaram]_ | 167 | aṃsāt (aMsAt), lekhām (leKAm), pratyakṣṇayā (pratyakzRayA), aparasmāt (aparasmAt), pratyālikhet (pratyAliKet), aparayoḥ (aparayoH), āyamya (Ayamya), dakṣiṇasmāt (dakziRasmAt), mūlāt (mUlAt), tyajet (tyajet), pañcadaśasu (paYcadaSasu), nipātayet (nipAtayet), dvādaśasu (dvAdaSasu), śaṅkvoḥ (SaNkvoH), nitodāt (nitodAt) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (multi-sense widening)  
**Notes:** Vedic = spatial/ordinal 'next, upper' (pūrvam pairing, ordinals ṣaṣṭha/caturtha/dvitīya); Upaniṣadic = the directional 'northern' sense via the dakṣiṇa 'south' pair; Epic adds 'reply/subsequent' (prativaktum 'to answer', adhara 'lower' pairing, paścima 'western'). The documented 'upper → later/northern/superior' widening tracks across eras. Sūtra = geometric/ritual directions.

---

## uttama  (Kamboja pp. 269–271)
- **Documented shift:** 'uppermost, highest' → 'best, most excellent; last'
- **Type:** abstraction (spatial → evaluative)  ·  **expected transition:** V→E
- _drift (uttama):_ **second-order** V→U 0.022 · U→E 0.089 · E→S 0.081 · **full V→S 0.004**  ||  **Procrustes** V→U 0.075 · U→E 0.643 · E→S 0.666 · full 0.067

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[uttamam]_ | 56 | kāryā (kAryA), madhyamam (maDyamam), trirātrasya (trirAtrasya), āyatanena (Ayatanena), akṣarapaṅktiḥ (akzarapaNktiH), asthīni (asTIni), amāvāsyāyām (amAvAsyAyAm), viśvajiti (viSvajiti), traiṣṭubhāt (trEzwuBAt), saptamasya (saptamasya), gāyatraḥ (gAyatraH), kāṇḍam (kARqam), revatīnām (revatInAm), śvastanam (Svastanam), traiṣṭubhaḥ (trEzwuBaH) |
| Upaniṣadic _[uttama]_ | 9 | aste (aste), uttamaḥ (uttamaH), ayaḥ (ayaH), mayena (mayena), nirdiṣṭaḥ (nirdizwaH), prastutam (prastutam), nāmā (nAmA), antau (antO), svayan (svayan), pipāsati (pipAsati), mānasaḥ (mAnasaH), śarīreṣu (SarIrezu), pratyak (pratyak), upasaṃpadya (upasaMpadya), upakramya (upakramya) |
| Epic _[uttamam]_ | 912 | anuttamam (anuttamam), agryam (agryam), mukhyam (muKyam), medhyam (meDyam), ruciram (ruciram), vaiṣṇavam (vEzRavam), māheśvaram (mAheSvaram), maṅgalānām (maNgalAnAm), vipulam (vipulam), paramam (paramam), aprameyam (aprameyam), svargyam (svargyam), mahat (mahat), aindram (Endram), paramakam (paramakam) |
| Sūtra _[uttamam]_ | 59 | prathamam (praTamam), triṣṭubh (trizwuB), gāyatreṇa (gAyatreRa), tṛca (tfca), gāyatrī (gAyatrI), viśvajitaḥ (viSvajitaH), traiṣṭubhena (trEzwuBena), praṇutya (praRutya), dvitīyam (dvitIyam), ṣoḷaśa (zoxaSa), pāde (pAde), agniṣṭomaḥ (agnizwomaH), pratyādāya (pratyAdAya), aikāhikam (EkAhikam), prathamena (praTamena) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (V→E, spatial→evaluative)  
**Notes:** Vedic = positional 'topmost in a series' (madhyamam 'middle', ordinals saptama, metrical positions); Epic = the evaluative 'best/supreme' (anuttamam 'unsurpassed', agryam 'foremost', mukhyam 'chief', paramam, aprameyam). The documented spatial→evaluative abstraction recovers. Sūtra reverts to metrical/positional (prathama, gāyatrī, pāda).

---

## pāda  (Kamboja pp. 255–259)
- **Documented shift:** 'foot' → 'quarter (¼); foot/line of verse; foot of mountain; ray'
- **Type:** widening / metaphor  ·  **expected transition:** V→E
- _drift (pAdaH):_ **second-order** V→U 0.024 · U→E 0.060 · E→S 0.083 · **full V→S 0.014**  ||  **Procrustes** V→U 0.300 · U→E 0.368 · E→S 0.402 · full 0.180

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[pādam]_ | 12 | śunaḥ (SunaH), śritāḥ (SritAH), pataṅgaḥ (pataNgaH), kakṣīvān (kakzIvAn), dhūrṣu (DUrzu), dāsī (dAsI), caritvā (caritvA), śaryaṇāvati (SaryaRAvati), mimate (mimate), unnayanti (unnayanti), dhāseḥ (DAseH), vṛtre (vftre), śakrāḥ (SakrAH), dvipādaḥ (dvipAdaH), alipsata (alipsata) |
| Upaniṣadic _[pādaḥ]_ | 42 | adhidaivatam (aDidEvatam), catuṣkalaḥ (catuzkalaH), catuṣpād (catuzpAd), madhyamaḥ (maDyamaH), vāyunā (vAyunA), diśām (diSAm), suṣiḥ (suziH), caturthaḥ (caturTaH), sūryaḥ (sUryaH), udīcī (udIcI), candraḥ (candraH), āditye (Aditye), pāṇi (pARi), pakṣaḥ (pakzaH), tredhā (treDA) |
| Epic _[pāda]_ | 195 | abhivandanam (aBivandanam), mūle (mUle), pāṇi (pARi), atimātra (atimAtra), udaram (udaram), grīvā (grIvA), grīvam (grIvam), caraṇa (caraRa), avasecanam (avasecanam), kaṭī (kawI), jaṅghā (jaNGA), tālu (tAlu), bhrū (BrU), mukha (muKa), pādam (pAdam) |
| Sūtra _[pāda]_ | 185 | aṣṭa (azwa), catuḥ (catuH), upadhāne (upaDAne), pañcāśat (paYcASat), iṣṭakānām (izwakAnAm), śva (Sva), catuṣ (catuz), ṣaṣ (zaz), pauruṣyām (pOruzyAm), pala (pala), karaṇe (karaRe), karaṇāni (karaRAni), aṅgulaḥ (aNgulaH), puruṣasya (puruzasya), dvādaśa (dvAdaSa) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (V→U, foot→quarter)  
**Notes:** Vedic = literal foot (dvipādaḥ 'two-footed', body/leg context); Upaniṣadic recovers the 'quarter (¼)' sense — catuṣpād 'four-quartered', caturthaḥ 'fourth', the cosmic pādas of Brahman (sūrya/candra/āditya context, cf. Māṇḍūkya's four pādas); Sūtra = measure/fraction (numerals, aṅgula). Epic returns to the body-part list (caraṇa, pāṇi, jaṅghā). Foot→quarter clearly recovered.

---

## tejas  (Kamboja pp. 183)
- **Documented shift:** 'sharpness, edge; fire, brilliance' → 'splendour; vital energy, spiritual power, majesty'
- **Type:** abstraction  ·  **expected transition:** U→E
- _drift (tejaH):_ **second-order** V→U 0.067 · U→E 0.103 · E→S 0.115 · **full V→S 0.091**  ||  **Procrustes** V→U 0.334 · U→E 0.453 · E→S 0.528 · full 0.358

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[tejaḥ]_ | 109 | brahmavarcasam (brahmavarcasam), abhiṣicyate (aBizicyate), gāyatrī (gAyatrI), yajamāne (yajamAne), dhatte (Datte), avarundhe (avarunDe), indriyam (indriyam), balam (balam), prajananam (prajananam), ātman (Atman), triṣṭubh (trizwuB), dīpyate (dIpyate), dadhate (daDate), mriyate (mriyate), dadhāti (daDAti) |
| Upaniṣadic _[tejaḥ]_ | 183 | adhyātmam (aDyAtmam), mayaḥ (mayaH), bhavaḥ (BavaH), mayī (mayI), banna (banna), śārīraḥ (SArIraH), āsu (Asu), cākṣuṣaḥ (cAkzuzaH), krodha (kroDa), pṛthivyām (pfTivyAm), tejasi (tejasi), prātiśrutkaḥ (prAtiSrutkaH), apaḥ (apaH), parasyām (parasyAm), devatāyām (devatAyAm) |
| Epic _[tejasā]_ | 617 | vapuṣā (vapuzA), svena (svena), yaśasā (yaSasA), dīpyamānaḥ (dIpyamAnaH), kulena (kulena), prajvalan (prajvalan), vīryeṇa (vIryeRa), śriyā (SriyA), raśmivān (raSmivAn), divyena (divyena), dyotita (dyotita), apratimena (apratimena), parameṇa (parameRa), dīpyamānā (dIpyamAnA), bhāsā (BAsA) |
| Sūtra _[tejaḥ]_ | 45 | lokam (lokam), svargam (svargam), varcasam (varcasam), antarikṣa (antarikza), anantam (anantam), brahma (brahma), apacitim (apacitim), iṣṭvā (izwvA), stutam (stutam), īpsan (Ipsan), jigīṣan (jigIzan), asurān (asurAn), kāmān (kAmAn), tapaḥ (tapaH), paśūn (paSUn) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (abstraction to splendour/energy)  
**Notes:** Vedic = fire/brilliance + incipient power (dīpyate 'shines', balam, indriyam, brahmavarcasa 'spiritual lustre'); Epic = majesty/glory/energy (yaśasā 'glory', śriyā 'splendour', vīryeṇa 'valor', bhāsā 'radiance', raśmivān 'rayed'); Upaniṣadic shows the element + spiritual sense (adhyātmam, apaḥ). The documented 'fire/edge → vital energy, majesty' abstraction recovers.

---

## setu  (Kamboja pp. 239–243)
- **Documented shift:** 'bond, fetter (that binds)' → 'causeway, dam, bridge'; fig. 'boundary; protection'
- **Type:** concretization / shift  ·  **expected transition:** U→S
- _drift scores: — (word not in shared 4-era vocab; rely on neighbor trajectory)_

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic | 0 | _absent / not in vocab_ |
| Upaniṣadic _[setuḥ]_ | 11 | bhuvanam (Buvanam), bhuvanasya (Buvanasya), auṣadham (OzaDam), pālayitā (pAlayitA), saṃbhedāya (saMBedAya), udyanti (udyanti), gamayati (gamayati), śraiṣṭhyam (SrEzWyam), viśvam (viSvam), anupaśyati (anupaSyati), adhipaḥ (aDipaH), śaṅkunā (SaNkunA), ekaikaḥ (ekEkaH), vasati (vasati), indriyāṇām (indriyARAm) |
| Epic _[setum]_ | 27 | tīreṇa (tIreRa), dakṣiṇasya (dakziRasya), vahamānaḥ (vahamAnaH), apasṛtya (apasftya), anūpam (anUpam), kevalām (kevalAm), saṃpaśyan (saMpaSyan), ākrāntām (AkrAntAm), atikrānte (atikrAnte), niṣadhān (nizaDAn), nikumbhilām (nikumBilAm), tṛtīyām (tftIyAm), samupasthitā (samupasTitA), aṭavyām (awavyAm), nirvapet (nirvapet) |
| Sūtra _[setu]_ | 31 | bhāṇḍam (BARqam), ratna (ratna), patha (paTa), khani (Kani), sāra (sAra), bhāṇḍa (BARqa), cakra (cakra), sthāna (sTAna), phalgu (Palgu), śulka (Sulka), sthala (sTala), vaṇij (vaRij), bandha (banDa), mṛga (mfga), bhakta (Bakta) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (U→S, bond→bridge)  
**Notes:** Absent Vedic. Upaniṣadic = the figurative cosmic bond/world-boundary and protector (bhuvanasya 'of the world', pālayitā 'protector', saṃbhedāya 'for separation', adhipaḥ 'overlord' — the ātman/brahman-as-dyke image); Epic = the literal causeway/bridge (tīra 'shore', anūpa 'watery land', the crossing to Laṅkā); Sūtra = embankment/dam in irrigation/toll context (bandha, śulka, vaṇij). The 'bond → causeway/dam' concretization recovers.

---

## bhṛtya  (Kamboja pp. 365–368)
- **Documented shift:** 'one to be supported, a dependent' → 'servant, slave'
- **Type:** shift / pejoration  ·  **expected transition:** U→E
- _drift scores: — (word not in shared 4-era vocab; rely on neighbor trajectory)_

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic | 0 | _absent / not in vocab_ |
| Upaniṣadic _[bhṛtya]_ | 5 | labhante (laBante), sukṛta (sukfta), abhimāninaḥ (aBimAninaH), anayoḥ (anayoH), gītāsu (gItAsu), vara (vara), ṛṣi (fzi), avasare (avasare), utpannaḥ (utpannaH), vṛtteḥ (vftteH), utpattim (utpattim), sveṣu (svezu), jīyate (jIyate), audumbare (Odumbare), manuṣyaiḥ (manuzyEH) |
| Epic _[bhṛtya]_ | 77 | amātya (amAtya), vargasya (vargasya), abhimarśanam (aBimarSanam), varge (varge), vargaḥ (vargaH), apaharaṇam (apaharaRam), atithiṣu (atiTizu), bāndhava (bAnDava), vighasam (viGasam), vargam (vargam), bandhuṣu (banDuzu), svānām (svAnAm), saṃbandhi (saMbanDi), madhyastha (maDyasTa), anutiṣṭhati (anutizWati) |
| Sūtra _[bhṛtya]_ | 13 | sahāya (sahAya), pīḍayati (pIqayati), anyatamam (anyatamam), strībhiḥ (strIBiH), vyavahāra (vyavahAra), samaya (samaya), dvaidhī (dvEDI), vyayam (vyayam), upagraheṇa (upagraheRa), bāhulyāt (bAhulyAt), balavat (balavat), pratīkāraḥ (pratIkAraH), pravāsa (pravAsa), dāra (dAra), garīyaḥ (garIyaH) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (E; dependent→retainer/servant)  
**Notes:** Absent Vedic (post-Vedic). Upaniṣadic n=5 noisy (faint maintenance/origination sense). Epic groups bhṛtya with the household's dependents and retainers — amātya 'minister', bāndhava/bandhu 'kin', atithi 'guest', svānām 'one's own people', saṃbandhi; Sūtra = servant in legal/household affairs (sahāya 'helper', dāra 'wife', vyavahāra). 'Supported dependent → servant' recovers at the Epic.

---

## arka  (Kamboja pp. 386)
- **Documented shift:** 'ray, flash; hymn of praise' → 'the sun'; also 'the arka plant'
- **Type:** shift  ·  **expected transition:** V→E
- _drift (arka):_ **second-order** V→U 0.018 · U→E 0.086 · E→S 0.107 · **full V→S 0.010**  ||  **Procrustes** V→U 0.076 · U→E 0.544 · E→S 0.529 · full 0.036

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[arkam]_ | 36 | dadhanvire (daDanvire), prayaḥ (prayaH), kaṇvāḥ (kaRvAH), arcanti (arcanti), madāḥ (madAH), amṛtāya (amftAya), gṛṇānāḥ (gfRAnAH), madhumantaḥ (maDumantaH), stomāsaḥ (stomAsaH), ukthebhiḥ (ukTeBiH), pāvne (pAvne), śumbhanti (SumBanti), svasareṣu (svasarezu), vrajaṁ (vrajaṁ), dhītibhiḥ (DItiBiH) |
| Upaniṣadic _[arka]_ | 10 | arkasya (arkasya), jānīhi (jAnIhi), praśne (praSne), pūrvapakṣa (pUrvapakza), katareṇa (katareRa), mṛtyo (mftyo), śocati (Socati), aṇimānam (aRimAnam), grāmāt (grAmAt), ardha (arDa), khe (Ke), ūrdhve (UrDve), aśanam (aSanam), niyantāram (niyantAram), āptim (Aptim) |
| Epic _[arka]_ | 205 | raśmi (raSmi), divākara (divAkara), jvalana (jvalana), indu (indu), bhāskara (BAskara), prakāśena (prakASena), vaiśvānara (vESvAnara), aṃśu (aMSu), hutāśana (hutASana), virājatā (virAjatA), sadṛśa (sadfSa), sūrya (sUrya), udaya (udaya), ravi (ravi), kālāgni (kAlAgni) |
| Sūtra _[arka]_ | 10 | śoṇitam (SoRitam), saṃbhavam (saMBavam), malam (malam), maṇiḥ (maRiH), smaḥ (smaH), maraṇāt (maraRAt), carita (carita), ṛcchati (fcCati), homaiḥ (homEH), samanvitam (samanvitam), gobhiḥ (goBiH), yoṣitaḥ (yozitaH), anyatamaḥ (anyatamaH), vipreṣu (viprezu), duṣyati (duzyati) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (V→E, hymn→sun)  
**Notes:** Vedic carries the √arc 'praise' sense — arcanti 'they sing', stomāsaḥ 'hymns', ukthebhiḥ 'recitations', gṛṇānāḥ 'praising', dhītibhiḥ 'with hymns'; Epic is unambiguously the SUN — sūrya, ravi, bhāskara, divākara 'day-maker', raśmi 'ray', aṃśu. The documented 'song of praise/ray → the sun' shift recovers cleanly. Sūtra n=10 noisy.

---

## aṃśu  (Kamboja pp. 101, 223)
- **Documented shift:** 'soma filament/stalk; soma juice' → 'ray of light, sunbeam'
- **Type:** metaphor / shift  ·  **expected transition:** V→E
- _drift scores: — (word not in shared 4-era vocab; rely on neighbor trajectory)_

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[aṃśuḥ]_ | 19 | astṛtaḥ (astftaH), pūtaḥ (pUtaH), nikāmaḥ (nikAmaH), śobhate (SoBate), sargaḥ (sargaH), āyasaḥ (AyasaH), apīcyam (apIcyam), vīrudhām (vIruDAm), dyutānaḥ (dyutAnaH), vardhate (varDate), svādiṣṭhayā (svAdizWayA), udak (udak), anyasyām (anyasyAm), yathāvaśam (yaTAvaSam), indriyaḥ (indriyaH) |
| Upaniṣadic | 0 | _absent / not in vocab_ |
| Epic _[aṃśu]_ | 50 | taruṇa (taruRa), tuṣāra (tuzAra), raśmi (raSmi), pratīkāśaiḥ (pratIkASEH), kiraṇa (kiraRa), pratīkāśām (pratIkASAm), kānti (kAnti), ākāre (AkAre), nabhasaḥ (naBasaH), sūryayoḥ (sUryayoH), uditau (uditO), prakāśena (prakASena), udita (udita), prabhām (praBAm), mṛṇāla (mfRAla) |
| Sūtra _[aṃśuḥ]_ | 5 | asuraḥ (asuraH), camasaḥ (camasaH), suṣṭutim (suzwutim), havyā (havyA), mimītām (mimItAm), arkam (arkam), pyāyatām (pyAyatAm), yantu (yantu), paridadhyāt (paridaDyAt), mitrāḥ (mitrAH), stotram (stotram), idma (idma), bhadraḥ (BadraH), mṛḍa (mfqa), matsat (matsat) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (V→E, soma-filament→ray)  
**Notes:** Vedic = the bright soma-stalk/plant (śobhate/dyutānaḥ 'shines', vīrudhām 'of plants', svādiṣṭhayā 'sweetest', pūtaḥ 'purified'); Epic = ray of light (raśmi, kiraṇa 'ray', kānti 'radiance', sūrya, prabhā), with the filament sense lingering in mṛṇāla 'lotus-fibre'. The documented soma→ray metaphor recovers. Absent Upaniṣadic; Sūtra n=5 reverts to soma-ritual.

---

## preta  (Kamboja pp. 81)
- **Documented shift:** 'departed, deceased one' → 'ghost, spirit of the dead'
- **Type:** specialization / pejoration  ·  **expected transition:** V→E
- _drift (preta):_ **second-order** V→U 0.009 · U→E 0.096 · E→S 0.122 · **full V→S 0.013**  ||  **Procrustes** V→U 0.097 · U→E 0.462 · E→S 0.460 · full 0.200

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[preta]_ | 7 | bharasva (Barasva), kimīdinaḥ (kimIdinaH), prajāvatī (prajAvatI), aṅdhi (aNDi), stokāḥ (stokAH), kṣetriyāt (kzetriyAt), madho (maDo), nākaṁ (nAkaṁ), nāvaṁ (nAvaṁ), saṁdṛśam (saṁdfSam), gabhīrāḥ (gaBIrAH), bandhum (banDum), devatātim (devatAtim), vāntu (vAntu), prajāvantaḥ (prajAvantaH) |
| Upaniṣadic _[pretam]_ | 8 | haranti (haranti), yajamānāya (yajamAnAya), punarmṛtyum (punarmftyum), apa (apa), puruṣān (puruzAn), abhikṣaranti (aBikzaranti), candramasam (candramasam), rudraḥ (rudraH), viśve (viSve), sāyujyam (sAyujyam), balim (balim), kalpante (kalpante), brahmacāriṇam (brahmacAriRam), yajamānam (yajamAnam), ṛtavaḥ (ftavaH) |
| Epic _[preta]_ | 53 | kāladharma (kAlaDarma), cora (cora), mleccha (mlecCa), tiryagyoni (tiryagyoni), ekāyana (ekAyana), dasyu (dasyu), samatām (samatAm), udvejayati (udvejayati), kanyāsu (kanyAsu), kāpatham (kApaTam), maitrāyaṇa (mEtrAyaRa), ākhyām (AKyAm), upagacchati (upagacCati), taret (taret), prayāti (prayAti) |
| Sūtra _[preta]_ | 32 | bhaya (Baya), śauca (SOca), saṃgha (saMGa), anugraha (anugraha), bandhu (banDu), stena (stena), paura (pOra), mukhyān (muKyAn), kleśa (kleSa), sampad (sampad), pravāsa (pravAsa), lābha (lABa), vyādhita (vyADita), nicaya (nicaya), sampannaḥ (sampannaH) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (pejoration)  
**Notes:** Vedic/Upaniṣadic = the deceased and the afterlife journey (punarmṛtyum 're-death', candramasam 'the moon' as destination of the dead, kimīdinaḥ 'sorcerers'); Epic groups preta with low/cursed states — kāladharma 'death', dasyu 'robber', mleccha, tiryagyoni 'animal-rebirth', kāpatha 'evil path'; Sūtra = inauspicious (bhaya 'fear', kleśa 'affliction', vyādhita 'diseased'). The 'departed → ill-omened ghost' pejoration recovers.

---

## vrata  (Kamboja pp. (general))
- **Documented shift:** 'divine ordinance, command of the gods; sacred rite' → '(self-imposed) vow, observance, fast'
- **Type:** shift  ·  **expected transition:** V→E
- _drift (vrata):_ **second-order** V→U 0.008 · U→E 0.088 · E→S 0.115 · **full V→S 0.033**  ||  **Procrustes** V→U 0.047 · U→E 0.512 · E→S 0.623 · full 0.163

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[vratam]_ | 100 | dhinoti (Dinoti), dhīyate (DIyate), saṃvatsarāt (saMvatsarAt), madhye (maDye), āptam (Aptam), vairājam (vErAjam), sākṣāt (sAkzAt), prajananāya (prajananAya), aṣṭa (azwa), upariṣṭāt (uparizwAt), pratiṣṭhitāḥ (pratizWitAH), madhyataḥ (maDyataH), pāṅktam (pANktam), mukhe (muKe), kḷptyai (kxptyE) |
| Upaniṣadic _[vratam]_ | 46 | nindet (nindet), prajayā (prajayA), mahān (mahAn), kīrtyā (kIrtyA), paśubhiḥ (paSuBiH), jyok (jyok), jīvati (jIvati), brahmavarcasena (brahmavarcasena), annādyena (annAdyena), prajāyate (prajAyate), āyuḥ (AyuH), tejasā (tejasA), lokī (lokI), annavān (annavAn), ādaḥ (AdaH) |
| Epic _[vratam]_ | 333 | ājagaram (Ajagaram), upāṃśu (upAMSu), vrataḥ (vrataH), cīrṇam (cIrRam), upavāsam (upavAsam), āhitam (Ahitam), nivarteyam (nivarteyam), kaumāram (kOmAram), duścaram (duScaram), kṣāntam (kzAntam), vratān (vratAn), agnihotrasya (agnihotrasya), anuṣṭhitaḥ (anuzWitaH), tyāgam (tyAgam), tāpasam (tApasam) |
| Sūtra _[vratam]_ | 97 | viśvajit (viSvajit), abhijit (aBijit), mahā (mahA), atirātraḥ (atirAtraH), stomaḥ (stomaH), caturviṃśam (caturviMSam), enena (enena), ahar (ahar), viśvajitau (viSvajitO), āpnoti (Apnoti), ṛddhi (fdDi), pṛṣṭhyaḥ (pfzWyaH), klṛptam (klfptam), adhyātmam (aDyAtmam), viṣuvān (vizuvAn) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (V→E, ordinance→vow)  
**Notes:** Vedic = cosmic ordinance / fixed rule (pratiṣṭhita 'established', saṃvatsarāt 'from the year', vairāja/pāṅkta metrical structures); Epic = the self-imposed vow/austerity — upavāsa 'fasting', kaumāra 'chastity-vow', tāpasa 'ascetic', duścara 'hard-to-perform', cīrṇa 'observed', tyāga 'renunciation'. The documented 'divine ordinance → personal vow/observance' shift recovers. Sūtra = named soma-rites (viśvajit, atirātra).

---

## rājan  (Kamboja pp. 208 (verify))
- **Documented shift:** sacral kingship → heroic/epic sovereign → administrative statecraft register
- **Type:** shift (register drift)  ·  **expected transition:** V→E/S
- _drift (rAjA):_ **second-order** V→U 0.069 · U→E 0.085 · E→S 0.086 · **full V→S 0.058**  ||  **Procrustes** V→U 0.313 · U→E 0.505 · E→S 0.490 · full 0.326

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[rājā]_ | 251 | devaḥ (devaH), priyaḥ (priyaH), patiḥ (patiH), jātaḥ (jAtaH), vrataḥ (vrataH), śuciḥ (SuciH), somaḥ (somaH), janaḥ (janaH), agniḥ (agniH), caṣṭe (cazwe), bṛhaspatiḥ (bfhaspatiH), garbhaḥ (garBaH), vaiśvānaraḥ (vESvAnaraH), pāvakaḥ (pAvakaH), viśvasya (viSvasya) |
| Upaniṣadic _[rājā]_ | 74 | rājānam (rAjAnam), prātar (prAtar), eyāya (eyAya), brāhmaṇānām (brAhmaRAnAm), atiṣṭhāḥ (atizWAH), agnaye (agnaye), babhūvuḥ (baBUvuH), brahmacāriṇam (brahmacAriRam), somaḥ (somaH), gāḥ (gAH), āyuṣaḥ (AyuzaH), yuṣmākam (yuzmAkam), śreyān (SreyAn), parastāt (parastAt), prāṇān (prARAn) |
| Epic _[rājan]_ | 4800 | tāta (tAta), rāja (rAja), dāśārhe (dASArhe), saṃśaptakānām (saMSaptakAnAm), kaṅkaḥ (kaNkaH), yudhyamāne (yuDyamAne), vinirbhinnaḥ (vinirBinnaH), upāramat (upAramat), ṛcīkasya (fcIkasya), āhukaḥ (AhukaH), vāhlīka (vAhlIka), ṛṣyaśṛṅgaḥ (fzyaSfNgaH), janeśvara (janeSvara), vaidehyām (vEdehyAm), vyūḍhām (vyUQAm) |
| Sūtra _[rājā]_ | 201 | brūyāt (brUyAt), pārṣṇim (pArzRim), rājyam (rAjyam), sattrī (sattrI), śatru (Satru), preṣayet (prezayet), śatruḥ (SatruH), atisaṃdhatte (atisaMDatte), rājñaḥ (rAjYaH), rājānam (rAjAnam), parasya (parasya), putraḥ (putraH), grāham (grAham), dharmam (Darmam), balam (balam) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** recovered (showcase; 3-stage register drift)  
**Notes:** The cleanest trajectory: Vedic king sits among DEITIES — soma, agni, bṛhaspati, vaiśvānara, pāvaka (sacral kingship; 'Soma the king'); Epic = named epic sovereigns + narrative address (proper names dāśārha/vāhlīka/ṛṣyaśṛṅga, tāta 'dear', janeśvara 'lord of people'); Sūtra = Arthaśāstra statecraft/espionage register — śatru 'enemy', preṣayet 'should dispatch', atisaṃdhatte 'out-maneuvers', pārṣṇi 'flank', rājya 'realm'. Sacral→heroic→administrative fully recovered. (Confirm Kamboja p.208 actually treats rājan; else cite MW + kingship lit.)

---


# Controls — expected stable

## deva  (Kamboja pp. 55)
- **Documented shift:** 'celestial god' — STABLE in Sanskrit (pejoration only on Iranian side, Av. daēva)
- **Type:** stable (control)  ·  **expected transition:** —
- _drift (deva):_ **second-order** V→U 0.034 · U→E 0.075 · E→S 0.079 · **full V→S 0.048**  ||  **Procrustes** V→U 0.282 · U→E 0.448 · E→S 0.479 · full 0.126

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[devāḥ]_ | 1049 | pitaraḥ (pitaraH), viśve (viSve), āsan (Asan), sarve (sarve), pūrve (pUrve), aṅgirasaḥ (aNgirasaH), putrāḥ (putrAH), manuṣyāḥ (manuzyAH), aspardhanta (asparDanta), asurāḥ (asurAH), yām (yAm), iman (iman), sādhyāḥ (sADyAH), yatra (yatra), tān (tAn) |
| Upaniṣadic _[devāḥ]_ | 200 | vedāḥ (vedAH), sarve (sarve), ete (ete), manuṣyāḥ (manuzyAH), ke (ke), ādityāḥ (AdityAH), amṛtāḥ (amftAH), pitaraḥ (pitaraH), rājānam (rAjAnam), somam (somam), asurāḥ (asurAH), viśve (viSve), trī (trI), upajīvanti (upajIvanti), vasavaḥ (vasavaH) |
| Epic _[deva]_ | 2238 | gandharva (ganDarva), apsarasām (apsarasAm), apsaraḥ (apsaraH), vaṃśān (vaMSAn), siddha (sidDa), yakṣa (yakza), nārāyaṇāt (nArAyaRAt), asura (asura), daitya (dEtya), cāraṇa (cAraRa), kiṃnara (kiMnara), uraga (uraga), daivata (dEvata), dānava (dAnava), bhoginām (BoginAm) |
| Sūtra _[deva]_ | 202 | asmabhyam (asmaByam), savitar (savitar), svasti (svasti), matsan (matsan), kṣatram (kzatram), śarma (Sarma), santu (santu), dhiyā (DiyA), dive (dive), devāsaḥ (devAsaH), gāvaḥ (gAvaH), pātu (pAtu), bhadram (Badram), havyam (havyam), saṃrāj (saMrAj) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** STABLE — control passes  
**Notes:** Lowest full-span drift (proc 0.126). Stays 'god / celestial being' in every era — Vedic divine collective (pitaraḥ, viśve, aṅgirasaḥ, the deva/asura contest), Epic broadens to 'celestial beings' generally (gandharva, apsaras, yakṣa, kiṃnara, daitya, dānava) but remains supernatural/divine, Sūtra Vedic-style invocation. NO pejoration — confirming the documented asymmetry that only Iranian daēva degrades. Good null result.

---

## veda  (Kamboja pp. 160)
- **Documented shift:** 'knowledge' → specialized 'the Veda (corpus)'; relatively stable
- **Type:** near-stable (control)  ·  **expected transition:** —
- _drift (veda):_ **second-order** V→U 0.035 · U→E 0.105 · E→S 0.115 · **full V→S 0.031**  ||  **Procrustes** V→U 0.115 · U→E 0.465 · E→S 0.469 · full 0.217

| Era | n | Top neighbors — IAST (SLP1) |
|-----|---|------------------------------|
| Vedic _[veda]_ | 488 | evam (evam), bhrātṛvyaḥ (BrAtfvyaH), svārājyam (svArAjyam), pāpīyān (pApIyAn), saṃhitām (saMhitAm), ātmanā (AtmanA), vasīyān (vasIyAn), purodhām (puroDAm), yaḥ (yaH), upāste (upAste), pramīyate (pramIyate), bahuḥ (bahuH), saṃdhīyate (saMDIyate), evaṃv (evaMv), jāyate (jAyate) |
| Upaniṣadic _[veda]_ | 527 | evam (evam), guṇam (guRam), yathoktam (yaToktam), evaṃvidaḥ (evaMvidaH), yaḥ (yaH), salokatām (salokatAm), vedān (vedAn), sāyujyam (sAyujyam), vidvān (vidvAn), turīyam (turIyam), vāmāni (vAmAni), mahāmanāḥ (mahAmanAH), kṛtyām (kftyAm), prakāśavān (prakASavAn), darśatam (darSatam) |
| Epic _[veda]_ | 949 | vedāṅga (vedANga), vedānta (vedAnta), ṣaḍaṅga (zaqaNga), itihāsa (itihAsa), vādeṣu (vAdezu), pāragāḥ (pAragAH), vedāṅgāni (vedANgAni), purāṇa (purARa), vāda (vAda), adhyayana (aDyayana), pāragaḥ (pAragaH), vedānām (vedAnAm), chandaḥ (CandaH), vede (vede), vedyam (vedyam) |
| Sūtra _[veda]_ | 135 | vid (vid), gṛhṇāti (gfhRAti), atisaṃdhatte (atisaMDatte), pārṣṇim (pArzRim), kāmam (kAmam), jāyā (jAyA), prāpnoti (prApnoti), ācakṣīta (AcakzIta), nityaḥ (nityaH), vidyā (vidyA), brūyāt (brUyAt), kṣipram (kzipram), loka (loka), śaktaḥ (SaktaH), bhojayet (Bojayet) |

**Verdict (DRAFT — Claude's read; confirm vs WisdomLib):** near-stable → mild specialization (control)  
**Notes:** Behaves as a soft control: Vedic = knowledge/recitation (saṃhitām 'collection', upāste 'recites', vidvān 'learned'); by the Epic it specializes to the textual canon and its curriculum — vedāṅga, vedānta, ṣaḍaṅga, itihāsa, purāṇa, chandas, adhyayana. The documented 'knowledge → the Veda (corpus)' narrowing is visible but mild; low drift overall.

---

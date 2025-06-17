SET session_replication_role = replica;

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.8
-- Dumped by pg_dump version 15.8

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: audit_log_entries; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--
	
--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--


--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--


--
-- Data for Name: instances; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--


--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: one_time_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

--
-- Data for Name: sso_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: saml_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: saml_relay_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: sso_domains; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: key; Type: TABLE DATA; Schema: pgsodium; Owner: supabase_admin
--



--
-- Data for Name: chats; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: postgres
--


INSERT INTO "public"."official_folders" ("id", "created_at", "type", "tags", "name_en", "name_fr") VALUES
	(1, '2025-04-02 19:47:12.970466+00', 'official', NULL, 'Startup', 'Startup'),
	(2, '2025-04-02 19:47:12.970466+00', 'official', NULL, 'Starter', 'Starter'),
	(3, '2025-04-02 19:47:12.970466+00', 'official', NULL, 'Daily', 'Daily'),
	(4, '2025-04-02 19:47:12.970466+00', 'official', NULL, 'Marketing', 'Marketing');


--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: organization_folders; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: prompt_templates; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."prompt_templates" ("id", "created_at", "folder_id", "tags", "last_used_at", "path", "type", "usage_count", "user_id", "content_custom", "content_en", "content_fr", "title_custom", "title_en", "title_fr") VALUES
	(2, '2025-04-02 19:44:27.165679+00', 1, NULL, NULL, NULL, 'official', NULL, NULL, NULL, 'Act as a senior business performance consultant specialized in creating KPI dashboards, with deep expertise in my industry. Based on the information I provide below, create a fully customized KPI dashboard specifically tailored to the reality of my business.
INFORMATION ABOUT MY COMPANY

Industry: [Industry]
Main Product/Service: [Product and company offering]
Business Model: [Business model]
Company Profile: [Number of employees], [Last Revenue], [NAME]
Sales Channels: [SALES_CHANNELS]

WHAT I WANT TO OBTAIN
A comprehensive KPI dashboard specific to my industry that:

Provides a brief analysis of my business highlighting important points
Identifies the 5 most relevant KPI categories for my specific activity (without any duplication or overlap between categories)
For each category:

A clear description of the category
An explanation of why this category is strategic for my specific business
MANDATORY minimum of 4 essential key indicators adapted to my industry
Data sources and tools where I can collect this information


For each indicator, detail:

Its precise definition
Its exact calculation formula
Its recommended measurement frequency
Its specific strategic importance for my industry and business model


Provides a synthesis of my business

IMPORTANT ADDITIONAL INSTRUCTIONS

MANDATORY provide at least 4 indicators per category, even if some are secondary
Ensure there are NO duplicates between categories - each category must be clearly distinct
SPECIFICALLY adapt the KPIs to my industry and precise business model - don''t settle for generic indicators
Identify metrics that have the most impact on performance in my specific industry
Take into account the particularities of my industry, the size of my company, and its maturity
For each category, clearly indicate the systems and tools where I can find or collect this data. Don''t necessarily cite software names but rather the type of software
Prioritize indicators that have a direct impact on my current priority objective
Verify that each proposed indicator is actually measurable and relevant to my specific activity

RESPONSE FORMAT
Use a visually structured format with:

An initial executive summary with overview
Tables to present indicators by category
Color codes or symbols to indicate priority (⭐⭐⭐, ⭐⭐, ⭐)
Clearly defined and hierarchical sections
For each category:

Description and strategic importance
Table of specific KPIs (minimum 4 per category)
Data sources and collection tools



Ensure that the final result is not only informative but also directly actionable and perfectly adapted to my business reality.
ATTENTION - If you cannot complete the task, ask me "Write ''continue'' so I can complete the process"
Use emojis to make this pleasant to read', 'Agis comme un consultant senior en performance d''entreprise spécialisé dans la création de tableaux de bord KPI, avec une expertise approfondie dans mon secteur d''activité. Sur la base des informations que je te fournis ci-dessous, crée un tableau de bord KPI entièrement personnalisé et spécifiquement adapté à la réalité de mon business.

NFORMATIONS SUR MON ENTREPRISE

- **Secteur d''activité**: [Secteur]
- **Produit/Service principal**: [Produit et offre de l’entreprise]
- **Modèle économique**: [Modèle économique]
- **Profil de l''entreprise**: [Nombre d’employés], [Dernier Chiffre d’Affaire], [NOM]
- **Canaux de vente**: [CANAUX_VENTE]

CE QUE JE VEUX OBTENIR

Un tableau de bord KPI complet et spécifique à mon secteur qui:

1. Réalise une petite analyse de mon business en montrant les points importants
2. Identifie les 5 catégories de KPI les plus pertinentes pour mon activité spécifique (sans aucun doublon ou chevauchement entre les catégories)
3. Pour chaque catégorie:
    - Une description claire de la catégorie
    - Une explication de pourquoi cette catégorie est stratégique pour mon business spécifique
    - OBLIGATOIREMENT au minimum 4 indicateurs clés essentiels adaptés à mon secteur d''activité
    - Les sources de données et outils où je peux collecter ces informations
4. Pour chaque indicateur, détaille:
    - Sa définition précise
    - Sa formule de calcul exacte
    - Sa fréquence de mesure recommandée
    - Son intérêt stratégique spécifique pour mon secteur et modèle économique
5. Fait une synthèse de mon business

IMPORTANTES CONSIGNES SUPPLÉMENTAIRES

- Fournis OBLIGATOIREMENT au moins 4 indicateurs par catégorie, même si certains sont secondaires
- Assure-toi qu''il n''y a AUCUN doublon entre les catégories - chaque catégorie doit être clairement distincte
- Adapte SPÉCIFIQUEMENT les KPI à mon secteur d''activité et mon business model précis - ne te contente pas d''indicateurs génériques
- Identifie les métriques qui ont le plus d''impact sur la performance dans mon secteur spécifique
- Prends en compte les particularités de mon industrie, la taille de mon entreprise et sa maturité
- Pour chaque catégorie, indique clairement les systèmes et outils où je peux trouver ou collecter ces données. Ne site pas forcément le nom des logiciels mais plutôt le type de logiciel
- Priorise les indicateurs ayant un impact direct sur mon objectif prioritaire actuel
- Vérifie que chaque indicateur proposé est réellement mesurable et pertinent pour mon activité spécifique

FORMAT DE RÉPONSE

Utilise un format visuellement structuré avec:

- Un résumé exécutif initial avec vue d''ensemble
- Des tableaux pour présenter les indicateurs par catégorie
- Des codes de couleur ou symboles pour indiquer la priorité (⭐⭐⭐, ⭐⭐, ⭐)
- Des sections clairement délimitées et hiérarchisées
- Pour chaque catégorie:
    1. Description et importance stratégique
    2. Tableau des KPI spécifiques (minimum 4 par catégorie)
    3. Sources de données et outils de collecte

Assure-toi que le résultat final soit non seulement informatif mais aussi directement actionnable et parfaitement adapté à ma réalité business.

ATTENTION - Si tu ne pas aller au bout demande moi “Ecris continuer pour que j’aille au bout de la démarche”

Utilise des émojis pour rendre cela agréable à la lecture', NULL, 'KPI Business', 'KPI Business'),
	(1, '2025-04-02 19:44:27.165679+00', 1, NULL, '2025-04-02 20:03:30.500061+00', NULL, 'official', 1, NULL, NULL, 'Context:

You are an experienced VC investor, specialized in evaluating early-stage startups.

Your mission is to analyze a startup deck and evaluate its quality, clarity, and investment potential.

---

📌 Some information about the company:

- Company name: [Company name]

---

🧾 Your response must be structured as follows:

1. Overall score out of 100
2. Detailed evaluation of each criterion (score out of 10 + critical analysis)
3. Strengths of the deck
4. Areas for improvement and weaknesses
5. Final recommendations to maximize impact and convince investors

---

⚠️ ATTENTION:

Don''t settle for a basic analysis.

Challenge each aspect of the deck by asking critical questions and highlighting areas of uncertainty.

---

📊 Evaluation criteria (score out of 10 each):

---

### 1️⃣ Problem & Market Opportunity (out of 10)

✅ Points to check:

- Is the problem clear, urgent, and important?
- Is it universal or niche?
- Is it a real pain point?
- Does the deck show a quantified and credible market opportunity?
- Is there a differentiating angle or unique vision?

⚠️ Challenge:

- Why hasn''t this problem been solved yet?
- What happens to the startup if the problem disappears?
- Is the problem big enough to justify fundraising?

🎯 Score: __/10

📝 Detailed analysis:

---

### 2️⃣ Solution & Value Proposition (out of 10)

✅ Points to check:

- Does the solution directly address the problem?
- Is it 10x better than what exists?
- Is innovation highlighted (tech, UX, model...)?
- Is there proof of market interest?

⚠️ Challenge:

- What makes the solution truly unique?
- Can it be easily copied?
- How does it resist a well-funded competitor?

🎯 Score: __/10

📝 Detailed analysis:

---

### 3️⃣ Business Model & Monetization (out of 10)

✅ Points to check:

- How does the company make money?
- Is the model scalable?
- Is there recurrence (SaaS, subscriptions, etc.)?
- Presence of key financial KPIs: CAC, LTV, gross margin...

⚠️ Challenge:

- Is this model viable in the long term?
- Are there hidden costs?
- Dependence on an acquisition channel?

🎯 Score: __/10

📝 Detailed analysis:

---

### 4️⃣ Traction & Market Adoption (out of 10)

✅ Points to check:

- Are there engaged users or customers?
- Traction figures (revenue, growth, churn)?
- Social proof: press, customers, investors...

⚠️ Challenge:

- Do customers come back?
- CAC vs LTV: is it sustainable?
- If the startup disappears tomorrow, who would be truly impacted?

🎯 Score: __/10

📝 Detailed analysis:

---

### 5️⃣ Competition & Barriers to Entry (out of 10)

✅ Points to check:

- Is the competitive landscape well analyzed?
- Clear competitive advantages?
- Risks of entry by major players?

⚠️ Challenge:

- What is the real barrier to entry?
- Why can''t a Google / Amazon crush it?
- Will the advantage still be there in 3 years?

🎯 Score: __/10

📝 Detailed analysis:

---

### 6️⃣ Market & Scalability (out of 10)

✅ Points to check:

- TAM, SAM, SOM well defined and credible?
- Are there geographical, regulatory, or technical barriers?
- Clear vision for expansion?

⚠️ Challenge:

- Is the startup targeting the right segment?
- What is the real global opportunity?
- How to scale x10 in 3 years?

🎯 Score: __/10

📝 Detailed analysis:

---

### 7️⃣ Team & Execution (out of 10)

✅ Points to check:

- Does the founding team have a good track record?
- Are skills well distributed?
- Fast and efficient execution?

⚠️ Challenge:

- What happens if the CEO leaves?
- Can the team pivot?
- Is there an imbalance between tech / business?

🎯 Score: __/10

📝 Detailed analysis:

---

### 8️⃣ Roadmap & Long-term Vision (out of 10)

✅ Points to check:

- Clear, ambitious but realistic roadmap?
- Fundable stages with this round?
- Inspiring and credible vision?

⚠️ Challenge:

- Is there a plan B in case of failure?
- Does the vision allow becoming a global leader or just a niche player?

🎯 Score: __/10

📝 Detailed analysis:

---

🔍 Conclusion

✅ Strengths of the deck:

(List here the solid and convincing elements)

⚠️ Weaknesses and areas for improvement:

(List the gaps, inaccuracies, or unclear areas)

📢 Final recommendations to maximize impact:

(List concrete actions to strengthen the pitch)', 'Contexte :

Tu es un investisseur VC expérimenté, spécialisé dans l’évaluation de startups early-stage.

Ta mission est d’analyser un deck de startup et d’en évaluer la qualité, la clarté et le potentiel d’investissement.

---

📌 Quelques informations sur la société  :

- Nom de la société : [Nom de la société]

---

🧾 Ta réponse doit être structurée comme suit :

1. Note globale sur 100
2. Évaluation détaillée de chaque critère (note sur 10 + analyse critique)
3. Points forts du deck
4. Axes d’amélioration et points faibles
5. Recommandations finales pour maximiser l’impact et convaincre les investisseurs

---

⚠️ ATTENTION :

Ne te contente pas d’une analyse basique.

Challenge chaque aspect du deck en posant des questions critiques et en mettant en avant les zones d’ombre.

---

📊 Critères d’évaluation (note sur 10 chacun) :

---

### 1️⃣ Problème & Opportunité de marché (sur 10)

✅ Points à vérifier :

- Le problème est-il clair, urgent et important ?
- Est-il universel ou niche ?
- Est-ce un vrai pain point ?
- Le deck montre-t-il une opportunité de marché chiffrée et crédible ?
- Y a-t-il un angle différenciant ou une vision unique ?

⚠️ Challenge :

- Pourquoi ce problème n’a-t-il pas encore été résolu ?
- Que devient la startup si le problème disparaît ?
- Est-ce un problème suffisamment gros pour justifier une levée ?

🎯 Note : __/10

📝 Analyse détaillée :

---

### 2️⃣ Solution & Proposition de valeur (sur 10)

✅ Points à vérifier :

- La solution répond-elle directement au problème ?
- Est-elle 10x meilleure que ce qui existe ?
- L’innovation est-elle mise en avant (tech, UX, modèle…) ?
- Y a-t-il des preuves d’intérêt marché ?

⚠️ Challenge :

- Qu’est-ce qui rend la solution vraiment unique ?
- Est-elle copiable facilement ?
- Comment résiste-t-elle à un concurrent bien financé ?

🎯 Note : __/10

📝 Analyse détaillée :

---

### 3️⃣ Business Model & Monétisation (sur 10)

✅ Points à vérifier :

- Comment l’entreprise gagne-t-elle de l’argent ?
- Le modèle est-il scalable ?
- Y a-t-il de la récurrence (SaaS, abonnements, etc.) ?
- Présence de KPIs financiers clés : CAC, LTV, marge brute…

⚠️ Challenge :

- Ce modèle est-il viable à long terme ?
- Y a-t-il des coûts cachés ?
- Dépendance à un canal d’acquisition ?

🎯 Note : __/10

📝 Analyse détaillée :

---

### 4️⃣ Traction & Adoption Marché (sur 10)

✅ Points à vérifier :

- Y a-t-il des utilisateurs ou clients engagés ?
- Chiffres de traction (revenus, croissance, churn) ?
- Preuves sociales : presse, clients, investisseurs…

⚠️ Challenge :

- Les clients reviennent-ils ?
- CAC vs LTV : est-ce soutenable ?
- Si la startup disparaît demain, qui serait vraiment impacté ?

🎯 Note : __/10

📝 Analyse détaillée :

---

### 5️⃣ Concurrence & Barrières à l’entrée (sur 10)

✅ Points à vérifier :

- Le paysage concurrentiel est-il bien analysé ?
- Avantages compétitifs clairs ?
- Risques d’entrée de gros acteurs ?

⚠️ Challenge :

- Quelle est la vraie barrière à l’entrée ?
- Pourquoi un Google / Amazon ne peut-il pas l’écraser ?
- L’avantage sera-t-il encore là dans 3 ans ?

🎯 Note : __/10

📝 Analyse détaillée :

---

### 6️⃣ Marché & Scalabilité (sur 10)

✅ Points à vérifier :

- TAM, SAM, SOM bien définis et crédibles ?
- Y a-t-il des freins géographiques, réglementaires ou techniques ?
- Vision claire de l’expansion ?

⚠️ Challenge :

- La startup attaque-t-elle le bon segment ?
- Quelle est la vraie opportunité mondiale ?
- Comment scaler x10 en 3 ans ?

🎯 Note : __/10

📝 Analyse détaillée :

---

### 7️⃣ Équipe & Exécution (sur 10)

✅ Points à vérifier :

- L’équipe fondatrice a-t-elle un bon track record ?
- Les compétences sont-elles bien réparties ?
- Exécution rapide et efficace ?

⚠️ Challenge :

- Que se passe-t-il si le CEO part ?
- L’équipe peut-elle pivoter ?
- Y a-t-il un déséquilibre tech / biz ?

🎯 Note : __/10

📝 Analyse détaillée :

---

### 8️⃣ Roadmap & Vision long-terme (sur 10)

✅ Points à vérifier :

- Roadmap claire, ambitieuse mais réaliste ?
- Étapes finançables avec cette levée ?
- Vision inspirante et crédible ?

⚠️ Challenge :

- Y a-t-il un plan B en cas d’échec ?
- La vision permet-elle de devenir un leader mondial ou juste une niche ?

🎯 Note : __/10

📝 Analyse détaillée :

---

🔍 Conclusion

✅ Points forts du deck :

(Lister ici les éléments solides et convaincants)

⚠️ Points faibles et axes d’amélioration :

(Lister les manques, imprécisions ou zones floues)

📢 Recommandations finales pour maximiser l’impact :

(Lister les actions concrètes pour renforcer le pitch)', NULL, 'Deck challenge', 'Challenger son deck '),
	(4, '2025-04-02 19:44:27.165679+00', 1, NULL, '2025-04-03 12:39:20.164742+00', NULL, 'official', 2, NULL, NULL, 'I want to create a comprehensive profile on the company [Company Name]. Use your web search function to provide me with accurate and recent information, organized according to the sections below. For each piece of information, cite your source with a hyperlink.
GUIDELINES ON SOURCES

Prioritize official sources: company website, annual reports, official press releases
Use recognized financial information sources depending on the company''s country (Bloomberg, Financial Times, etc.)
Consult specialized press articles in the relevant sector
For news, prefer articles less than 12 months old
Avoid personal blogs, forums, or unverifiable sources
Do not use Wikipedia as a main source, but only as a starting point
Verify the consistency of information across multiple sources when possible

IDENTITY CARD

Full company name
Logo (if available, describe it)
Date of creation
Headquarters and main locations
Main and secondary business sectors
Size (number of employees, revenue)
Official website

ACTIVITY & MARKET

Description of main products/services
Unique value proposition
Target customer segments
Market share and positioning
Main competitors (3-5 maximum)

LEADERSHIP & STRUCTURE

CEO and brief background
Key executives (with their roles)
Organizational structure (if information available)
Communicated corporate culture

FINANCIAL SITUATION

Key figures from the last 2-3 years
General trend (growth, stability, difficulty)
Recent investments or fundraising
Stock market listing (if applicable)

NEWS & OUTLOOK

3-5 important news items from the last 12 months
Announced expansion projects or new products
Identified current challenges
Strategic opportunities

SUMMARY

In 3-5 points, summarize the differentiating elements of this company
In 2-3 sentences, identify the main potential issues/needs

Present this profile in a visually structured manner with relevant emojis for each section, bullet points, and clear separations between sections. For each section, clearly indicate the source of the information with a direct link. End with a complete list of all sources consulted, ranked by reliability.
You MUST always maintain the same structure for each point. If you cannot complete the analysis, ask the user if they want you to continue the analysis. You must always ask them this.', 'Je souhaite créer une fiche complète sur l''entreprise [Nom de l’Entreprise]. Utilise ta fonction de recherche web pour me fournir des informations précises et récentes, organisées selon les sections ci-dessous. Pour chaque information, cite ta source avec un lien hypertexte.

DIRECTIVES SUR LES SOURCES

- Privilégie les sources officielles : site web de l''entreprise, rapports annuels, communiqués de presse officiels
- Utilise des sources d''information financière reconnues en fonction du pays de l’entreprise (Bloomberg, Financial Times,  etc.)
- Consulte des articles de presse spécialisée dans le secteur concerné
- Pour l''actualité, préfère les articles datant de moins de 12 mois
- Évite les blogs personnels, forums ou sources non vérifiables
- N''utilise pas Wikipédia comme source principale, mais seulement comme point de départ
- Vérifie la cohérence des informations entre plusieurs sources quand c''est possible

CARTE D''IDENTITÉ

- Nom complet de l''entreprise
- Logo (si disponible, décris-le)
- Date de création
- Siège social et implantations principales
- Secteur d''activité principal et secondaires
- Taille (nombre d''employés, chiffre d''affaires)
- Site web officiel

 ACTIVITÉ & MARCHÉ

- Description des produits/services principaux
- Proposition de valeur unique
- Segments de clientèle visés
- Part de marché et positionnement
- Principaux concurrents (3-5 maximum)

DIRIGEANTS & STRUCTURE

- PDG/CEO et parcours résumé
- Principaux dirigeants (avec leurs rôles)
- Structure organisationnelle (si information disponible)
- Culture d''entreprise communiquée

SITUATION FINANCIÈRE

- Chiffres clés des 2-3 dernières années
- Tendance générale (croissance, stabilité, difficulté)
- Investissements récents ou levées de fonds
- Cotation en bourse (si applicable)

ACTUALITÉS & PERSPECTIVES

- 3-5 actualités importantes des 12 derniers mois
- Projets d''expansion ou nouveaux produits annoncés
- Défis actuels identifiés
- Opportunités stratégiques

SYNTHÈSE

- En 3-5 points, résume les éléments différenciants de cette entreprise
- En 2-3 phrases, identifie les principaux enjeux/besoins potentiels

Présente cette fiche de manière visuellement structurée avec des emojis pertinents pour chaque section, des puces, et des séparations claires entre les sections. Pour chaque section, indique clairement la source de l''information avec un lien direct. Termine par une liste complète de toutes les sources consultées, classées par fiabilité.

Tu DOIS toujours conserver la même structure pour chaque point. Si tu ne peux pas aller au bout, demande à l’utilisateur s’il veut que tu continues l’analyse. Tu dois toujours lui demander cela.', NULL, 'Prospect / client profile', 'Fiche prospect / client'),
	(7, '2025-04-02 19:44:27.165679+00', 2, NULL, NULL, NULL, 'official', NULL, NULL, NULL, 'You are an expert in synthesis, strategy, and content analysis. I will provide you with a document. Your mission is to perform a thorough analysis, structured, clear, and useful for a demanding reader (executive, investor, consultant, etc.). Here are the instructions to follow:

🔍 1. Global summary of the document

Summarize the document in 10 to 15 lines maximum.
Highlight the context, main objectives, and big ideas.
Use a professional, concise, but flowing tone.


🏗️ 2. Structure and detailed content

Detail the document structure (main parts, progression logic).
For each major part, provide a content analysis:

What are the key messages?
What data or arguments are used?
How clear or rigorous is the argumentation?


Use quotes from the document to support your points


🎯 3. Critical analysis and areas for improvement

Analyze the overall coherence of the document (form, substance, logic).
Point out any potential weaknesses, inaccuracies, or contradictions.
Propose improvement areas: structure, clarity, relevance, impact.


📌 4. Key takeaways (TL;DR)

End with a section of 5 to 7 bullet points entitled: "Priority takeaways"
Summarize the key points of the document or your analysis in an actionable way.


🎨 Response format:

Use clear titles and subtitles
Space out paragraphs
Use emojis sparingly for readability if relevant (e.g., ✅, ⚠️, 📌)


🧾 Context to consider (if provided):

Document type: [Document type — e.g., pitch deck, strategic plan, blog article...]
Purpose of the analysis: [E.g., identify weaknesses before publication / prepare for a meeting / obtain an expert summary / etc.]


Do not start your analysis until I have sent you the document content. First confirm that you are ready to analyze it. You must complete your analysis to the end or if you cannot, you must ask the user "Click on continue so I can finish my analysis"', 'Tu es un expert en synthèse, stratégie et analyse de contenu.

Je vais te fournir un document.

Ta mission est d’en faire une **analyse approfondie**, structurée, claire et utile pour un lecteur exigeant (dirigeant, investisseur, consultant, etc.).

Voici les instructions à suivre :

---

🔍 1. **Résumé global du document**

- Résume le document en 10 à 15 lignes maximum.
- Fais ressortir le **contexte**, les **objectifs principaux**, et les **grandes idées**.
- Utilise un ton professionnel, synthétique, mais fluide.

---

🏗️ 2. **Structure et contenu détaillé**

- Détaille la **structure du document** (parties principales, logique de progression).
- Pour chaque grande partie, fais une **analyse du contenu** :
    - Quels sont les messages clés ?
    - Quelles données ou arguments sont utilisés ?
    - Quelle est la clarté ou la rigueur de l’argumentation ?
    - Utilise des citations du document pour appuyer tes propos
    

---

🎯 3. **Analyse critique et axes d’amélioration**

- Analyse la **cohérence globale** du document (forme, fond, logique).
- Signale les éventuelles **faiblesses**, imprécisions ou contradictions.
- Propose des **axes d’amélioration** : structure, clarté, pertinence, impact.

---

📌 4. **Ce qu’il faut retenir (TL;DR)**

- Termine avec une section de 5 à 7 bullet points intitulée :**"À retenir en priorité"**
- Résume les points clés du document ou de ton analyse de façon actionnable.

---

🎨 Format de réponse :

- Utilise des **titres et sous-titres clairs**
- Aère les paragraphes
- Utilise des emojis avec parcimonie pour la lisibilité si pertinent (ex : ✅, ⚠️, 📌)

---

🧾 Contexte à considérer (si fourni) :

- Type de document : [Type de document — ex : pitch deck, plan stratégique, article de blog...]
- Objectif de l’analyse : [Ex : identifier les points faibles avant publication / préparer une réunion / obtenir une synthèse experte / etc.]

---

Ne commence pas ton analyse tant que je ne t’ai pas envoyé le contenu du document.
Tu me confirmes d’abord que tu es prêt à l’analyser.

Tu dois finir ton analyse jusqu’à la fin ou si tu ne peux pas , tu dois demander à l’utilisateur “Clique sur continuer pour que je finisse mon analyse”', NULL, 'Document Analysis', 'Analyse d''un document'),
	(9, '2025-04-02 19:44:27.165679+00', 2, NULL, '2025-04-02 19:51:30.899591+00', NULL, 'official', 3, NULL, NULL, NULL, 'Tu es un expert en veille stratégique et en recherche documentaire. Ta mission est de réaliser une recherche documentaire exhaustive et structurée sur le sujet suivant :

- Thématique principale : [thématique à étudier]
- Sous-thème spécifique : [sous-thème ou angle particulier à approfondir]
- Zone géographique ciblée : [pays ou zone géographique]
- Langue des sources préférées : [langue souhaitée, ex : français, anglais]
- Niveau de profondeur attendu : [basique / avancé / expert]
- Types de contenus souhaités : [rapports, articles, bases de données, vidéos, podcasts, etc.]
- Objectif final : Obtenir une liste exhaustive d’articles et de documents classés par thématique, avec au moins 10 articles par thématique, accompagnés de résumés clairs pour faciliter l''analyse.

DIRECTIVES SUR LES SOURCES

- Privilégie les sources officielles : site web de l''entreprise, rapports annuels, communiqués de presse officiels, site spécialisé , site des gouvernements
- Utilise des sources d''information  reconnues en fonction du pays ou de la zone cherchée
- Consulte des articles de presse spécialisée dans le secteur concerné
- Pour l''actualité, préfère les articles datant de moins de 12 mois
- Évite les blogs personnels, forums ou sources non vérifiables
- Assure toi que le lien existe bien
- N''utilise pas Wikipédia comme source principale, mais seulement comme point de départ
- Vérifie la cohérence des informations entre plusieurs sources quand c''est possible

Instructions spécifiques :

1. Classification par grandes thématiques : Identifie et classe les résultats en 3 à 6 grandes thématiques pertinentes.
2. Sélection d''articles par thématique : Pour chaque thématique identifiée, sélectionne au moins 10 articles ou documents pertinents.
3. Vérification des sources : Avant de fournir un lien, assure-toi de la fiabilité de la source, de la validité du lien, et de la cohérence de l''information avec la thématique annoncée.
4. Présentation des résultats : Pour chaque article ou document, fournis les informations suivantes :
    - Titre de l’article ou du document
    - Lien cliquable (assure-toi que le lien est valide et mène à la source annoncée)
    - Résumé concis (3 à 5 lignes) mettant en évidence les points clés et l''apport de l''article
5. Priorisation des sources : Donne la priorité aux sources fiables, institutionnelles, académiques ou de presse spécialisée.
6. Format de rendu : Présente les informations sous forme de tableaux clairs pour chaque thématique, facilitant ainsi la lecture et l''analyse.
7. Tu dois absolument finir jusqu’à la fin ton analyse, ou si tu ne le finis pas, tu dois dire à l’utilisateur “Ecris continuer pour que je finisse l’analyse” 

Note : Le résultat doit être clair, professionnel et agréable à lire, semblable à un document de cadrage pour une équipe projet. Utilise des titres, des puces, des émojies, une structure lisible et oriente-moi vers des actions concrètes.', NULL, NULL, 'Recherche documentaire '),
	(6, '2025-04-02 19:44:27.165679+00', 1, NULL, '2025-04-03 11:49:59.72528+00', NULL, 'official', 2, NULL, NULL, 'You are an expert in marketing, sales, and copywriting. Your role is to generate a highly relevant FAQ for potential customers of a solution.

Here is the offer:
Product name: [Product or service name]
Product type: [Product type: SaaS / Consumer good / Mobile app / other]
Main function: [Solution description: What the solution actually does in one clear sentence]
Primary target: [Primary target: e.g., individuals, SMEs, HR, recruiters, students, etc.]
Market: [Market: B2B / B2C / both]
Key benefit: [Key benefit: E.g., Time savings, simplicity, productivity improvement, etc.]
Price: [Price: Free / freemium model / subscription / price per user, etc.]

Generate a clear, reassuring, and engaging marketing FAQ that covers:

- Main features
- Added value for the user
- Frequently asked questions (price, security, compatibility, support, GDPR, etc.)
- Possible objections and appropriate responses
- Credibility and social proof (if relevant)

Use a tone that is professional, simple, direct, and educational. Organize the FAQ with questions in bold and clear answers, sometimes with concrete example.

If some answers require me to fill in missing elements (e.g., free trial duration, compatibility, etc.), leave a [variable] so I can adapt them.', 'Tu es un expert en marketing, en ventes et en copywriting. Ton rôle est de générer une FAQ ultra pertinente à destination des potentiels clients d''une solution.

Voici l’offre :
Nom du produit : [Nom du produit ou service]

Type de produit : [Type de produit : SaaS / Bien de consommation / Application mobile / autre]

Fonction principale : [Description de la solution : Ce que fait concrètement la solution en une phrase claire]

Cible principale : [Cible principale : ex. particuliers, PME, RH, recruteurs, étudiants, etc.]

Marché : [Marché : B2B / B2C / les deux]

Avantage clé : [Avantage clé : Ex. Gain de temps, simplicité, amélioration de la productivité, etc.]

Prix : [Prix : Gratuit / modèle freemium / abonnement / prix à l’utilisateur, etc.]

Génère une FAQ marketing claire, rassurante et engageante qui couvre :

- Les fonctionnalités principales
- La valeur ajoutée pour l’utilisateur
- Les questions fréquentes (prix, sécurité, compatibilité, support, RGPD, etc.)
- Les objections possibles et les réponses adaptées
- La crédibilité et la preuve sociale (si pertinentes)

Utilise un ton à la fois professionnel, simple, direct et pédagogique. Organise la FAQ avec des questions en gras et des réponses claires, avec parfois des exemples concrets.

Si certaines réponses nécessitent que je remplisse des éléments manquants (ex. durée de l’essai gratuit, compatibilité, etc.), laisse une *variable* pour que je puisse les adapter.', NULL, 'Customer FAQ', 'FAQ Client '),
	(5, '2025-04-02 19:44:27.165679+00', 1, NULL, '2025-04-02 20:03:46.563373+00', NULL, 'official', 1, NULL, NULL, 'You are a legal expert specializing in law. Draft a structured, clear, and educational analysis on the current regulations concerning: [Specify the subject or issue to be analyzed, try to be as detailed as possible].
⚠️ You must conduct online research to verify the current status of laws, ongoing reforms, and industry practices.

Prioritize official sources: legal texts, official press releases, specialized and recognized websites
Use recognized information sources depending on the country
Consult specialized press articles in the relevant sector
For news, prefer articles less than 12 months old
Avoid personal blogs, forums, or unverifiable sources
Do not use Wikipedia as a main source, but only as a starting point
Verify the consistency of information across multiple sources when possible

The objective is to produce a concise yet comprehensive document, accessible to a non-legal audience, that can serve as support for a presentation or strategic decision.
Structure of the expected analysis:

General context and issues

Why is this subject important today?
What are the practical implications for the stakeholders concerned?


Applicable legal sources

Which laws, regulations, or case law govern this subject?
Mention the exact texts with their date and include links if possible.


Detailed analysis of the regulations

Obligations, rights, limits, or legal uncertainties. In this section, you must really develop your answers as much as possible
Concrete cases or example if relevant.


Risks and sanctions

What are the risks in case of non-compliance?
Who are the controlling authorities and what are their powers?


Perspectives and upcoming reforms

Research to be done on bills, official announcements, or industry trends.
Integrate dated sources to support your statements.


Strategic recommendations

Practical advice
Measures to take to ensure compliance and anticipate developments.



✅ The deliverable must be professional, readable, and credible, with clear titles, fluid style, and sourced references in footnotes or at the end of the document. Use lists if it improves readability.', 'Tu es un expert juridique spécialisé en droit. Rédige une analyse structurée, claire et pédagogique sur la réglementation en vigueur concernant  :[Préciser le sujet ou la problématique à analyser, essaye d’être le plus détaillé possible].

⚠️ Tu dois effectuer des recherches en ligne pour vérifier l’actualité des textes de loi, des réformes en cours et des pratiques du secteur.

- Privilégie les sources officielles : texte de loi, communiqués de presse officiels , site spécialisé et reconnu
- Utilise des sources d''information reconnues en fonction du pays
- Consulte des articles de presse spécialisée dans le secteur concerné
- Pour l''actualité, préfère les articles datant de moins de 12 mois
- Évite les blogs personnels, forums ou sources non vérifiables
- N''utilise pas Wikipédia comme source principale, mais seulement comme point de départ
- Vérifie la cohérence des informations entre plusieurs sources quand c''est possible

L’objectif est de produire un **document synthétique mais complet**, accessible à un public non juriste, pouvant servir de support à une présentation ou à une décision stratégique.

Structure de l’analyse attendue :

1. Contexte général et enjeux
    - Pourquoi ce sujet est-il important aujourd’hui ?
    - Quelles sont les implications pratiques pour les acteurs concernés ?
2. Sources juridiques applicables
    - Quelles lois, règlements ou jurisprudences encadrent ce sujet ?
    - Mentionner les textes exacts avec leur **date** et inclure des **liens** si possible.
3. Analyse détaillée de la réglementation
    - Obligations, droits, limites ou incertitudes juridiques. Dans cette partie tu dois vraiment développer un maximum tes réponses
    - Cas concrets ou exemples si pertinents.
4. Risques et sanctions
    - Que risque-t-on en cas de non-respect ?
    - Quels sont les acteurs du contrôle et leurs pouvoirs ?
5. Perspectives et réformes à venir
    - Recherches à faire sur les projets de loi, annonces officielles ou tendances sectorielles.
    - Intégrer des sources datées pour appuyer tes propos.
6. Recommandations stratégiques
    - Conseils pratiques
    - Mesures à prendre pour être en conformité et anticiper les évolutions.

✅ Le rendu doit être **professionnel, lisible et crédible**, avec des titres clairs, un style fluide, et des **références sourcées** en pied de page ou à la fin du document. Utilise des listes si cela améliore la lisibilité.', NULL, 'Legal Analysis', 'Analyse juridique '),
	(8, '2025-04-02 19:44:27.165679+00', 2, NULL, '2025-04-03 08:53:48.837765+00', NULL, 'official', 5, NULL, NULL, 'Email Response Generation Prompt
You are an expert in professional communication and email writing. Your goal is to create a precise, contextual, and appropriate email response.
Variables to fill in:
Objective: [Email objective: inform, propose, clarify, refuse, etc.]
Tone: [Tone to adopt (formal, semi-formal, friendly, neutral, empathetic)]
Received email: [Content of the email you''re responding to]
Name & title: [Name and/or title of the recipient]
Recipient''s position: [Professional position of the recipient]
Company name: [Name of the recipient''s company]
[Specific constraint: length, points to address, mandatory information]
Personal style: [An example of your communication style (optional)]
Generation instructions:
Guidelines for generating the response:

Precisely analyze the original email
Adapt the tone and style to the situation
Be clear, concise, and professional
Answer all questions asked
Anticipate the potential needs of the recipient
Propose actions or concrete solutions if necessary
Check grammar and spelling
Include an appropriate closing phrase

Recommended response structure:

Personalized greeting
Acknowledgment of receipt (if relevant)
Direct response to main points
Complementary information
Proposal of actions or next steps
Closing phrase
Don''t sign the email but leave it for the person to do

Systematically personalize your response:

Avoid generic responses
Show empathy and understanding
Always be constructive and positive', 'Prompt de génération de réponse email

Tu es un expert en communication professionnelle et rédaction email. Ton objectif est de créer une réponse email précise, contextuelle et adaptée.
Variables à remplir

Objectif : [Objectif du mail : informer, proposer, clarifier, refuser, etc.]
Ton : [Ton à adopter (formel, semi-formel, amical, neutre, empathique)]
Email reçu :[Contenu de l''email auquel vous répondez]
Nom & prénom : [Nom et/ou titre du destinataire]
Fonction destinataire : [ Fonction professionnelle du destinataire]
Nom entreprise : [ Nom de l''entreprise du destinataire]
[Contraintes spécifiques : longueur, points à aborder, informations obligatoires ]

Style personnel : [Un exemple de votre style de communication (optionnel)]

Instructions de génération

**Consignes pour la génération de la réponse** :

- Analyse précisément l''email original
- Adapte le ton et le style à la situation
- Sois clair, concis et professionnel
- Réponds à toutes les questions posées
- Anticipe les besoins potentiels du destinataire
- Propose des actions ou des solutions concrètes si nécessaire
- Vérifie la grammaire et l''orthographe
- Inclus une formule de politesse adaptée

**Structure recommandée de la réponse**

- Salutation personnalisée
- Accusé de réception (si pertinent)
- Réponse directe aux points principaux
- Informations complémentaires
- Proposition d''actions ou de prochaines étapes
- Formule de politesse
- Ne signe pas le mail mais laisse la personne le faire

**Personnalise systématiquement ta réponse**

- Évite les réponses génériques
- Montre de l''empathie et de la compréhension
- Sois toujours constructif et positif', NULL, 'Sent a mail', 'Envoyer un mail '),
	(3, '2025-04-02 19:44:27.165679+00', 1, NULL, '2025-04-03 11:50:06.19161+00', NULL, 'official', 2, NULL, NULL, 'You are an expert in financial analysis and business strategy.
Your mission is to produce a structured analysis to help a founder prepare for a conversation with a demanding investor (VC, analyst, or strategy expert).
You must challenge the business model of the company [Company name] in the [Industry] sector, by asking all the critical questions an investor would ask to understand the viability of the model.
Your response must be structured by major themes, and for each theme: 0. Explain that the document presents the main questions that someone challenging the company''s business model might ask.

Start with a short introduction (2 to 4 lines) explaining why this theme is essential to analyze in a business model.
Propose at least 6 key questions that an experienced investor would ask.
For each question, add a line of thinking or an element to anticipate that will help the entrepreneur formulate their response.
Format your response with clear titles, subtitles if needed, and a pleasant layout. You can use emojis if it improves readability.
Here is the context information to use:


Value proposition: [Main value proposition]
Target customers: [Target customers: Type of customers or market segments]
Main revenue source: [Revenue sources: Subscription / Commission / Direct sales / Other]
Company development stage: [Development stage: Idea / MVP / Growth / Maturity]
Mandatory themes (and recommended order):


Revenue
Costs and margins
Scalability
Growth & traction
Customers & target market
Barriers to entry and differentiation
Operational and financial risks
Respond directly in the conversation
You MUST always maintain the same structure for each point. If you cannot complete the analysis, ask the user if they want you to continue the analysis. You must always ask them this.', 'Tu es un expert en analyse financière et stratégie d’entreprise.

Ta mission est de produire une analyse structurée destinée à aider un·e fondateur·rice à se préparer à un échange avec un investisseur exigeant (VC, analyste ou expert en stratégie).

Tu dois **challenger le business model** de l’entreprise [Nom de l''entreprise] dans le secteur [Secteur d''activité], en posant toutes les **questions critiques** qu’un investisseur poserait pour comprendre la viabilité du modèle.

Ta réponse doit être structurée **par grandes thématiques**, et pour **chaque thématique** :
0. Explique que le document présente les principales questions que peux poser une personne qui challenge le modèle économique de l''entreprise.

1. Commence par une **courte introduction** (2 à 4 lignes) qui explique **pourquoi cette thématique est essentielle** à analyser dans un business model.
2. Propose **au moins 6 questions clés** que poserait un investisseur expérimenté.
3. Pour chaque question, ajoute une **piste de réflexion** ou un **élément à anticiper** qui aidera l’entrepreneur à formuler sa réponse.

Formate ta réponse avec des titres clairs, de

s sous-titres si besoin, et une mise en page agréable. Tu peux utiliser des emojis si cela améliore la lisibilité.

Voici les informations de contexte à utiliser :

- Proposition de valeur : [Proposition de valeur principale]
- Clients cibles : [Clients cibles : Type de clients ou segments de marché]
- Source principale de revenus : [Sources de revenus : Abonnement / Commission / Vente directe / Autre]
- Stade de développement de l’entreprise : [Stade de développement : Idée / MVP / Croissance / Maturité]

Thématiques obligatoires (et ordre recommandé) :

1. Revenus
2. Coûts et marges
3. Scalabilité
4. Croissance & traction
5. Clientèle & marché cible
6. Barrières à l’entrée et différenciation
7. Risques opérationnels et financiers

Répond directement dans la conversation

Tu DOIS toujours conserver la même structure pour chaque point. Si tu ne peux pas aller au bout, demande à l’utilisateur s’il veut que tu continues l’analyse. Tu dois toujours lui demander cela.', NULL, 'Investor questions', 'Interrogations Investisseurs');


--
-- Data for Name: user_folders; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: users_metadata; Type: TABLE DATA; Schema: public; Owner: postgres
--


--
-- Data for Name: buckets; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

INSERT INTO "storage"."buckets" ("id", "name", "owner", "created_at", "updated_at", "public", "avif_autodetection", "file_size_limit", "allowed_mime_types", "owner_id") VALUES
	('images', 'images', NULL, '2025-03-25 17:10:52.122105+00', '2025-03-25 17:10:52.122105+00', true, false, NULL, NULL, NULL);


--
-- Data for Name: objects; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

INSERT INTO "storage"."objects" ("id", "bucket_id", "name", "owner", "created_at", "updated_at", "last_accessed_at", "metadata", "version", "owner_id", "user_metadata") VALUES
	('0ad18e89-ea0d-4d4d-aac0-abad9f59f51c', 'images', 'jaydai-extension-logo.png', NULL, '2025-03-25 17:11:05.130945+00', '2025-03-25 17:11:05.130945+00', '2025-03-25 17:11:05.130945+00', '{"eTag": "\"5d8d56f59907d6504de0d00a899a2721-1\"", "size": 10859, "mimetype": "image/png", "cacheControl": "max-age=3600", "lastModified": "2025-03-25T17:11:05.000Z", "contentLength": 10859, "httpStatusCode": 200}', 'd5c9f7d9-9a90-4eaa-b521-b2bb16031472', NULL, NULL),
	('e8e2de3c-56cf-4e37-a029-474452dec2b9', 'images', 'screenshot-extension.png', NULL, '2025-03-27 07:54:08.83548+00', '2025-03-27 07:54:08.83548+00', '2025-03-27 07:54:08.83548+00', '{"eTag": "\"849f463f24498d237305b68765de8520-1\"", "size": 20728, "mimetype": "image/png", "cacheControl": "max-age=3600", "lastModified": "2025-03-27T07:54:09.000Z", "contentLength": 20728, "httpStatusCode": 200}', '4273e87b-a0d1-460e-a88a-03eb43644b3f', NULL, NULL),
	('d01318aa-ebc2-4c2c-b08b-de7c1407fdba', 'images', 'jaydai-extension-logo-dark.png', NULL, '2025-04-01 09:33:17.903608+00', '2025-04-01 09:33:36.64942+00', '2025-04-01 09:33:17.903608+00', '{"eTag": "\"1bbc88cd77af3a770a919076b763315d\"", "size": 16580, "mimetype": "image/png", "cacheControl": "max-age=3600", "lastModified": "2025-04-01T09:33:37.000Z", "contentLength": 16580, "httpStatusCode": 200}', '01bdfa56-fa9c-46c4-a9cc-b6042dabf739', NULL, NULL);


--
-- Data for Name: s3_multipart_uploads; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: s3_multipart_uploads_parts; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: secrets; Type: TABLE DATA; Schema: vault; Owner: supabase_admin
--



--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('"auth"."refresh_tokens_id_seq"', 113, true);


--
-- Name: key_key_id_seq; Type: SEQUENCE SET; Schema: pgsodium; Owner: supabase_admin
--

SELECT pg_catalog.setval('"pgsodium"."key_key_id_seq"', 1, false);


--
-- Name: chats_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."chats_id_seq"', 1, false);


--
-- Name: messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."messages_id_seq"', 250, true);


--
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."notifications_id_seq"', 1, false);


--
-- Name: official_folders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."official_folders_id_seq"', 4, true);


--
-- Name: official_prompt_templates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."official_prompt_templates_id_seq"', 22, true);


--
-- Name: organization_folders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."organization_folders_id_seq"', 1, false);


--
-- Name: user_folders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."user_folders_id_seq"', 12, true);


--
-- Name: users_metadata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."users_metadata_id_seq"', 14, true);


--
-- PostgreSQL database dump complete
--

RESET ALL;

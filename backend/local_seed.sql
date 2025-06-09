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

INSERT INTO "public"."notifications" ("id", "created_at", "user_id", "read_at", "type", "title", "body", "metadata") VALUES
	(1, '2025-05-14 08:25:52.513827+00', 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, 'welcome_new_user', 'welcome_notification_title', 'welcome_notification_body', '{"action_url": "https://www.linkedin.com/company/104914264/admin/dashboard/", "action_type": "openLinkedIn", "action_title_key": "followOnLinkedIn"}');


--
-- Data for Name: official_folders; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."official_folders" ("id", "created_at", "type", "tags", "name_en", "name_fr") VALUES
	(1, '2025-04-02 19:47:12.970466+00', 'official', NULL, 'Startup', 'Startup'),
	(2, '2025-04-02 19:47:12.970466+00', 'official', NULL, 'Starter', 'Starter'),
	(3, '2025-04-02 19:47:12.970466+00', 'official', NULL, 'Daily', 'Daily'),
	(4, '2025-04-02 19:47:12.970466+00', 'official', NULL, 'Marketing', 'Marketing');


--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."organizations" ("id", "created_at", "name") VALUES
	('376c65b0-b333-498f-97c8-33434002b2e7', '2025-05-14 08:43:41.344188+00', 'Jaydai'),
	('0e41d031-b0b4-485f-94af-5e475331c897', '2025-05-14 08:43:57.518478+00', 'Not Jaydai');


--
-- Data for Name: organization_folders; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: prompt_blocks; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."prompt_blocks" ("id", "created_at", "company_id", "organization_id", "user_id", "type", "content", "title", "description") VALUES
	(12, '2025-05-27 18:01:57.474779+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'role', '{"en": "A Tech entrepreneur who has already successfully created and sold several companies", "fr": "Un entrepreneur dans le domaine de la Tech qui a déjà réussi à créer et à vendre plusieurs entreprises"}', '{"en": "The Entrepreneur", "fr": "L''entrepreneur"}', NULL),
	(13, '2025-05-27 18:02:33.686684+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'role', '{"en": "An experienced financial director who specializes in Business Plan analysis and knows how to set realistic objectives for a startup", "fr": "un directeur financier chevronné qui est spécialiste dans l''analyse de Business Plan et sait fixer des objectifs réalistes pour une startup"}', '{"en": "The Financial Director", "fr": "Le directeur financier"}', NULL),
	(14, '2025-05-27 18:03:14.258783+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'role', '{"en": "A consultant working for BCG specialized in business plan creation who knows how to be ambitious while staying connected to reality", "fr": "un consultant travaillant pour le BCG spécialiste dans la création de business plan qui sait faire preuve d''ambition tout en restant connecté à la réalité"}', '{"en": "The BCG Consultant", "fr": "Le consultant BCG"}', NULL),
	(15, '2025-05-27 18:03:52.845672+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'context', '{"en": "I am currently working on the Jaydai company.", "fr": "Je suis en train de travailler sur l''entreprise Jaydai."}', '{"en": "Jaydai Tech Context", "fr": "Contexte Jaydai Tech"}', NULL),
	(16, '2025-05-27 18:04:27.886877+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'context', '{"en": "I am a freelancer looking for missions", "fr": "Je suis un freelance en recherche de missions"}', '{"en": "For my freelance role", "fr": "Pour mon rôle de freelance"}', NULL),
	(18, '2025-05-27 19:29:59.150966+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'example', '{"en": "Go Paris", "fr": "Allez Paris"}', '{"en": "New Example Block", "fr": "Nouveau bloc d''exemple"}', NULL),
	(19, '2025-05-28 08:32:17.485724+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'context', '{"en": "At Jaydai, we help individuals and organizations use AI effectively and intelligently by converting real and professional use cases into prompts that are available in all AI tools (like ChatGPT, Claude, etc.).\\n\\nOur main product is a Google Chrome extension that allows users to access the best prompts for use cases that can be solved by AI in just a few clicks.\\n\\nWith Jaydai, individuals and organizations maximize the results they get from AI, even if they don''t subscribe to any paid version of these tools, because a good prompt on an average model gives better results than a basic prompt on the best models.\\n\\nWe spend hours building prompts so our clients can directly benefit from this work, and we also create unique custom prompts for our clients so they can have the best prompt engineering skills for their own use cases.\\n\\nWe allow users to create their own prompt templates to save a lot of time when working on different projects and often querying AI on the same topics.\\n\\nWe also have an online learning school where users can learn to use AI effectively through real simulations.\\n\\nIn addition to the products we have created, we offer companies training and coaching to help them teach their teams how to use AI and start their journey towards increased productivity with these tools.\\n\\nWe also offer audits and consulting to help companies start their AI transformation.", "fr": "Chez Jaydai, nous aidons les personnes et les organisations à utiliser l''IA de manière efficace et intelligente en convertissant des cas d''usage réels et professionnels en prompts qui sont disponibles dans tous les outils d''IA (comme ChatGPT, Claude, etc.).\\n\\nNotre produit principal est une extension Google Chrome qui permet aux utilisateurs d''accéder en quelques clics aux meilleurs prompts pour les cas d''usage pouvant être résolus par l''IA.\\n\\nAvec Jaydai, les particuliers et les organisations maximisent les résultats qu''ils obtiennent de l''IA, même s''ils ne souscrivent à aucune version payante de ces outils, car un bon prompt sur un modèle moyen donne de meilleurs résultats qu''un prompt basique sur les meilleurs modèles.\\n\\nNous passons des heures à construire des prompts pour que nos clients puissent bénéficier directement de ce travail, et nous créons également des prompts personnalisés uniques pour nos clients afin qu''ils puissent avoir les meilleures compétences en ingénierie de prompts pour leurs propres cas d''usage.\\n\\nNous permettons aux utilisateurs de créer leurs propres modèles de prompts pour économiser beaucoup de temps lorsqu''ils travaillent sur différents projets et interrogent souvent l''IA sur les mêmes sujets.\\n\\nNous avons également une école d''apprentissage en ligne où les utilisateurs peuvent apprendre à utiliser l''IA efficacement grâce à des simulations réelles.\\n\\nEn plus des produits que nous avons créés, nous proposons aux entreprises des formations et du coaching pour les aider à enseigner à leurs équipes comment utiliser l''IA et commencer leur parcours vers une productivité accrue avec ces outils.\\n\\nNous proposons également des audits et des conseils pour aider les entreprises à démarrer leur transformation vers l''IA."}', '{"en": "Jaydai Business Description", "fr": "Description de l''entreprise Jaydai"}', NULL),
	(20, '2025-05-28 08:36:27.081081+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'format', '{"en": "A PDF file that I can easily download with professional formatting", "fr": "Un fichier PDF que je peux facilement télécharger et avec une mise en forme professionnelle"}', '{"en": "PDF format", "fr": "format PDF"}', NULL),
	(21, '2025-05-28 08:40:24.752781+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'format', '{"en": "A JSON file that I could copy-paste and integrate directly into my code", "fr": "un fichier JSON que je pourrais copier-coller et intégrer directement dans mon code"}', '{"en": "JSON file", "fr": "fichier JSON"}', NULL),
	(22, '2025-05-28 08:41:06.677202+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'format', '{"en": "Just a simple answer to my question, without adding any comments", "fr": "juste une réponse simple à ma question, sans ajouter le moindre commentaire"}', '{"en": "Simple response", "fr": "réponse simple"}', NULL),
	(23, '2025-05-28 10:00:48.081782+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'goal', '{"en": "Fix my code", "fr": "corriger mon code"}', '{"en": "Code Correction", "fr": "Correction de code"}', NULL),
	(24, '2025-05-29 07:03:12.774817+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'role', '{"en": "test", "fr": "test"}', NULL, NULL),
	(25, '2025-05-29 08:52:02.016423+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'goal', '{"en": "Your goal is to help me improve my commercial strategy", "fr": "Ton but est de m''aider à améliorer ma stratégie commerciale"}', NULL, NULL),
	(26, '2025-05-29 09:09:16.485977+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'example', '{"en": "Go team", "fr": "allez les gard"}', '{"en": "New Block", "fr": "Nouveau bloc"}', NULL),
	(27, '2025-05-29 13:22:23.186394+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'example', '{"en": "Test new example", "fr": "Test nouvel exemple"}', NULL, NULL),
	(28, '2025-05-29 14:26:00.46478+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'example', '{"en": "Go Paris", "fr": "Allez Paris"}', '{"en": "Example Block", "fr": "Bloc d''exemple"}', NULL),
	(29, '2025-05-29 14:56:26.209461+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'tone_style', '{"en": "ok", "fr": "ok"}', '{"en": "Goal Block loool", "fr": "Bloc objectif loool"}', NULL),
	(30, '2025-05-29 14:59:27.40373+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'custom', '{"en": "huoohviouadjviofdjvioajvioajvaiodjvadiofvjdfiovjadiofvjdfiovjadfiovjafdiobnsiovnasjofn jodnvaiosfj diofvnsiovnaef nafsiovsio", "fr": "huoohviouadjviofdjvioajvioajvaiodjvadiofvjdfiovjadiofvjdfiovjadfiovjafdiobnsiovnasjofn jodnvaiosfj diofvnsiovnaef nafsiovsio"}', '{"en": "Custom Block", "fr": "Bloc personnalisé"}', NULL),
	(31, '2025-05-29 15:03:37.102499+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'context', '{"en": "Lol", "fr": "Mdr"}', '{"en": "Context Block", "fr": "Bloc de contexte"}', NULL),
	(32, '2025-05-29 15:05:29.262382+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'goal', '{"en": "okokokokokokoko", "fr": "okokokokokokoko"}', '{"en": "Goal Block test", "fr": "Bloc objectif test"}', NULL),
	(33, '2025-05-29 16:21:31.558478+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'example', '{"en": "Your objective is okokokokokokoko    Your objective is okokokokokokoko    Your tone and style: ok", "fr": "Ton objectif est okokokokokokoko    Ton objectif est okokokokokokoko    Ton ton et style : ok"}', '{"en": "Content Block", "fr": "Bloc de contenu"}', NULL),
	(34, '2025-05-29 21:19:32.281965+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'content', '{"en": "a way to chmkmkmk", "fr": "une façon de chmkmkmk"}', '{"en": "wdc;evmefkvmke;mfkm", "fr": "wdc;evmefkvmke;mfkm"}', '{"en": "mkmkmkm", "fr": "mkmkmkm"}'),
	(101, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'role', '{"en": "You are a senior software engineer with 10+ years of experience in full-stack development, specializing in React, Node.js, and cloud architecture. You write clean, maintainable code and follow best practices.", "fr": "Vous êtes un ingénieur logiciel senior avec plus de 10 ans d''expérience en développement full-stack, spécialisé en React, Node.js et architecture cloud. Vous écrivez du code propre et maintenable en suivant les meilleures pratiques."}', '{"en": "Senior Software Engineer", "fr": "Ingénieur logiciel senior"}', '{"en": "Experienced full-stack developer", "fr": "Développeur full-stack expérimenté"}'),
	(102, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'role', '{"en": "You are a management consultant working at [COMPANY_NAME] with expertise in business strategy, operational efficiency, and digital transformation. You provide data-driven insights and actionable recommendations.", "fr": "Vous êtes un consultant en management travaillant chez [COMPANY_NAME] avec une expertise en stratégie d''entreprise, efficacité opérationnelle et transformation numérique. Vous fournissez des insights basés sur les données et des recommandations actionnables."}', '{"en": "Management Consultant", "fr": "Consultant en management"}', '{"en": "Strategy and operations expert", "fr": "Expert en stratégie et opérations"}'),
	(103, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'role', '{"en": "You are a digital marketing specialist with deep knowledge of SEO, content marketing, social media strategy, and performance analytics. You create campaigns that drive measurable results.", "fr": "Vous êtes un spécialiste du marketing numérique avec une connaissance approfondie du SEO, du marketing de contenu, de la stratégie des réseaux sociaux et de l''analyse de performance. Vous créez des campagnes qui génèrent des résultats mesurables."}', '{"en": "Digital Marketing Specialist", "fr": "Spécialiste en marketing numérique"}', '{"en": "Marketing and growth expert", "fr": "Expert en marketing et croissance"}'),
	(104, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'role', '{"en": "You are a financial analyst with expertise in financial modeling, investment analysis, and risk assessment. You provide clear insights on financial performance and investment opportunities.", "fr": "Vous êtes un analyste financier avec une expertise en modélisation financière, analyse d''investissement et évaluation des risques. Vous fournissez des insights clairs sur la performance financière et les opportunités d''investissement."}', '{"en": "Financial Analyst", "fr": "Analyste financier"}', '{"en": "Finance and investment expert", "fr": "Expert en finance et investissement"}'),
	(105, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'role', '{"en": "You are an experienced project manager certified in Agile and Scrum methodologies. You excel at coordinating teams, managing timelines, and ensuring successful project delivery.", "fr": "Vous êtes un chef de projet expérimenté certifié en méthodologies Agile et Scrum. Vous excellez dans la coordination d''équipes, la gestion des délais et l''assurance d''une livraison de projet réussie."}', '{"en": "Project Manager", "fr": "Chef de projet"}', '{"en": "Agile project management expert", "fr": "Expert en gestion de projet Agile"}'),
	(201, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'context', '{"en": "I am analyzing this Excel spreadsheet that contains our company''s sales data for the past 12 months. The data includes customer information, product sales, revenue figures, and regional performance metrics.", "fr": "J''analyse cette feuille de calcul Excel qui contient les données de ventes de notre entreprise pour les 12 derniers mois. Les données incluent les informations clients, les ventes de produits, les chiffres de revenus et les métriques de performance régionale."}', '{"en": "Sales Data Analysis", "fr": "Analyse des données de ventes"}', '{"en": "Context for analyzing sales spreadsheets", "fr": "Contexte pour l''analyse des feuilles de calcul de ventes"}'),
	(202, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'context', '{"en": "I am working on a presentation for [CLIENT_NAME] that needs to be delivered next week. The presentation should cover our company''s capabilities, past successes, and proposed solution for their specific needs.", "fr": "Je travaille sur une présentation pour [CLIENT_NAME] qui doit être livrée la semaine prochaine. La présentation doit couvrir les capacités de notre entreprise, les succès passés et la solution proposée pour leurs besoins spécifiques."}', '{"en": "Client Presentation Prep", "fr": "Préparation de présentation client"}', '{"en": "Context for preparing client presentations", "fr": "Contexte pour la préparation de présentations client"}'),
	(203, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'context', '{"en": "I am conducting market research for [PRODUCT_NAME] to understand our competitive landscape, target audience preferences, and potential market opportunities in [REGION/COUNTRY].", "fr": "Je mène une étude de marché pour [PRODUCT_NAME] afin de comprendre notre paysage concurrentiel, les préférences de l''audience cible et les opportunités de marché potentielles en [REGION/COUNTRY]."}', '{"en": "Market Research Project", "fr": "Projet d''étude de marché"}', '{"en": "Context for market research activities", "fr": "Contexte pour les activités d''étude de marché"}'),
	(204, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'context', '{"en": "I am reviewing job applications for a [JOB_TITLE] position at our company. I need to evaluate candidates based on their technical skills, experience, cultural fit, and potential for growth.", "fr": "Je révise les candidatures pour un poste de [JOB_TITLE] dans notre entreprise. Je dois évaluer les candidats selon leurs compétences techniques, leur expérience, leur adéquation culturelle et leur potentiel de croissance."}', '{"en": "Recruitment Process", "fr": "Processus de recrutement"}', '{"en": "Context for hiring and recruitment", "fr": "Contexte pour l''embauche et le recrutement"}'),
	(205, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'context', '{"en": "I am preparing for a strategic planning meeting where we will discuss our company''s goals for the next fiscal year, including budget allocation, new initiatives, and performance targets.", "fr": "Je me prépare pour une réunion de planification stratégique où nous discuterons des objectifs de notre entreprise pour la prochaine année fiscale, incluant l''allocation budgétaire, les nouvelles initiatives et les objectifs de performance."}', '{"en": "Strategic Planning", "fr": "Planification stratégique"}', '{"en": "Context for strategic business planning", "fr": "Contexte pour la planification stratégique d''entreprise"}'),
	(301, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'goal', '{"en": "Help me identify key insights, trends, and actionable recommendations from this data that can improve our business performance.", "fr": "Aidez-moi à identifier les insights clés, les tendances et les recommandations actionnables de ces données qui peuvent améliorer notre performance commerciale."}', '{"en": "Data Analysis & Insights", "fr": "Analyse de données et insights"}', '{"en": "Extract insights from data", "fr": "Extraire des insights des données"}'),
	(302, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'goal', '{"en": "Create a comprehensive competitive analysis that identifies our main competitors, their strengths and weaknesses, and opportunities for our company to gain market advantage.", "fr": "Créer une analyse concurrentielle complète qui identifie nos principaux concurrents, leurs forces et faiblesses, et les opportunités pour notre entreprise de gagner un avantage marché."}', '{"en": "Competitive Analysis", "fr": "Analyse concurrentielle"}', '{"en": "Analyze competition and market position", "fr": "Analyser la concurrence et la position sur le marché"}'),
	(303, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'goal', '{"en": "Develop a detailed project plan with timelines, milestones, resource requirements, and risk mitigation strategies for successful implementation.", "fr": "Développer un plan de projet détaillé avec des délais, des jalons, des exigences de ressources et des stratégies d''atténuation des risques pour une mise en œuvre réussie."}', '{"en": "Project Planning", "fr": "Planification de projet"}', '{"en": "Create comprehensive project plans", "fr": "Créer des plans de projet complets"}'),
	(304, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'goal', '{"en": "Review and optimize this code for better performance, readability, and maintainability while following industry best practices and design patterns.", "fr": "Réviser et optimiser ce code pour une meilleure performance, lisibilité et maintenabilité tout en suivant les meilleures pratiques de l''industrie et les patterns de conception."}', '{"en": "Code Review & Optimization", "fr": "Révision et optimisation de code"}', '{"en": "Improve code quality and performance", "fr": "Améliorer la qualité et la performance du code"}'),
	(305, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'goal', '{"en": "Generate creative and engaging content ideas that align with our brand voice and will resonate with our target audience across different marketing channels.", "fr": "Générer des idées de contenu créatives et engageantes qui s''alignent avec la voix de notre marque et résonneront avec notre audience cible à travers différents canaux marketing."}', '{"en": "Content Strategy", "fr": "Stratégie de contenu"}', '{"en": "Develop content marketing strategies", "fr": "Développer des stratégies de marketing de contenu"}'),
	(401, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'output_format', '{"en": "Provide your response as a structured executive summary with: 1) Key Findings (3-5 bullet points), 2) Strategic Recommendations (numbered list), 3) Next Steps (timeline with priorities), 4) Potential Risks & Mitigation.", "fr": "Fournissez votre réponse sous forme de résumé exécutif structuré avec : 1) Conclusions clés (3-5 points), 2) Recommandations stratégiques (liste numérotée), 3) Prochaines étapes (calendrier avec priorités), 4) Risques potentiels et atténuation."}', '{"en": "Executive Summary Format", "fr": "Format de résumé exécutif"}', '{"en": "Professional executive summary structure", "fr": "Structure de résumé exécutif professionnel"}'),
	(402, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'output_format', '{"en": "Format your response as clean, well-commented code with explanations for each major section. Include variable names that are descriptive and follow naming conventions for the specified programming language.", "fr": "Formatez votre réponse sous forme de code propre et bien commenté avec des explications pour chaque section majeure. Incluez des noms de variables descriptifs qui suivent les conventions de nommage pour le langage de programmation spécifié."}', '{"en": "Clean Code Format", "fr": "Format de code propre"}', '{"en": "Well-structured code with documentation", "fr": "Code bien structuré avec documentation"}'),
	(403, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'output_format', '{"en": "Present the information as a detailed comparison table with columns for each option/competitor and rows for key criteria. Include a summary section with pros/cons and a final recommendation.", "fr": "Présentez l''information sous forme de tableau de comparaison détaillé avec des colonnes pour chaque option/concurrent et des lignes pour les critères clés. Incluez une section de résumé avec les avantages/inconvénients et une recommandation finale."}', '{"en": "Comparison Table", "fr": "Tableau de comparaison"}', '{"en": "Structured comparison format", "fr": "Format de comparaison structuré"}'),
	(404, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'output_format', '{"en": "Organize your response as a step-by-step action plan with: Phase 1 (Immediate actions - 0-30 days), Phase 2 (Short-term goals - 1-3 months), Phase 3 (Long-term objectives - 3-12 months). Include success metrics for each phase.", "fr": "Organisez votre réponse sous forme de plan d''action étape par étape avec : Phase 1 (Actions immédiates - 0-30 jours), Phase 2 (Objectifs à court terme - 1-3 mois), Phase 3 (Objectifs à long terme - 3-12 mois). Incluez des métriques de succès pour chaque phase."}', '{"en": "Action Plan Format", "fr": "Format de plan d''action"}', '{"en": "Phased implementation timeline", "fr": "Chronologie de mise en œuvre par phases"}'),
	(405, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'output_format', '{"en": "Provide the response in valid JSON format that can be easily parsed and integrated into applications. Include all relevant data with clear key-value pairs and proper nesting where appropriate.", "fr": "Fournissez la réponse au format JSON valide qui peut être facilement analysé et intégré dans les applications. Incluez toutes les données pertinentes avec des paires clé-valeur claires et un nesting approprié si nécessaire."}', '{"en": "JSON Format", "fr": "Format JSON"}', '{"en": "Machine-readable JSON output", "fr": "Sortie JSON lisible par machine"}'),
	(501, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'audience', '{"en": "The audience consists of C-level executives and senior leadership who need high-level strategic insights without getting into technical details. Focus on business impact, ROI, and strategic implications.", "fr": "L''audience se compose de dirigeants de niveau C et de cadres supérieurs qui ont besoin d''insights stratégiques de haut niveau sans entrer dans les détails techniques. Concentrez-vous sur l''impact commercial, le ROI et les implications stratégiques."}', '{"en": "Executive Leadership", "fr": "Direction exécutive"}', '{"en": "C-suite and senior management audience", "fr": "Audience direction générale et management senior"}'),
	(502, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'audience', '{"en": "The audience is technical professionals including developers, engineers, and IT specialists who understand technical concepts and appreciate detailed implementation specifics and code examples.", "fr": "L''audience est composée de professionnels techniques incluant développeurs, ingénieurs et spécialistes IT qui comprennent les concepts techniques et apprécient les spécificités détaillées d''implémentation et les exemples de code."}', '{"en": "Technical Professionals", "fr": "Professionnels techniques"}', '{"en": "Developers and technical experts", "fr": "Développeurs et experts techniques"}'),
	(503, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'audience', '{"en": "The audience consists of marketing and sales teams who need actionable insights they can implement in campaigns, customer interactions, and go-to-market strategies.", "fr": "L''audience se compose d''équipes marketing et ventes qui ont besoin d''insights actionnables qu''elles peuvent implémenter dans les campagnes, interactions client et stratégies de mise sur le marché."}', '{"en": "Marketing & Sales Teams", "fr": "Équipes marketing et ventes"}', '{"en": "Revenue-focused team members", "fr": "Membres d''équipe axés sur le chiffre d''affaires"}'),
	(504, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'audience', '{"en": "The audience includes new team members and junior professionals who need clear explanations, context, and step-by-step guidance to understand complex concepts.", "fr": "L''audience inclut de nouveaux membres d''équipe et des professionnels juniors qui ont besoin d''explications claires, de contexte et de guidage étape par étape pour comprendre les concepts complexes."}', '{"en": "Junior Team Members", "fr": "Membres d''équipe juniors"}', '{"en": "Entry-level and new professionals", "fr": "Professionnels débutants et nouveaux"}'),
	(601, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'tone_style', '{"en": "Use a professional, authoritative tone that demonstrates expertise while remaining approachable. Avoid jargon and explain complex concepts clearly. Be confident but not condescending.", "fr": "Utilisez un ton professionnel et autoritaire qui démontre l''expertise tout en restant approchable. Évitez le jargon et expliquez clairement les concepts complexes. Soyez confiant mais pas condescendant."}', '{"en": "Professional & Authoritative", "fr": "Professionnel et autoritaire"}', '{"en": "Expert but accessible communication", "fr": "Communication experte mais accessible"}'),
	(602, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'tone_style', '{"en": "Adopt a collaborative and supportive tone that encourages dialogue and partnership. Use inclusive language and acknowledge different perspectives while providing guidance.", "fr": "Adoptez un ton collaboratif et bienveillant qui encourage le dialogue et le partenariat. Utilisez un langage inclusif et reconnaissez les différentes perspectives tout en fournissant des orientations."}', '{"en": "Collaborative & Supportive", "fr": "Collaboratif et bienveillant"}', '{"en": "Team-oriented communication style", "fr": "Style de communication orienté équipe"}'),
	(603, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'tone_style', '{"en": "Communicate with urgency and focus on actionable outcomes. Be direct, concise, and results-oriented. Prioritize the most critical information and next steps.", "fr": "Communiquez avec urgence et concentrez-vous sur les résultats actionnables. Soyez direct, concis et orienté résultats. Priorisez les informations les plus critiques et les prochaines étapes."}', '{"en": "Urgent & Action-Oriented", "fr": "Urgent et orienté action"}', '{"en": "Results-focused communication", "fr": "Communication axée sur les résultats"}'),
	(604, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'tone_style', '{"en": "Use a friendly, conversational tone that makes complex topics accessible. Include relevant examples and analogies to help explain concepts in an engaging way.", "fr": "Utilisez un ton amical et conversationnel qui rend les sujets complexes accessibles. Incluez des exemples pertinents et des analogies pour aider à expliquer les concepts de manière engageante."}', '{"en": "Friendly & Conversational", "fr": "Amical et conversationnel"}', '{"en": "Approachable and engaging style", "fr": "Style approchable et engageant"}'),
	(701, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'example', '{"en": "For instance, when analyzing sales data, you might identify that ''Product A shows 23% higher conversion rates in the North region compared to South, suggesting we should reallocate marketing budget to capitalize on this geographic preference.''", "fr": "Par exemple, lors de l''analyse des données de ventes, vous pourriez identifier que ''le Produit A montre des taux de conversion 23% plus élevés dans la région Nord comparé au Sud, suggérant que nous devrions réallouer le budget marketing pour capitaliser sur cette préférence géographique.''"}', '{"en": "Sales Analysis Example", "fr": "Exemple d''analyse des ventes"}', '{"en": "Sample sales data insight", "fr": "Exemple d''insight de données de ventes"}'),
	(702, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'example', '{"en": "Example code review comment: ''Consider using async/await instead of Promise.then() for better readability. Also, extract this logic into a separate utility function to improve reusability and testing.''", "fr": "Exemple de commentaire de révision de code : ''Considérez utiliser async/await au lieu de Promise.then() pour une meilleure lisibilité. Aussi, extrayez cette logique dans une fonction utilitaire séparée pour améliorer la réutilisabilité et les tests.''"}', '{"en": "Code Review Example", "fr": "Exemple de révision de code"}', '{"en": "Sample code feedback", "fr": "Exemple de retour sur le code"}'),
	(703, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'example', '{"en": "Sample recommendation: ''Based on competitor analysis, we should focus on our superior customer service as a key differentiator, as 3 out of 5 main competitors have poor customer satisfaction scores below 3.5/5.''", "fr": "Exemple de recommandation : ''Basé sur l''analyse concurrentielle, nous devrions nous concentrer sur notre service client supérieur comme différenciateur clé, car 3 des 5 principaux concurrents ont de mauvais scores de satisfaction client en dessous de 3.5/5.''"}', '{"en": "Strategic Recommendation", "fr": "Recommandation stratégique"}', '{"en": "Business strategy example", "fr": "Exemple de stratégie d''entreprise"}'),
	(704, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'example', '{"en": "Example project milestone: ''Week 3: Complete user research interviews (15 participants), analyze findings, and create persona documentation. Deliverable: User Research Report with actionable insights.''", "fr": "Exemple de jalon de projet : ''Semaine 3 : Compléter les entretiens de recherche utilisateur (15 participants), analyser les résultats et créer la documentation des personas. Livrable : Rapport de recherche utilisateur avec insights actionnables.''"}', '{"en": "Project Milestone Example", "fr": "Exemple de jalon de projet"}', '{"en": "Sample project planning output", "fr": "Exemple de sortie de planification de projet"}'),
	(801, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'constraint', '{"en": "Keep the response concise and limit to maximum 500 words. Focus on the most critical information and avoid unnecessary details or repetition.", "fr": "Gardez la réponse concise et limitez à un maximum de 500 mots. Concentrez-vous sur les informations les plus critiques et évitez les détails inutiles ou la répétition."}', '{"en": "Word Limit Constraint", "fr": "Contrainte de limite de mots"}', '{"en": "Length limitation requirement", "fr": "Exigence de limitation de longueur"}'),
	(802, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'constraint', '{"en": "Do not include any confidential information, proprietary data, or sensitive details that should not be shared outside the organization. Keep all examples generic and anonymous.", "fr": "N''incluez aucune information confidentielle, donnée propriétaire ou détail sensible qui ne devrait pas être partagé en dehors de l''organisation. Gardez tous les exemples génériques et anonymes."}', '{"en": "Confidentiality Constraint", "fr": "Contrainte de confidentialité"}', '{"en": "Information security requirement", "fr": "Exigence de sécurité d''information"}'),
	(803, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'constraint', '{"en": "Base all recommendations on data and evidence provided. Do not make assumptions about information not explicitly stated in the context or input materials.", "fr": "Basez toutes les recommandations sur les données et preuves fournies. Ne faites pas d''hypothèses sur les informations non explicitement mentionnées dans le contexte ou les matériaux d''entrée."}', '{"en": "Data-Driven Constraint", "fr": "Contrainte basée sur les données"}', '{"en": "Evidence-based analysis only", "fr": "Analyse basée sur les preuves uniquement"}'),
	(804, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'constraint', '{"en": "Ensure all suggestions are actionable and realistic given typical business constraints such as budget limitations, timeline restrictions, and resource availability.", "fr": "Assurez-vous que toutes les suggestions sont actionnables et réalistes compte tenu des contraintes commerciales typiques telles que les limitations budgétaires, les restrictions de délais et la disponibilité des ressources."}', '{"en": "Feasibility Constraint", "fr": "Contrainte de faisibilité"}', '{"en": "Realistic implementation requirement", "fr": "Exigence d''implémentation réaliste"}'),
	(901, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'content', '{"en": "Analyze this Excel file and identify opportunities for process improvement, cost reduction, and efficiency gains. Look for patterns, anomalies, and trends that could impact business performance.", "fr": "Analysez ce fichier Excel et identifiez les opportunités d''amélioration des processus, de réduction des coûts et de gains d''efficacité. Recherchez des patterns, anomalies et tendances qui pourraient impacter la performance commerciale."}', '{"en": "Excel Analysis Request", "fr": "Demande d''analyse Excel"}', '{"en": "Spreadsheet analysis and optimization", "fr": "Analyse et optimisation de feuille de calcul"}'),
	(902, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'content', '{"en": "Research comprehensive information about [COMPANY_NAME] including their business model, recent news, financial performance, key executives, and market position. Provide insights on potential partnership or competitive opportunities.", "fr": "Recherchez des informations complètes sur [COMPANY_NAME] incluant leur modèle d''entreprise, actualités récentes, performance financière, dirigeants clés et position sur le marché. Fournissez des insights sur les opportunités potentielles de partenariat ou de concurrence."}', '{"en": "Company Research Request", "fr": "Demande de recherche d''entreprise"}', '{"en": "Comprehensive company intelligence", "fr": "Intelligence d''entreprise complète"}'),
	(903, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'content', '{"en": "Create a detailed marketing strategy for [PRODUCT_NAME] targeting [TARGET_AUDIENCE]. Include messaging positioning, channel recommendations, budget allocation, and success metrics.", "fr": "Créez une stratégie marketing détaillée pour [PRODUCT_NAME] ciblant [TARGET_AUDIENCE]. Incluez le positionnement de message, les recommandations de canaux, l''allocation budgétaire et les métriques de succès."}', '{"en": "Marketing Strategy Development", "fr": "Développement de stratégie marketing"}', '{"en": "Comprehensive marketing plan creation", "fr": "Création de plan marketing complet"}'),
	(904, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'content', '{"en": "Review this business proposal and provide feedback on its strengths, weaknesses, feasibility, and recommendations for improvement. Focus on financial projections, market analysis, and implementation timeline.", "fr": "Révisez cette proposition d''entreprise et fournissez des commentaires sur ses forces, faiblesses, faisabilité et recommandations d''amélioration. Concentrez-vous sur les projections financières, l''analyse de marché et le calendrier d''implémentation."}', '{"en": "Business Proposal Review", "fr": "Révision de proposition d''entreprise"}', '{"en": "Proposal evaluation and feedback", "fr": "Évaluation et commentaires de proposition"}'),
	(905, '2025-05-29 23:19:11.703562+00', NULL, NULL, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'content', '{"en": "Develop a comprehensive training plan for [SKILL/TOPIC] that includes learning objectives, curriculum structure, delivery methods, assessment criteria, and resource requirements.", "fr": "Développez un plan de formation complet pour [SKILL/TOPIC] qui inclut les objectifs d''apprentissage, la structure du curriculum, les méthodes de livraison, les critères d''évaluation et les exigences de ressources."}', '{"en": "Training Plan Development", "fr": "Développement de plan de formation"}', '{"en": "Educational program design", "fr": "Conception de programme éducatif"}');


--
-- Data for Name: prompt_folders; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."prompt_folders" ("id", "created_at", "user_id", "organization_id", "parent_folder_id", "title", "content", "description", "company_id", "type") VALUES
	(4, '2025-05-14 08:38:43.745616+00', 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, '{"en": "Quentin folder 1", "fr": "Dossier Quentin 1"}', '{"en": "Quentin folder 1 [test]", "fr": "Dossier Quentin 1 [test]"}', '{"en": "Quentin folder 1. DESCRIPTION", "fr": "DESCRIPTION Dossier Quentin 1"}', NULL, 'user'),
	(5, '2025-05-14 08:38:43.745616+00', 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, '{"en": "Quentin folder 2", "fr": "Dossier Quentin 2"}', '{"en": "Quentin folder 2 [test]", "fr": "Dossier Quentin 2 [test]"}', '{"en": "Quentin folder 2. DESCRIPTION", "fr": "DESCRIPTION Dossier Quentin 2"}', NULL, 'user'),
	(6, '2025-05-14 08:38:43.745616+00', NULL, '376c65b0-b333-498f-97c8-33434002b2e7', NULL, '{"en": "Jaydai folder 1", "fr": "Dossier Jaydai 1"}', '{"en": "Jaydai folder 1 [test]", "fr": "Dossier Jaydai 1 [test]"}', '{"en": "Jaydai folder 1. DESCRIPTION", "fr": "DESCRIPTION Dossier Jaydai 1"}', NULL, 'organization'),
	(7, '2025-05-14 08:38:43.745616+00', NULL, '0e41d031-b0b4-485f-94af-5e475331c897', NULL, '{"en": "NOT Jaydai folder 1", "fr": "Dossier NOT Jaydai 1"}', '{"en": "NOT Jaydai folder 1 [test]", "fr": "Dossier NOT Jaydai 1 [test]"}', '{"en": "NOT Jaydai folder 1. DESCRIPTION", "fr": "DESCRIPTION Dossier NOT Jaydai 1"}', NULL, 'organization'),
	(1, '2025-05-14 08:38:43.745616+00', NULL, NULL, NULL, '{"en": "Business", "fr": "Dossier Officiel 1"}', '{"en": "Offifial folder 1 [test]", "fr": "Dossier Officiel 1 [test]"}', '{"en": "Offifial folder 1. DESCRIPTION", "fr": "DESCRIPTION Dossier Officiel 1"}', NULL, 'official'),
	(2, '2025-05-14 08:38:43.745616+00', NULL, NULL, NULL, '{"en": "Code", "fr": "Dossier Officiel 2"}', '{"en": "Offifial folder 2 [test]", "fr": "Dossier Officiel 2 [test]"}', '{"en": "Offifial folder 2. DESCRIPTION", "fr": "DESCRIPTION Dossier Officiel 2"}', NULL, 'official'),
	(3, '2025-05-14 08:38:43.745616+00', NULL, NULL, 1, '{"en": "Marketing", "fr": "Dossier Officiel 3"}', '{"en": "Offifial folder 3 [test]", "fr": "Dossier Officiel 3 [test]"}', '{"en": "Offifial folder 3. DESCRIPTION", "fr": "DESCRIPTION Dossier Officiel 3"}', NULL, 'official'),
	(9, '2025-05-27 17:58:17.4401+00', 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, '{"en": "Levée de fonds"}', '{"en": "Business"}', '{}', NULL, 'user'),
	(10, '2025-06-02 17:24:25.775621+00', 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, '{"en": "cccc"}', '{"en": "cccc"}', '{"en": "ccccccc"}', NULL, 'user');


--
-- Data for Name: prompt_templates; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."prompt_templates" ("id", "created_at", "folder_id", "tags", "last_used_at", "path", "type", "usage_count", "user_id", "content_custom", "content_en", "content_fr", "title_custom", "title_en", "title_fr", "title", "content", "description", "blocks", "company_id", "organization_id", "metadata") VALUES
	(47, '2025-05-30 00:11:06.777238+00', NULL, '{}', NULL, NULL, 'user', 0, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, NULL, NULL, NULL, NULL, '{"en": ";lpkk"}', '{"en": "Ton rôle est de Vous êtes un spécialiste du marketing numérique avec une connaissance approfondie du SEO, du marketing de contenu, de la stratégie des réseaux sociaux et de l''analyse de performance. Vous créez des campagnes qui génèrent des résultats mesurables.\n\nLe contexte est Je mène une étude de marché pour [PRODUCT_NAME] afin de comprendre notre paysage concurrentiel, les préférences de l''audience cible et les opportunités de marché potentielles en [REGION/COUNTRY].\n\nTon objectif est Aidez-moi à identifier les insights clés, les tendances et les recommandations actionnables de ces données qui peuvent améliorer notre performance commerciale."}', '{}', '{}', NULL, NULL, '{"role": 0, "audience": 0, "main_goal": 0, "tone_style": 0, "main_context": 0, "output_format": 0, "output_language": 0}'),
	(46, '2025-05-29 14:58:43.620927+00', NULL, '{}', '2025-05-30 00:11:18.145574+00', NULL, 'user', 3, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, NULL, NULL, NULL, NULL, '{"en": "ok"}', '{"en": "Ton rôle est de un consultant  travaillant pour le BCG spécialiste dans la création de business plan qui sait faire preuve d''ambition tout en restant connecté à la réalité\n\nLe contexte est Chez Jaydai, nous aidons les personnes et les organisations à utiliser l''IA de manière efficace et intelligente en convertissant des cas d''usage réels et professionnels en prompts qui sont disponibles dans tous les outils d''IA (comme ChatGPT, Claude, etc.).\n\nNotre produit principal est une extension Google Chrome qui permet aux utilisateurs d''accéder en quelques clics aux meilleurs prompts pour les cas d''usage pouvant être résolus par l''IA.\n\nAvec Jaydai, les particuliers et les organisations maximisent les résultats qu''ils obtiennent de l''IA, même s''ils ne souscrivent à aucune version payante de ces outils, car un bon prompt sur un modèle moyen donne de meilleurs résultats qu''un prompt basique sur les meilleurs modèles.\n\nNous passons des heures à construire des prompts pour que nos clients puissent bénéficier directement de ce travail, et nous créons également des prompts personnalisés uniques pour nos clients afin qu''ils puissent avoir les meilleures compétences en ingénierie de prompts pour leurs propres cas d''usage.\n\nNous permettons aux utilisateurs de créer leurs propres modèles de prompts pour économiser beaucoup de temps lorsqu''ils travaillent sur différents projets et interrogent souvent l''IA sur les mêmes sujets.\n\nNous avons également une école d''apprentissage en ligne où les utilisateurs peuvent apprendre à utiliser l''IA efficacement grâce à des simulations réelles.\n\nEn plus des produits que nous avons créés, nous proposons aux entreprises des formations et du coaching pour les aider à enseigner à leurs équipes comment utiliser l''IA et commencer leur parcours vers une productivité accrue avec ces outils.\n\nNous proposons également des audits et des conseils pour aider les entreprises à démarrer leur transformation vers l''IA."}', '{}', '{}', NULL, NULL, '{"role": 0, "audience": 0, "main_goal": 0, "tone_style": 0, "main_context": 0, "output_format": 0, "output_language": 0}'),
	(48, '2025-06-02 11:43:47.66426+00', NULL, '{}', '2025-06-02 12:00:28.4028+00', NULL, 'user', 2, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, NULL, NULL, NULL, NULL, '{"en": "mllmlmlm"}', '{"en": "Ton rôle est de Vous êtes un consultant en management travaillant chez [COMPANY_NAME] avec une expertise en stratégie d''entreprise, efficacité opérationnelle et transformation numérique. Vous fournissez des insights basés sur les données et des recommandations actionnables."}', '{}', '{}', NULL, NULL, '{"role": 0, "audience": 0, "main_goal": 0, "tone_style": 0, "main_context": 0, "output_format": 0, "output_language": 0}'),
	(49, '2025-06-02 12:00:25.839159+00', NULL, '{}', NULL, NULL, 'user', 0, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, NULL, NULL, NULL, NULL, '{"en": "mmmmmll"}', '{"en": "Ton rôle est de Vous êtes un ingénieur logiciel senior avec plus de 10 ans d''expérience en développement full-stack, spécialisé en React, Node.js et architecture cloud. Vous écrivez du code propre et maintenable en suivant les meilleures pratiques."}', '{}', '{}', NULL, NULL, '{"role": 0, "audience": 0, "main_goal": 0, "tone_style": 0, "main_context": 0, "output_format": 0, "output_language": 0}'),
	(50, '2025-06-02 12:10:06.477245+00', NULL, '{}', '2025-06-02 12:10:09.487636+00', NULL, 'user', 1, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, NULL, NULL, NULL, NULL, '{"en": "kjk"}', '{"en": "njnjnj. []"}', '{}', '{}', NULL, NULL, '{"role": 0, "audience": 0, "main_goal": 0, "tone_style": 0, "main_context": 0, "output_format": 0, "output_language": 0}'),
	(35, '2025-05-27 18:00:45.710723+00', 9, '{}', '2025-06-02 17:04:48.337063+00', NULL, 'user', 45, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, NULL, NULL, NULL, NULL, '{"en": "Création d''un Business Plan"}', '{"en": "Ta mission est de générer un **business plan complet**, clair, cohérent et structuré à partir des éléments fournis, en respectant les meilleures pratiques du secteur.\n\n📄 Structure attendue du business plan généré :\n\nRésumé exécutif\n\n- Vision\n- Objectifs à 3-5 ans\n- Stade actuel et ambitions\n\nAnalyse du Problème\n\n- Problème(s) identifié(s)\n- Urgence, fréquence, coût actuel pour les clients\n- Pourquoi il persiste\n\nSolution proposée\n\n- Description détaillée\n- Innovations / différenciations\n- Démonstration de la valeur\n\nÉtude de marché\n\n- Taille du marché (TAM, SAM, SOM)\n- Tendances clés\n- Segmentation et focus stratégique\n\nAnalyse concurrentielle\n\n- Cartographie des concurrents\n- Forces/faiblesses relatives\n- Barrières à l’entrée construites\n\nBusiness model\n\n- Sources de revenus\n- Pricing\n- Récurrence et scalabilité\n\nGo-to-Market Strategy\n\n- Canaux d’acquisition clients\n- Positionnement\n- KPI suivis\n\nRoadmap produit & opérationnelle\n\n- Prochaines étapes clés (6-24 mois)\n- Jalons produits, clients, techniques\n\nTraction à date\n\n- Utilisateurs, clients, revenus, partenariats\n- Preuves d’adoption\n\nÉquipe & Advisory board\n\n- Rôles, complémentarité, gaps éventuels\n- Réseau et mentors\n\nPrévisions financières (3 ans)\n\n- Compte de résultat prévisionnel\n- Hypothèses clés (CAC, LTV, marge brute…)\n- Besoins de financement\n\nPlan de financement\n\n- Montant recherché\n- Usage détaillé (tech, RH, marketing…)\n- Horizon d’autonomie financière\n\n📌 ATTENTES SPÉCIALES DU MODÈLE :\n\n- Utilise un ton professionnel, clair et structuré\n- Appuie-toi sur des benchmarks crédibles lorsque des hypothèses sont nécessaires\n- Si des données sont manquantes, pose des questions ou formule plusieurs scénarios\n- Formule chaque section comme si elle devait être intégrée telle quelle dans un document officiel envoyé à des investisseurs\n- N’hésite pas à challenger la pertinence ou la viabilité de certaines parties si nécessaire\n\n🛡️ BONUS : Évaluation critique automatique (optionnelle à la fin)\n\nÀ la fin du business plan, tu peux inclure :\n\n- Une analyse SWOT\n- Une note de robustesse du plan (sur 100), évaluée selon :\n  - La clarté\n  - La cohérence stratégique\n  - La viabilité économique\n  - L’attractivité pour les investisseurs"}', '{}', '{}', NULL, NULL, '{"role": 0, "audience": 0, "main_goal": 0, "tone_style": 0, "main_context": 0, "output_format": 0, "output_language": 0}'),
	(40, '2025-05-28 14:04:35.710852+00', NULL, '{}', '2025-05-29 15:04:59.637566+00', NULL, 'user', 9, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, NULL, NULL, NULL, NULL, '{"en": "Alors la"}', '{"en": "vah [j] [sfff] pas"}', '{}', '{}', NULL, NULL, '{"role": 0, "audience": 0, "main_goal": 0, "tone_style": 0, "main_context": 0, "output_format": 0, "output_language": 0}'),
	(42, '2025-05-28 15:45:49.419407+00', NULL, '{}', '2025-05-30 00:25:37.31485+00', NULL, 'user', 2, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, NULL, NULL, NULL, NULL, '{"en": "klkoko"}', '{"en": "dedede [deede]"}', '{}', '{}', NULL, NULL, '{"role": 0, "audience": 0, "main_goal": 0, "tone_style": 0, "main_context": 0, "output_format": 0, "output_language": 0}'),
	(43, '2025-05-28 16:30:58.270724+00', NULL, '{}', '2025-05-30 00:40:47.706781+00', NULL, 'user', 1, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, NULL, NULL, NULL, NULL, '{"en": "okoko"}', '{"en": "ppl wnfw ef pefk ofk[efwef] qfam"}', '{}', '{}', NULL, NULL, '{"role": 0, "audience": 0, "main_goal": 0, "tone_style": 0, "main_context": 0, "output_format": 0, "output_language": 0}'),
	(51, '2025-06-02 17:24:41.822056+00', 10, '{}', NULL, NULL, 'user', 0, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, NULL, NULL, NULL, NULL, '{"en": "lklk"}', '{"en": "Ton rôle est de Vous êtes un ingénieur logiciel senior avec plus de 10 ans d''expérience en développement full-stack, spécialisé en React, Node.js et architecture cloud. Vous écrivez du code propre et maintenable en suivant les meilleures pratiques.\n\ndd"}', '{}', '{}', NULL, NULL, '{"role": 0, "audience": 0, "main_goal": 0, "tone_style": 0, "main_context": 0, "output_format": 0, "output_language": 0}'),
	(38, '2025-05-28 13:43:42.090199+00', NULL, '{}', '2025-05-29 08:03:59.343224+00', NULL, 'user', 2, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, NULL, NULL, NULL, NULL, '{"en": "ok"}', '{"en": "bonjour [test]\n\nWhat ? \n"}', '{}', '{}', NULL, NULL, '{"role": 0, "audience": 0, "main_goal": 0, "tone_style": 0, "main_context": 0, "output_format": 0, "output_language": 0}'),
	(39, '2025-05-28 13:43:58.757782+00', NULL, '{}', '2025-05-28 16:24:01.246399+00', NULL, 'user', 6, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, NULL, NULL, NULL, NULL, '{"en": "alors"}', '{"en": "alre [ppp]\n\njij\n"}', '{}', '{}', NULL, NULL, '{"role": 0, "audience": 0, "main_goal": 0, "tone_style": 0, "main_context": 0, "output_format": 0, "output_language": 0}'),
	(37, '2025-05-28 13:16:43.596417+00', NULL, '{}', '2025-05-29 12:54:16.74894+00', NULL, 'user', 9, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, NULL, NULL, NULL, NULL, '{"en": "test"}', '{"en": "avec un beau [caca]"}', '{}', '{}', NULL, NULL, '{"role": 0, "audience": 0, "main_goal": 0, "tone_style": 0, "main_context": 0, "output_format": 0, "output_language": 0}'),
	(41, '2025-05-28 14:06:18.579154+00', NULL, '{}', '2025-05-29 08:12:21.091924+00', NULL, 'user', 5, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, NULL, NULL, NULL, NULL, '{"en": "oo"}', '{"en": "Ton rôle est de un consultant  travaillant pour le BCG spécialiste dans la création de business plan qui sait faire preuve d''ambition tout en restant connecté à la réalité\n\nLe contexte est Chez Jaydai, nous aidons les personnes et les organisations à utiliser l''IA de manière efficace et intelligente en convertissant des cas d''usage réels et professionnels en prompts qui sont disponibles dans tous les outils d''IA (comme ChatGPT, Claude, etc.).\n\nNotre produit principal est une extension Google Chrome qui permet aux utilisateurs d''accéder en quelques clics aux meilleurs prompts pour les cas d''usage pouvant être résolus par l''IA.\n\nAvec Jaydai, les particuliers et les organisations maximisent les résultats qu''ils obtiennent de l''IA, même s''ils ne souscrivent à aucune version payante de ces outils, car un bon prompt sur un modèle moyen donne de meilleurs résultats qu''un prompt basique sur les meilleurs modèles.\n\nNous passons des heures à construire des prompts pour que nos clients puissent bénéficier directement de ce travail, et nous créons également des prompts personnalisés uniques pour nos clients afin qu''ils puissent avoir les meilleures compétences en ingénierie de prompts pour leurs propres cas d''usage.\n\nNous permettons aux utilisateurs de créer leurs propres modèles de prompts pour économiser beaucoup de temps lorsqu''ils travaillent sur différents projets et interrogent souvent l''IA sur les mêmes sujets.\n\nNous avons également une école d''apprentissage en ligne où les utilisateurs peuvent apprendre à utiliser l''IA efficacement grâce à des simulations réelles.\n\nEn plus des produits que nous avons créés, nous proposons aux entreprises des formations et du coaching pour les aider à enseigner à leurs équipes comment utiliser l''IA et commencer leur parcours vers une productivité accrue avec ces outils.\n\nNous proposons également des audits et des conseils pour aider les entreprises à démarrer leur transformation vers l''IA.\n\nTon objectif est corriger mon code\n\nL''audience ciblée est WAAAI"}', '{}', '{}', NULL, NULL, '{"role": 0, "audience": 0, "main_goal": 0, "tone_style": 0, "main_context": 0, "output_format": 0, "output_language": 0}'),
	(45, '2025-05-29 08:53:51.730442+00', NULL, '{}', '2025-05-29 08:53:56.722806+00', NULL, 'user', 1, 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', NULL, NULL, NULL, NULL, NULL, NULL, '{"en": "ale2"}', '{"en": "Ton rôle est de un consultant  travaillant pour le BCG spécialiste dans la création de business plan qui sait faire preuve d''ambition tout en restant connecté à la réalité\n\nLe contexte est Chez Jaydai, nous aidons les personnes et les organisations à utiliser l''IA de manière efficace et intelligente en convertissant des cas d''usage réels et professionnels en prompts qui sont disponibles dans tous les outils d''IA (comme ChatGPT, Claude, etc.).\n\nNotre produit principal est une extension Google Chrome qui permet aux utilisateurs d''accéder en quelques clics aux meilleurs prompts pour les cas d''usage pouvant être résolus par l''IA.\n\nAvec Jaydai, les particuliers et les organisations maximisent les résultats qu''ils obtiennent de l''IA, même s''ils ne souscrivent à aucune version payante de ces outils, car un bon prompt sur un modèle moyen donne de meilleurs résultats qu''un prompt basique sur les meilleurs modèles.\n\nNous passons des heures à construire des prompts pour que nos clients puissent bénéficier directement de ce travail, et nous créons également des prompts personnalisés uniques pour nos clients afin qu''ils puissent avoir les meilleures compétences en ingénierie de prompts pour leurs propres cas d''usage.\n\nNous permettons aux utilisateurs de créer leurs propres modèles de prompts pour économiser beaucoup de temps lorsqu''ils travaillent sur différents projets et interrogent souvent l''IA sur les mêmes sujets.\n\nNous avons également une école d''apprentissage en ligne où les utilisateurs peuvent apprendre à utiliser l''IA efficacement grâce à des simulations réelles.\n\nEn plus des produits que nous avons créés, nous proposons aux entreprises des formations et du coaching pour les aider à enseigner à leurs équipes comment utiliser l''IA et commencer leur parcours vers une productivité accrue avec ces outils.\n\nNous proposons également des audits et des conseils pour aider les entreprises à démarrer leur transformation vers l''IA.\n\nTon objectif est Ton but est de m''aider à améliorer ma stratégie commerciale\n\nEn te basant sur tes recherches sur le web, donne moi trois éléments intéressants pour Jaydai\n\nTu ne peux pas prendre de mauvauses sources\n\nTu ne peux pas non plus dire n''importe quoi"}', '{}', '{}', NULL, NULL, '{"role": 0, "audience": 0, "main_goal": 0, "tone_style": 0, "main_context": 0, "output_format": 0, "output_language": 0}');


--
-- Data for Name: user_folders; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: users_metadata; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."users_metadata" ("id", "created_at", "user_id", "name", "phone_number", "pinned_official_folder_ids", "pinned_organization_folder_ids", "preferences_metadata", "additional_email", "additional_organization", "linkedin_headline", "linkedin_id", "linkedin_profile_url", "email", "google_id", "job_type", "job_industry", "job_seniority", "interests", "signup_source", "organization_ids", "company_id") VALUES
	(15, '2025-05-14 08:25:52.488643+00', 'd8a51f48-87b3-4a79-9dab-f96c73810bd9', 'Quentin Bragard', '+33630299726', '{4,1,2,3}', '{}', NULL, 'quentin@sopatech.co', NULL, NULL, NULL, NULL, 'quentin@sopatech.co', '115073634455849698205', NULL, NULL, NULL, NULL, NULL, NULL, NULL);


--
-- Data for Name: buckets; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

INSERT INTO "storage"."buckets" ("id", "name", "owner", "created_at", "updated_at", "public", "avif_autodetection", "file_size_limit", "allowed_mime_types", "owner_id") VALUES
	('images', 'images', NULL, '2025-03-25 17:10:52.122105+00', '2025-03-25 17:10:52.122105+00', true, false, NULL, NULL, NULL);


--
-- Data for Name: objects; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

INSERT INTO "storage"."objects" ("id", "bucket_id", "name", "owner", "created_at", "updated_at", "last_accessed_at", "metadata", "version", "owner_id", "user_metadata", "level") VALUES
	('0ad18e89-ea0d-4d4d-aac0-abad9f59f51c', 'images', 'jaydai-extension-logo.png', NULL, '2025-03-25 17:11:05.130945+00', '2025-03-25 17:11:05.130945+00', '2025-03-25 17:11:05.130945+00', '{"eTag": "\"5d8d56f59907d6504de0d00a899a2721-1\"", "size": 10859, "mimetype": "image/png", "cacheControl": "max-age=3600", "lastModified": "2025-03-25T17:11:05.000Z", "contentLength": 10859, "httpStatusCode": 200}', 'd5c9f7d9-9a90-4eaa-b521-b2bb16031472', NULL, NULL, NULL),
	('e8e2de3c-56cf-4e37-a029-474452dec2b9', 'images', 'screenshot-extension.png', NULL, '2025-03-27 07:54:08.83548+00', '2025-03-27 07:54:08.83548+00', '2025-03-27 07:54:08.83548+00', '{"eTag": "\"849f463f24498d237305b68765de8520-1\"", "size": 20728, "mimetype": "image/png", "cacheControl": "max-age=3600", "lastModified": "2025-03-27T07:54:09.000Z", "contentLength": 20728, "httpStatusCode": 200}', '4273e87b-a0d1-460e-a88a-03eb43644b3f', NULL, NULL, NULL),
	('d01318aa-ebc2-4c2c-b08b-de7c1407fdba', 'images', 'jaydai-extension-logo-dark.png', NULL, '2025-04-01 09:33:17.903608+00', '2025-04-01 09:33:36.64942+00', '2025-04-01 09:33:17.903608+00', '{"eTag": "\"1bbc88cd77af3a770a919076b763315d\"", "size": 16580, "mimetype": "image/png", "cacheControl": "max-age=3600", "lastModified": "2025-04-01T09:33:37.000Z", "contentLength": 16580, "httpStatusCode": 200}', '01bdfa56-fa9c-46c4-a9cc-b6042dabf739', NULL, NULL, NULL);


--
-- Data for Name: prefixes; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: s3_multipart_uploads; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: s3_multipart_uploads_parts; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: hooks; Type: TABLE DATA; Schema: supabase_functions; Owner: supabase_functions_admin
--



--
-- Data for Name: secrets; Type: TABLE DATA; Schema: vault; Owner: supabase_admin
--



--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('"auth"."refresh_tokens_id_seq"', 826, true);


--
-- Name: key_key_id_seq; Type: SEQUENCE SET; Schema: pgsodium; Owner: supabase_admin
--

SELECT pg_catalog.setval('"pgsodium"."key_key_id_seq"', 1, false);


--
-- Name: blog_posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."blog_posts_id_seq"', 1, false);


--
-- Name: chats_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."chats_id_seq"', 276, true);


--
-- Name: landing_page_contact_form_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."landing_page_contact_form_id_seq"', 1, false);


--
-- Name: messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."messages_id_seq"', 1032, true);


--
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."notifications_id_seq"', 1, true);


--
-- Name: official_folders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."official_folders_id_seq"', 4, true);


--
-- Name: official_prompt_templates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."official_prompt_templates_id_seq"', 51, true);


--
-- Name: organization_folders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."organization_folders_id_seq"', 1, false);


--
-- Name: prompt_blocks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."prompt_blocks_id_seq"', 34, true);


--
-- Name: prompt_folders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."prompt_folders_id_seq"', 10, true);


--
-- Name: user_folders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."user_folders_id_seq"', 12, true);


--
-- Name: users_metadata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."users_metadata_id_seq"', 15, true);


--
-- Name: hooks_id_seq; Type: SEQUENCE SET; Schema: supabase_functions; Owner: supabase_functions_admin
--

SELECT pg_catalog.setval('"supabase_functions"."hooks_id_seq"', 1, false);


--
-- PostgreSQL database dump complete
--

RESET ALL;

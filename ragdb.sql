--
-- PostgreSQL database dump
--

\restrict elxprWPXpJw8HBcaCxQ8X0YxYePYs2rqnYJHlYgKSDPhAJb2SItR9ZPrCPmrCKP

-- Dumped from database version 17.6 (Debian 17.6-2.pgdg13+1)
-- Dumped by pg_dump version 17.6 (Debian 17.6-2.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.products (
    id integer NOT NULL,
    product_name text NOT NULL,
    brand text NOT NULL,
    category text,
    material text,
    fit_type text,
    sizes_available text,
    color text,
    description text,
    user_reviews text,
    washing_instructions text,
    price numeric(10,2),
    shipping_info text,
    stock_status text,
    last_modified timestamp without time zone DEFAULT now()
);


--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.products (id, product_name, brand, category, material, fit_type, sizes_available, color, description, user_reviews, washing_instructions, price, shipping_info, stock_status, last_modified) FROM stdin;
1	Veste en jean pour femme	BlueStyle	Veste	100% coton denim	Regular	S, M, L, XL	Bleu clair	Veste en jean classique avec boutons et deux poches poitrine. Légère mais durable.	• Bonne taille, confortable.\\n• Le tissu devient plus doux après le premier lavage.\\n• Couleur conforme aux photos.	Lavage en machine à froid. Séchage à l’air libre. Ne pas utiliser d’eau de javel.	59.99	Expédition sous 3-5 jours ouvrables. Retours gratuits sous 30 jours.	En stock	2025-11-15 01:34:01.889455
2	Pantalon chino slim pour homme	UrbanWear	Pantalon	98% coton, 2% élasthanne	Slim	30, 32, 34, 36	Kaki	Chino slim parfait pour le bureau ou les sorties décontractées. Tissu extensible pour plus de confort.	• Tissu de bonne qualité, agréable au toucher.\\n• La taille correspond parfaitement.\\n• Un peu serré à la taille si vous êtes entre deux tailles.	Lavage en machine à froid. Séchage en machine à basse température.	45.50	Expédition le jour suivant. Retours gratuits sous 15 jours.	En stock	2025-11-15 01:34:01.889455
3	Robe longue d’été pour femme	Elegance Co.	Robe	100% polyester, léger et respirant	Regular	S, M, L, XL	Imprimé floral bleu	Robe longue fluide avec imprimé floral, parfaite pour l’été ou les sorties à la plage.	• Très légère et agréable à porter.\\n• Longueur conforme aux photos.\\n• Taille fidèle au tableau des tailles.	Lavage à la main recommandé. Ne pas sécher en machine.	72.00	Expédition sous 2-4 jours ouvrables. Retours acceptés sous 30 jours.	En stock	2025-11-15 01:34:01.889455
4	Sweat à capuche unisexe en polaire	StreetStyle	Sweat	80% coton / 20% polyester	Regular	S, M, L, XL, XXL	Gris charbon	Sweat confortable avec poches et capuche réglable. Idéal pour un usage quotidien.	• Chaud et doux.\\n• Taille conforme.\\n• Quelques bouloches après 3 lavages.\\n• Capuche pratique avec cordon solide.	Lavage en machine à froid. Séchage en machine à basse température.	39.99	Expédition le jour suivant. Retours gratuits sous 15 jours.	Limité	2025-11-15 01:34:01.889455
5	Bottes à chevilles en cuir pour femme	FootTrend	Chaussures	Cuir véritable, semelle en caoutchouc	Regular	36, 37, 38, 39, 40	Noir	Bottes élégantes en cuir avec petit talon, parfaites pour un usage quotidien et sorties décontractées.	• Confortables dès le premier port.\\n• Taille fidèle.\\n• Légère odeur de cuir qui disparaît après une journée.\\n• Semelle robuste et adhérente.	Nettoyer avec un chiffon humide. Éviter l’immersion dans l’eau.	120.00	Expédition sous 2-5 jours ouvrables. Retours gratuits sous 30 jours.	En stock	2025-11-15 01:34:01.889455
6	product X	brand X	category X	material X	oversize	L	colorX	an oversized t-shirt for man, you should wash it on 30 degree to avoid the color fade	"• don't buy this t-shirt , the first time i washed it the color faded.\\n• amazing t-shirt, the color is perfect it's like in the pictures."	Machine wash cold. Do not exceed 30 degrees to avoid color fading.	10.00	you will get the product after 3 to 5 days after the order	In Stock	2025-12-04 11:32:58.640248
7	productY	brandY	categoryY	coton, nylon	Regular	S, M, L, XL	black	This men’s classic denim jacket combines timeless style with everyday comfort. Crafted from high-quality cotton denim, it features a regular fit that pairs easily with casual and smart outfits. Designed with a button-front closure and multiple pockets, this jacket is perfect for all seasons and adds a modern touch to any wardrobe.	• This jacket exceeded my expectations! The material feels durable and warm without being too heavy. The fit is perfect and true to size. I’ve worn it on several outings already and get compliments every time. • Absolutely love this jacket! The fit is perfect, the material feels durable, and the style goes with almost everything in my wardrobe. Definitely worth the price.	"Machine wash cold. Do not exceed 30 degrees to avoid color fading."	35.00	you will get the product after 3 to 5 days after the order	In Stock	2025-12-22 01:19:47.540592
\.


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.products_id_seq', 7, true);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict elxprWPXpJw8HBcaCxQ8X0YxYePYs2rqnYJHlYgKSDPhAJb2SItR9ZPrCPmrCKP


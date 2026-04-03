# PrzeglądAI 🤖

Landing page oraz archiwum newslettera "PrzeglądAI" – źródła wyselekcjonowanej wiedzy o sztucznej inteligencji dla branży IT i entuzjastów technologii.

## 📝 O Projekcie

**PrzeglądAI** to newsletter tworzony przez Engineering Managera, który filtruje szum informacyjny, dostarczając konkretne materiały o nowościach, praktykach, narzędziach i finansach w świecie AI.

Aplikacja pełni rolę wizytówki newslettera, umożliwiając:
- 📧 Subskrypcję (integracja z MailerLite).
- 🗄️ Dostęp do archiwum poprzednich wydań.
- 📖 Czytanie poszczególnych numerów w formie artykułów.

## 🛠 Technologie

Projekt został zbudowany w oparciu o nowoczesny stos technologiczny:

- **React 19** - Biblioteka UI.
- **TypeScript** - Bezpieczeństwo typów.
- **Tailwind CSS** - Szybkie stylowanie interfejsu.
- **React Router** - Routing po stronie klienta (SPA).
- **Lucide React** - Nowoczesne ikony.
- **Vite** - Narzędzie budowania i serwer deweloperski (domyślne dla tego typu konfiguracji).

## 🚀 Uruchomienie lokalne

1. **Instalacja zależności:**
   ```bash
   npm install
   ```

2. **Uruchomienie w trybie deweloperskim:**
   ```bash
   npm start
   # lub
   npm run dev
   ```

3. **Budowanie wersji produkcyjnej:**
   ```bash
   npm run build
   ```

## ☁️ Deployment

Projekt jest skonfigurowany do automatycznego wdrażania na **GitHub Pages** przy użyciu GitHub Actions. Plik konfiguracyjny znajduje się w `.github/workflows/pages-deploy.yml`.

## 👤 Autor

**Jakub Prądzyński**  
Engineering Manager w Allegro. Łączy świat biznesu z inżynierią oprogramowania.

- [LinkedIn](https://www.linkedin.com/in/jakubpradzynski/)
- [Strona WWW](https://jakubpradzynski.pl)

## 🤖 Jak utworzyć nowe wydanie przy pomocy AI

Proces tworzenia nowego wydania został zautomatyzowany za pomocą dedykowanych skilli AI (np. w Gemini CLI) oraz wsparcia narzędzia Antigravity do głębokiej analizy treści.

1. **Przygotuj artykuły do selekcji**
   Agent AI wyczyści linki z `data.csv`, usunie duplikaty i wygeneruje szkielet pliku `prepared_data.csv`.
2. **Uzupełnienie danych w Antigravity**
   Skopiuj treść `prepared_data.csv` i użyj promptu z pliku `generate_articles_metadata_prompt.md` w narzędziu Antigravity. Pozwoli to na dokładne zescrapowanie treści (w tym z social mediów przez przeglądarkę) i wygenerowanie opisów oraz tagów. Wynik zapisz z powrotem do `prepared_data.csv`.
3. **Uruchom selekcję artykułów**
   Zostanie uruchomiony lokalny serwer i interfejs webowy (`http://localhost:8000`). Tam wygodnie przejrzysz, odrzucisz lub edytujesz artykuły i sfinalizujesz wybór do pliku `final_prepared_data.csv`.
4. **Przygotuj wydanie bazując na artykułach**
   Agent zaproponuje tytuł, wygeneruje plik HTML nowego wydania, zaktualizuje konfigurację strony (`constants.ts`, `llms.txt`, `sitemap.xml`), przygotuje wpisy na social media i wygeneruje okładkę numeru.
5. **Ukończ tworzenie wydania**
   Agent posprząta pliki tymczasowe, stworzy nowego brancha, przygotuje commit i wygeneruje gotowy Pull Request zaplanowany do scalenia na najbliższy piątek.

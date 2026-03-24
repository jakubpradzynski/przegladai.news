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

Cały proces tworzenia nowego wydania został zautomatyzowany za pomocą dedykowanych skilli AI (np. w Gemini CLI). Wystarczy, że będąc w folderze głównym projektu użyjesz kolejno wywołań w czacie z agentem:

1. **"Przygotuj artykuły do selekcji"**
   Agent AI uruchomi pipeline czyszczący linki z `data.csv`, scrapujący treść z sieci i generujący opisy oraz tagi (zapis do `prepared_data.csv`).
2. **"Uruchom selekcję artykułów"**
   Zostanie uruchomiony lokalny serwer i interfejs webowy (`http://localhost:8000`). Tam wygodnie przejrzysz, odrzucisz lub edytujesz artykuły i sfinalizujesz wybór do pliku `final_prepared_data.csv` (postępy pracy same się zapisują).
3. **"Przygotuj wydanie bazując na artykułach"**
   Agent zaproponuje tytuł, po Twojej akceptacji wygeneruje plik HTML nowego wydania (bazując na szablonie i artykułach z CSV), zaktualizuje konfigurację strony (`constants.ts`, `llms.txt`, `sitemap.xml`), przygotuje wpisy na social media i wygeneruje poprawną okładkę najnowszego numeru za pomocą narzędzia graficznego.
4. **"Ukończ tworzenie wydania"**
   Agent wyłączy serwer, posprząta pliki tymczasowe CSV, stworzy nowego brancha, przygotuje commit, wypchnie zmiany i wygeneruje gotowy Pull Request zaplanowany do scalenia na najbliższy piątek.

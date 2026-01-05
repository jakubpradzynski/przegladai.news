import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Pobierz __dirname w środowisku ES Module
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Importuj stałe z listą postów
// Ponieważ constants.ts jest w TypeScript, a ten skrypt uruchamiamy w Node,
// najprościej będzie, jeśli tymczasowo zduplikujemy definicję lub użyjemy ts-node.
// Dla prostoty i niezawodności, odczytamy zawartość pliku constants.ts i wyciągniemy slugi regexem.

const constantsPath = path.resolve(__dirname, 'constants.ts');
const distPath = path.resolve(__dirname, 'dist');
const indexPath = path.resolve(distPath, 'index.html');

// Funkcja pomocnicza do odczytu slugów
function getSlugsFromConstants() {
  const content = fs.readFileSync(constantsPath, 'utf-8');
  // Szukamy: slug: 'tekst-tekst'
  const regex = /slug:\s*'([^']+)'/g;
  const slugs = [];
  let match;

  while ((match = regex.exec(content)) !== null) {
    slugs.push(match[1]);
  }

  return slugs;
}

async function generateStaticPaths() {
  if (!fs.existsSync(distPath)) {
    console.error('Folder dist nie istnieje. Uruchom najpierw "npm run build".');
    process.exit(1);
  }

  const slugs = getSlugsFromConstants();
  console.log(`Znaleziono ${slugs.length} slugów do wygenerowania.`);

  // Odczytaj zawartość index.html (szablonu)
  const indexContent = fs.readFileSync(indexPath, 'utf-8');

  for (const slug of slugs) {
    const dirPath = path.resolve(distPath, slug);

    // Stwórz katalog dla sluga
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath, { recursive: true });
    }

    // Skopiuj index.html do katalogu sluga
    // Dzięki temu /slug/ zadziała i zwróci 200 OK
    fs.writeFileSync(path.join(dirPath, 'index.html'), indexContent);
    console.log(`Wygenerowano: ${slug}/index.html`);
  }

  console.log('Zakończono generowanie statycznych ścieżek.');
}

generateStaticPaths();

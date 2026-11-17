# Wearden pitch: ağ versiya

## Qovluqlar
- `deck-ag/`: HyperFrames layihəsi (ağ tema). `index.html` əsas fayldır, `compositions/` içində 14 slayd, `assets/` içində şəkillər var.
- `build2.py`: bütün slaydları yaradan skript. Mətni və ya animasiyanı burada dəyişin.
- `serve-deck.mjs`: animasiyaları oynadan təqdimat səhifəsi.
- `static/`: serversiz hazır sayt (GitHub Pages və ya istənilən hostinq üçün).

## Yenidən qurmaq
```
THEME=light python3 build2.py
```

## Canlı təqdimat (lokal)
```
cd deck-ag && npx hyperframes@0.8.226 present . --no-open --port 3005
cd .. && DECK=deck-ag BG="#f7faf8" UPSTREAM=http://localhost:3005 PORT=3011 node serve-deck.mjs
```
Sonra brauzerdə http://localhost:3011 açın. İdarəetmə: Space və ya → irəli, ← geri, F tam ekran.

## Statik sayt
`static/` qovluğunu istənilən statik hostinqə yükləyin. Lokal yoxlamaq üçün:
```
cd static && python3 -m http.server 8099
```

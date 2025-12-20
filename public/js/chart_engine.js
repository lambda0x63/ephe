/**
 * ChartEngine v3.1 - Enhanced Readability High-Fidelity
 * - Slightly Larger Glyphs for clarity
 * - Distinct Typography hierarchy
 */

const CHART_CONFIG = {
    // VS-15 applied text symbols
    signSymbols: ['♈︎', '♉︎', '♊︎', '♋︎', '♌︎', '♍︎', '♎︎', '♏︎', '♐︎', '♑︎', '♒︎', '♓︎'],
    planetSymbols: {
        'Sun': '☉', 'Moon': '☾', 'Mercury': '☿', 'Venus': '♀', 'Mars': '♂',
        'Jupiter': '♃', 'Saturn': '♄',
        'Uranus': '♅', 'Neptune': '♆', 'Pluto': '♇',
        'North Node': '☊', 'South Node': '☋', 'Chiron': '⚷'
    },

    r: {
        outer: 380,
        sign_out: 380,
        sign_in: 330,  // Slightly wider ring for bigger zodiac symbols
        tick_high: 330,
        tick_low: 320,
        house_num: 305,
        planet_base: 255,
        inner: 210
    },

    center: { x: 400, y: 400 },

    colors: {
        ink: '#1a1a1a',      // Very Dark Grey (softer than #000)
        grey: '#666666',
        accent: '#9A2121',   // Deep Red (Venetian Red) for emphasis
        paper: '#F9F7F1'
    }
};

class ChartEngine {
    constructor(svgId) {
        this.svg = document.getElementById(svgId);
    }

    clear() { if (this.svg) this.svg.innerHTML = ''; }

    // Anti-Clockwise
    getPos(radius, deg) {
        const rad = deg * (Math.PI / 180);
        return {
            x: CHART_CONFIG.center.x + radius * Math.cos(rad),
            y: CHART_CONFIG.center.y - radius * Math.sin(rad)
        };
    }

    line(p1, p2, color, width, dash = "") {
        return `<line x1="${p1.x}" y1="${p1.y}" x2="${p2.x}" y2="${p2.y}" stroke="${color}" stroke-width="${width}" stroke-dasharray="${dash}" stroke-linecap="round" />`;
    }

    text(pos, content, size, color, align = "middle", weight = "normal", family = "'Playfair Display', serif") {
        return `<text x="${pos.x}" y="${pos.y}" text-anchor="${align}" dominant-baseline="central" 
                font-size="${size}" font-weight="${weight}" fill="${color}" style="font-family: ${family};">${content}</text>`;
    }

    resolveCollisions(planets) {
        let sorted = [...planets].sort((a, b) => a.position - b.position);
        for (let pass = 0; pass < 5; pass++) {
            sorted.forEach((p, i) => {
                p.level = 0;
                if (i > 0) {
                    let prev = sorted[i - 1];
                    let diff = p.position - prev.position;
                    if (diff < 0) diff += 360;

                    if (diff < 12) { // Increased distance threshold for better readability
                        p.level = (prev.level + 1) % 3;
                    }
                }
            });
        }
        return sorted;
    }

    render(data) {
        if (!data) return;
        this.clear();

        const asc = data.ascendant.position;
        let html = '';

        // 1. Background
        html += `<rect x="0" y="0" width="800" height="800" fill="${CHART_CONFIG.colors.paper}" />`;

        // 2. Rings
        [CHART_CONFIG.r.outer, CHART_CONFIG.r.sign_in, CHART_CONFIG.r.tick_low, CHART_CONFIG.r.inner].forEach(r => {
            html += `<circle cx="${CHART_CONFIG.center.x}" cy="${CHART_CONFIG.center.y}" r="${r}" fill="none" stroke="${CHART_CONFIG.colors.ink}" stroke-width="1.5" />`;
        });

        // 3. Zodiac & House Divisions
        for (let h = 0; h < 12; h++) {
            const deg = h * 30;
            const rotDeg = deg - asc + 180;

            // House Divider (Outer to Inner)
            const pIn = this.getPos(CHART_CONFIG.r.inner, rotDeg);
            const pOut = this.getPos(CHART_CONFIG.r.outer, rotDeg);
            html += this.line(pIn, pOut, CHART_CONFIG.colors.ink, 1);

            // Symbol (Larger for readability)
            const midDeg = rotDeg + 15;
            const symPos = this.getPos((CHART_CONFIG.r.sign_in + CHART_CONFIG.r.outer) / 2, midDeg);
            html += this.text(symPos, CHART_CONFIG.signSymbols[h], 32, CHART_CONFIG.colors.ink, "middle", "normal", "'Segoe UI Symbol', sans-serif");

            // House Number (Roman)
            const romanHouses = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"];
            const ascIndex = Math.floor(data.ascendant.position / 30);
            const houseIdx = (h - ascIndex + 12) % 12;
            const numPos = this.getPos(CHART_CONFIG.r.house_num, midDeg);
            html += this.text(numPos, romanHouses[houseIdx], 14, CHART_CONFIG.colors.grey, "middle", "bold");
        }

        // 4. Precision Ticks
        for (let d = 0; d < 360; d++) {
            let rStart = CHART_CONFIG.r.tick_low;
            let rEnd = CHART_CONFIG.r.sign_in;
            let width = 0.5;
            let color = CHART_CONFIG.colors.grey;
            const rotDeg = d - asc + 180;

            if (d % 10 === 0) {
                width = 1.5; color = CHART_CONFIG.colors.ink;
            } else if (d % 5 === 0) {
                rEnd -= 3; color = CHART_CONFIG.colors.ink; width = 1;
            } else {
                rEnd -= 6;
            }
            const p1 = this.getPos(rStart, rotDeg);
            const p2 = this.getPos(rEnd, rotDeg);
            html += this.line(p1, p2, color, width);
        }

        // 5. Aspects
        data.aspects.forEach(asp => {
            if (["Conjunction", "Opposition", "Trine", "Square", "Sextile"].includes(asp.type)) {
                if (asp.orb < 8) {
                    const p1 = data.planets.find(p => p.name === asp.planet1);
                    const p2 = data.planets.find(p => p.name === asp.planet2);
                    if (p1 && p2) {
                        const pos1 = this.getPos(CHART_CONFIG.r.inner, p1.position - asc + 180);
                        const pos2 = this.getPos(CHART_CONFIG.r.inner, p2.position - asc + 180);

                        let stroke = "#bbb";
                        let width = 0.8;
                        let dash = "";

                        if (asp.type === "Square" || asp.type === "Opposition") { stroke = CHART_CONFIG.colors.accent; width = 1.2; }
                        if (asp.type === "Trine") { stroke = CHART_CONFIG.colors.ink; width = 1.0; }
                        if (asp.type === "Sextile") { stroke = CHART_CONFIG.colors.ink; width = 0.6; dash = "4,4"; }

                        html += this.line(pos1, pos2, stroke, width, dash);
                    }
                }
            }
        });

        // 6. Planets (Bigger & Clearer)
        const planets = this.resolveCollisions(data.planets);
        planets.forEach(p => {
            // Spacing factor: 32px between levels
            const r = CHART_CONFIG.r.planet_base - (p.level * 32);
            const deg = p.position - asc + 180;
            const pos = this.getPos(r, deg);

            // Leader Line
            const pTick = this.getPos(CHART_CONFIG.r.tick_low, deg);
            html += this.line(pos, pTick, "#d1d5db", 0.5);

            // White Backdrop for Text
            html += `<circle cx="${pos.x}" cy="${pos.y}" r="14" fill="${CHART_CONFIG.colors.paper}" stroke="none" />`;

            const symbol = CHART_CONFIG.planetSymbols[p.name] || p.symbol;
            // Glyph - Size 24
            html += this.text(pos, symbol, 24, CHART_CONFIG.colors.ink, "middle", "normal", "'Segoe UI Symbol', sans-serif");

            // Degree - Size 11, Bold, Sans-Serif for readability
            const degPos = { x: pos.x, y: pos.y + 18 };
            html += this.text(degPos, p.degree_formatted, 11, "#333", "middle", "600", "'Inter', sans-serif");
        });

        // 7. Angles (Arrows)
        const angles = [
            { deg: asc, label: "ASC", color: CHART_CONFIG.colors.accent },
            { deg: data.midheaven.position, label: "MC", color: CHART_CONFIG.colors.accent },
            { deg: asc + 180, label: "DSC", color: CHART_CONFIG.colors.ink },
            { deg: data.midheaven.position + 180, label: "IC", color: CHART_CONFIG.colors.ink }
        ];

        angles.forEach(ang => {
            const rotDeg = ang.deg - asc + 180;
            const pOut = this.getPos(CHART_CONFIG.r.outer, rotDeg);
            const pExt = this.getPos(CHART_CONFIG.r.outer + 30, rotDeg);
            html += this.line(pOut, pExt, ang.color, 2.5);

            const pLbl = this.getPos(CHART_CONFIG.r.outer + 42, rotDeg);
            html += this.text(pLbl, ang.label, 16, ang.color, "middle", "bold");
        });

        this.svg.innerHTML = html;
        this.svg.style.background = CHART_CONFIG.colors.paper;
    }
}

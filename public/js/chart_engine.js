/**
 * ChartEngine v4.4 - Direct Interaction Framework
 * - Added mouse hovering directly on SVG planets.
 * - Dynamic aspect reveal on hover.
 */

const CHART_CONFIG = {
    signSymbols: ['♈︎', '♉︎', '♊︎', '♋︎', '♌︎', '♍︎', '♎︎', '♏︎', '♐︎', '♑︎', '♒︎', '♓︎'],
    planetSymbols: {
        'Sun': '☉', 'Moon': '☾', 'Mercury': '☿', 'Venus': '♀', 'Mars': '♂',
        'Jupiter': '♃', 'Saturn': '♄', 'Uranus': '♅', 'Neptune': '♆', 'Pluto': '♇',
        'North Node': '☊', 'South Node': '☋', 'Chiron': '⚷'
    },
    signNames: ['양', '황소', '쌍둥이', '게', '사자', '처녀', '천칭', '전갈', '사수', '염소', '물병', '물고기'],
    planetNames: {
        'Sun': '태양', 'Moon': '달', 'Mercury': '수성', 'Venus': '금성', 'Mars': '화성',
        'Jupiter': '목성', 'Saturn': '토성', 'Uranus': '천왕성', 'Neptune': '해왕성', 'Pluto': '명왕성',
        'North Node': '북노드', 'South Node': '남노드', 'Chiron': '카이론'
    },
    houseKeywords: [
        "자아/생명", "소유/가치", "소통/학습", "가정/뿌리",
        "유희/자녀", "헌신/건강", "관계/결혼", "변화/공유",
        "철학/확장", "사회/천직", "공동체/미래", "성찰/무의식"
    ],
    r: {
        outer: 380, sign_in: 330, tick_low: 320,
        house_num: 280,
        planet_base: 250,
        inner: 210
    },
    center: { x: 400, y: 400 },
    colors: { ink: '#1a1a1a', grey: '#555', accent: '#9A2121', paper: '#F9F7F1' }
};

class ChartEngine {
    constructor(svgId) {
        this.svg = document.getElementById(svgId);
        this.data = null;
        this.mode = 'symbol';
        this.activePlanet = null;
    }

    toggleMode() {
        this.mode = (this.mode === 'symbol') ? 'text' : 'symbol';
        this.render(this.data);
        return this.mode;
    }

    clear() { if (this.svg) this.svg.innerHTML = ''; }

    getPos(radius, deg) {
        const rad = (deg % 360) * (Math.PI / 180);
        return {
            x: CHART_CONFIG.center.x + radius * Math.cos(rad),
            y: CHART_CONFIG.center.y - radius * Math.sin(rad)
        };
    }

    line(p1, p2, color, width, dash = "") {
        return `<line x1="${p1.x}" y1="${p1.y}" x2="${p2.x}" y2="${p2.y}" stroke="${color}" stroke-width="${width}" stroke-dasharray="${dash}" stroke-linecap="butt" />`;
    }

    text(pos, content, size, color, align = "middle", weight = "normal", family = "'Noto Serif KR', 'Playfair Display', serif") {
        return `<text x="${pos.x}" y="${pos.y}" text-anchor="${align}" dominant-baseline="central" 
                font-size="${size}" font-weight="${weight}" fill="${color}" style="font-family: ${family}; pointer-events:none;">${content}</text>`;
    }

    highlight(planetName) {
        if (this.activePlanet === planetName) return; // No-op if same
        this.activePlanet = planetName;
        if (this.data) this.render(this.data);
    }

    render(data) {
        if (!data) return;
        this.data = data;
        this.clear();

        const asc = data.ascendant.position;
        let html = '';
        const isEdu = (this.mode === 'text');

        // Background
        html += `<rect width="800" height="800" fill="${CHART_CONFIG.colors.paper}" />`;

        // 1. Precise Ink Ticks
        for (let d = 0; d < 360; d++) {
            const rotDeg = d - asc + 180;
            let rStart = CHART_CONFIG.r.tick_low;
            let rEnd = CHART_CONFIG.r.sign_in;
            let color = CHART_CONFIG.colors.ink;
            let width = 0.5;
            if (d % 30 === 0) continue;
            if (d % 10 === 0) width = 1.2;
            else if (d % 5 === 0) { rEnd -= 4; width = 0.8; }
            else { rEnd -= 6; color = CHART_CONFIG.colors.grey; width = 0.4; }
            html += this.line(this.getPos(rStart, rotDeg), this.getPos(rEnd, rotDeg), color, width);
        }

        // 2. Aspects (Dynamic Reveal)
        data.aspects.forEach(asp => {
            if (["Conjunction", "Opposition", "Trine", "Square", "Sextile"].includes(asp.type) && asp.orb < 8) {
                const hasActive = (this.activePlanet === asp.planet1 || this.activePlanet === asp.planet2);

                // If a planet is hovered, hide all other aspects
                if (this.activePlanet && !hasActive) return;

                const p1 = data.planets.find(p => p.name === asp.planet1);
                const p2 = data.planets.find(p => p.name === asp.planet2);
                if (p1 && p2) {
                    const pos1 = this.getPos(CHART_CONFIG.r.inner, p1.position - asc + 180);
                    const pos2 = this.getPos(CHART_CONFIG.r.inner, p2.position - asc + 180);

                    // Faint if no selection, Bold if selected
                    let color = hasActive ? "#333" : "rgba(0,0,0,0.05)";
                    let width = hasActive ? 2 : 0.5;

                    if (asp.type === "Square" || asp.type === "Opposition") {
                        color = hasActive ? CHART_CONFIG.colors.accent : "rgba(139,0,0,0.05)";
                    }
                    html += this.line(pos1, pos2, color, width, asp.type === "Sextile" ? "4,4" : "");
                }
            }
        });

        // 3. Rings
        [CHART_CONFIG.r.outer, CHART_CONFIG.r.sign_in, CHART_CONFIG.r.tick_low, CHART_CONFIG.r.inner].forEach((r, i) => {
            html += `<circle cx="400" cy="400" r="${r}" fill="none" stroke="${CHART_CONFIG.colors.ink}" stroke-width="${i === 0 || i === 3 ? 2 : 1}" />`;
        });

        // 4. House & Zodiac
        for (let h = 0; h < 12; h++) {
            const rotDeg = (h * 30) - asc + 180;
            const midDeg = rotDeg + 15;
            html += this.line(this.getPos(CHART_CONFIG.r.inner, rotDeg), this.getPos(CHART_CONFIG.r.outer, rotDeg), CHART_CONFIG.colors.ink, 1.2);

            const symPos = this.getPos((CHART_CONFIG.r.sign_in + CHART_CONFIG.r.outer) / 2, midDeg);
            if (isEdu) html += this.text(symPos, CHART_CONFIG.signNames[h], 15, CHART_CONFIG.colors.ink, "middle", "700");
            else html += this.text(symPos, CHART_CONFIG.signSymbols[h], 32, CHART_CONFIG.colors.ink, "middle", "normal", "'Segoe UI Symbol'");

            const houseIdx = (h - Math.floor(asc / 30) + 12) % 12;
            const numPos = this.getPos(CHART_CONFIG.r.house_num, midDeg);
            if (isEdu) {
                html += this.text(numPos, `${houseIdx + 1}. ${CHART_CONFIG.houseKeywords[houseIdx]}`, 11, CHART_CONFIG.colors.grey, "middle", "700");
            } else {
                html += this.text(numPos, (houseIdx + 1), 13, CHART_CONFIG.colors.grey, "middle", "800", "'Inter'");
            }
        }

        // 5. Planets (Interactive!)
        const sorted = [...data.planets].sort((a, b) => a.position - b.position);
        sorted.forEach((p, i) => {
            p.level = 0;
            if (i > 0) {
                let diff = p.position - sorted[i - 1].position;
                if (diff < 0) diff += 360;
                if (diff < 15) p.level = (sorted[i - 1].level + 1) % 3;
            }
        });

        sorted.forEach(p => {
            const rotDeg = p.position - asc + 180;
            const radius = CHART_CONFIG.r.planet_base - (p.level * 36);
            const pos = this.getPos(radius, rotDeg);
            const active = this.activePlanet === p.name;
            const isRetro = p.speed < 0;

            // Planet Group with Mouse Events
            html += `<g class="planet-node" style="cursor:pointer; pointer-events:all;" 
                        onmouseenter="highlightPlanet('${p.name}')" onmouseleave="highlightPlanet(null)">`;

            html += this.line(pos, this.getPos(CHART_CONFIG.r.tick_low, rotDeg), active ? CHART_CONFIG.colors.accent : "#999", active ? 1.5 : 0.7);
            html += `<circle cx="${pos.x}" cy="${pos.y}" r="${active ? 22 : 16}" fill="${CHART_CONFIG.colors.paper}" stroke="${active ? CHART_CONFIG.colors.accent : CHART_CONFIG.colors.grey}" stroke-width="${active ? 2.5 : 0.5}" />`;

            if (isEdu) {
                const label = CHART_CONFIG.planetNames[p.name] || p.name;
                html += this.text(pos, label, 13, active ? CHART_CONFIG.colors.accent : CHART_CONFIG.colors.ink, "middle", "700");
                html += this.text({ x: pos.x, y: pos.y + 19 }, `${p.degree_formatted}${isRetro ? ' ℞' : ''}`, 9, "#333", "middle", "700", "'Inter'");
            } else {
                const sym = CHART_CONFIG.planetSymbols[p.name] || '•';
                html += this.text(pos, sym, 25, active ? CHART_CONFIG.colors.accent : CHART_CONFIG.colors.ink, "middle", "normal", "'Segoe UI Symbol'");
                html += this.text({ x: pos.x, y: pos.y + 19 }, `${p.degree_formatted}${isRetro ? ' ℞' : ''}`, 9, "#333", "middle", "700", "'Inter'");
            }
            html += `</g>`;
        });

        // 6. Angles
        const angs = [{ v: asc, l: "ASC", c: CHART_CONFIG.colors.accent }, { v: data.midheaven.position, l: "MC", c: CHART_CONFIG.colors.accent }];
        angs.forEach(a => {
            const rot = a.v - asc + 180;
            html += this.line(this.getPos(CHART_CONFIG.r.outer, rot), this.getPos(CHART_CONFIG.r.outer + 40, rot), a.c, 3.5);
            html += this.text(this.getPos(CHART_CONFIG.r.outer + 55, rot), a.l, 15, a.c, "middle", "900", "'Inter'");
        });

        this.svg.innerHTML = html;
        this.svg.style.background = CHART_CONFIG.colors.paper;
    }
}

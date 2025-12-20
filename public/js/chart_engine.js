/**
 * ChartEngine v4.7 - Perfect Symmetry & Optical Alignment
 * - Implemented Local Coordinate System for planet nodes.
 * - Added optical dy-correction for specific fonts (Symbol vs KR).
 * - Refined geometric balance for 19th-century scientific look.
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
        'Jupiter': '목성', 'Saturn': '토성', 'Uranus': '천왕', 'Neptune': '해왕', 'Pluto': '명왕',
        'North Node': '북노드', 'South Node': '남노드', 'Chiron': '카이론'
    },
    houseKeywords: [
        "신체/성격/외형", "재산/소유/생계", "형제/소통/이웃", "가정/가족/기초",
        "자녀/즐거움/창의", "질병/고난/일", "결혼/파트너/계약", "죽음/유산/숨겨진 것",
        "철학/종교/여행", "경력/명성/권위", "친구/도움/획득", "적/고통/은둔"
    ],
    r: {
        outer: 380, sign_in: 335, tick_low: 325,
        planet_base: 300,
        inner: 215,
        house_num: 175
    },
    center: { x: 400, y: 400 },
    colors: { ink: '#2D2D2D', grey: '#777', accent: '#9A2121', paper: '#F9F7F1', muted_accent: 'rgba(154, 33, 33, 0.1)' },
    elementColors: {
        fire: '#D14124',   // Fire: Deep Burnt Red/Orange
        earth: '#4E6E58',  // Earth: Sage/Olive Green
        air: '#B29412',    // Air: Ocher/Golden Yellow
        water: '#2B5A82'   // Water: Slate/Deep Blue
    },
    signElements: [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
    elementNames: ['fire', 'earth', 'air', 'water']
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

    line(p1, p2, color, width, dash = "", filter = "") {
        return `<line x1="${p1.x}" y1="${p1.y}" x2="${p2.x}" y2="${p2.y}" stroke="${color}" stroke-width="${width}" stroke-dasharray="${dash}" stroke-linecap="butt" ${filter ? `filter="url(#${filter})"` : ''} />`;
    }

    // Advanced Text Helper with dy correction
    text(pos, content, size, color, align = "middle", weight = "normal", family = "'Noto Serif KR', serif", dy = "0em") {
        return `<text x="${pos.x}" y="${pos.y}" dy="${dy}" text-anchor="${align}" dominant-baseline="central" 
                font-size="${size}" font-weight="${weight}" fill="${color}" style="font-family: ${family}; pointer-events:none;">${content}</text>`;
    }

    highlight(planetName) {
        if (this.activePlanet === planetName) return;
        this.activePlanet = planetName;
        if (this.data) this.render(this.data);
    }

    render(data) {
        if (!data) return;
        this.data = data;
        this.clear();

        const asc = data.ascendant.position;
        const isEdu = (this.mode === 'text');

        // 1. Defs & Background
        let html = `
            <defs>
                <filter id="inkBleed" x="-10%" y="-10%" width="120%" height="120%">
                    <feGaussianBlur in="SourceGraphic" stdDeviation="0.2" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
            </defs>
            <rect width="800" height="800" fill="${CHART_CONFIG.colors.paper}" />
        `;

        // 2. High-Precision Ticks
        for (let d = 0; d < 360; d++) {
            const rotDeg = d - asc + 180;
            let rEnd = CHART_CONFIG.r.sign_in;
            let weight = 0.5;
            let color = CHART_CONFIG.colors.ink;
            if (d % 30 === 0) continue;
            if (d % 10 === 0) weight = 1.3;
            else if (d % 5 === 0) { rEnd -= 4; weight = 0.8; }
            else { rEnd -= 6; weight = 0.4; color = CHART_CONFIG.colors.grey; }
            html += this.line(this.getPos(CHART_CONFIG.r.tick_low, rotDeg), this.getPos(rEnd, rotDeg), color, weight);
        }

        // 3. Aspects (Interactive)
        data.aspects.forEach(asp => {
            if (["Conjunction", "Opposition", "Trine", "Square", "Sextile"].includes(asp.type) && asp.orb < 8) {
                const hasActive = (this.activePlanet === asp.planet1 || this.activePlanet === asp.planet2);
                if (this.activePlanet && !hasActive) return;
                const p1 = data.planets.find(p => p.name === asp.planet1);
                const p2 = data.planets.find(p => p.name === asp.planet2);
                if (p1 && p2) {
                    const pos1 = this.getPos(CHART_CONFIG.r.inner, p1.position - asc + 180);
                    const pos2 = this.getPos(CHART_CONFIG.r.inner, p2.position - asc + 180);
                    let color = hasActive ? "#333" : "rgba(0,0,0,0.03)";
                    let width = hasActive ? 1.8 : 0.4;
                    if (asp.type === "Square" || asp.type === "Opposition") color = hasActive ? CHART_CONFIG.colors.accent : "rgba(154,33,33,0.03)";
                    html += this.line(pos1, pos2, color, width, asp.type === "Sextile" ? "5,5" : "");
                }
            }
        });

        // 4. Rings
        html += `<circle cx="400" cy="400" r="${CHART_CONFIG.r.outer}" fill="none" stroke="${CHART_CONFIG.colors.ink}" stroke-width="2.2" />`;
        [CHART_CONFIG.r.sign_in, CHART_CONFIG.r.tick_low, CHART_CONFIG.r.inner].forEach((r, i) => {
            html += `<circle cx="400" cy="400" r="${r}" fill="none" stroke="${CHART_CONFIG.colors.ink}" stroke-width="${i === 2 ? 1.8 : 0.8}" />`;
        });

        // 5. House & Zodiac
        for (let h = 0; h < 12; h++) {
            const rotDeg = (h * 30) - asc + 180;
            const midDeg = rotDeg + 15;
            html += this.line(this.getPos(CHART_CONFIG.r.inner, rotDeg), this.getPos(CHART_CONFIG.r.outer, rotDeg), CHART_CONFIG.colors.ink, 1.2, "", "inkBleed");

            const symPos = this.getPos((CHART_CONFIG.r.sign_in + CHART_CONFIG.r.outer) / 2, midDeg);
            const elementType = CHART_CONFIG.elementNames[CHART_CONFIG.signElements[h]];
            const elementColor = CHART_CONFIG.elementColors[elementType];

            if (isEdu) {
                html += this.text(symPos, CHART_CONFIG.signNames[h], 14, elementColor, "middle", "700");
            } else {
                // Optical centering for symbols with element colors
                html += this.text(symPos, CHART_CONFIG.signSymbols[h], 30, elementColor, "middle", "normal", "'Segoe UI Symbol'", "0.05em");
            }

            const houseIdx = (h - Math.floor(asc / 30) + 12) % 12;
            const numPos = this.getPos(CHART_CONFIG.r.house_num, midDeg);

            if (isEdu) {
                // Stack Number and Keyword vertically to save horizontal space
                html += this.text(numPos, houseIdx + 1, 12, CHART_CONFIG.colors.grey, "middle", "900", "'Playfair Display'", "-0.6em");
                html += this.text(numPos, CHART_CONFIG.houseKeywords[houseIdx], 8, "#666", "middle", "700", "'Noto Serif KR'", "0.8em");
            } else {
                html += this.text(numPos, houseIdx + 1, 13, CHART_CONFIG.colors.grey, "middle", "700", "'Playfair Display'");
            }
        }

        // 6. Planets (Perfectly Centered via Groups)
        const sorted = [...data.planets].sort((a, b) => a.position - b.position);
        sorted.forEach((p, i) => {
            p.level = 0;
            if (i > 0) {
                let diff = p.position - sorted[i - 1].position;
                if (diff < 0) diff += 360;
                if (diff < 15) p.level = (sorted[i - 1].level + 1) % 4;
            }
        });

        sorted.forEach(p => {
            const rotDeg = p.position - asc + 180;
            const radius = CHART_CONFIG.r.planet_base - (p.level * 38);
            const pos = this.getPos(radius, rotDeg);
            const active = this.activePlanet === p.name;
            const isRetro = p.speed < 0;

            // Start Group at precise point for geometric symmetry
            html += `<g transform="translate(${pos.x}, ${pos.y})" style="cursor:pointer; pointer-events:all;" 
                        onmouseenter="highlightPlanet('${p.name}')" onmouseleave="highlightPlanet(null)">`;

            // Interaction Ray (locally from -radius to 0)
            if (active) {
                const diffR = radius - CHART_CONFIG.r.inner;
                html += `<line x1="${-diffR * Math.cos(rotDeg * Math.PI / 180)}" y1="${diffR * Math.sin(rotDeg * Math.PI / 180)}" 
                               x2="0" y2="0" stroke="${CHART_CONFIG.colors.muted_accent}" stroke-width="8" stroke-dasharray="1,4" />`;
            }

            // Connecting Tick
            const pTick = this.getPos(CHART_CONFIG.r.tick_low, rotDeg);
            html += `<line x1="0" y1="0" x2="${pTick.x - pos.x}" y2="${pTick.y - pos.y}" 
                           stroke="${active ? CHART_CONFIG.colors.accent : '#999'}" stroke-width="${active ? 1.5 : 0.6}" />`;

            // Concentric Nodes for a "Target" look
            html += `<circle cx="0" cy="0" r="${active ? 22 : 16}" fill="${CHART_CONFIG.colors.paper}" stroke="${active ? CHART_CONFIG.colors.accent : CHART_CONFIG.colors.grey}" stroke-width="${active ? 2.5 : 0.6}" />`;
            if (!active) html += `<circle cx="0" cy="0" r="13" fill="none" stroke="#eee" stroke-width="0.3" />`;

            // Optical Offset Correction for Symbol/Text
            const label = isEdu ? (CHART_CONFIG.planetNames[p.name] || p.name) : (CHART_CONFIG.planetSymbols[p.name] || '•');
            const family = isEdu ? "'Noto Serif KR'" : "'Segoe UI Symbol'";
            const size = isEdu ? 12 : 24;
            const dy = isEdu ? "0.05em" : "0.08em"; // Push symbol slightly down to visually center

            html += this.text({ x: 0, y: 0 }, label, size, active ? CHART_CONFIG.colors.accent : CHART_CONFIG.colors.ink, "middle", isEdu ? "700" : "normal", family, dy);

            // Metadata (Degree & Rx) clearly centered below
            html += this.text({ x: 0, y: 20 }, `${p.degree_formatted}${isRetro ? '℞' : ''}`, 9, "#444", "middle", "700", "'Playfair Display'");

            html += `</g>`;
        });

        // 7. Angles
        const angs = [
            { v: asc, l: "ASC", c: CHART_CONFIG.colors.accent, m: true, desc: "Ascendant (Rising)" },
            { v: data.midheaven.position, l: "MC", c: CHART_CONFIG.colors.accent, m: true, desc: "Midheaven" },
            { v: asc + 180, l: "DSC", c: "#444", m: false, desc: "Descendant" },
            { v: data.midheaven.position + 180, l: "IC", c: "#444", m: false, desc: "Imum Coeli" }
        ];
        angs.forEach(a => {
            const rot = a.v - asc + 180;
            const pOuter = this.getPos(CHART_CONFIG.r.outer, rot);
            const pTip = this.getPos(CHART_CONFIG.r.outer + 48, rot); // Slightly longer
            html += this.line(pOuter, pTip, a.c, a.m ? 5 : 2); // Thicker lines
            if (a.m) {
                const s1 = this.getPos(CHART_CONFIG.r.outer + 12, rot + 1.8);
                const s2 = this.getPos(CHART_CONFIG.r.outer + 12, rot - 1.8);
                html += `<polygon points="${pTip.x},${pTip.y} ${s1.x},${s1.y} ${s2.x},${s2.y}" fill="${a.c}" />`;
            }
            // Larger, bolder labels for critical points
            html += this.text(this.getPos(CHART_CONFIG.r.outer + 68, rot), a.l, a.m ? 18 : 14, a.c, "middle", "900", "'Playfair Display'");
        });

        this.svg.innerHTML = html;
    }
}

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
        'North Node': '☊', 'South Node': '☋', 'Chiron': '⚷', 'Fortuna': '⊗'
    },
    signNames: ['양', '황소', '쌍둥이', '게', '사자', '처녀', '천칭', '전갈', '사수', '염소', '물병', '물고기'],
    planetNames: {
        'Sun': '태양', 'Moon': '달', 'Mercury': '수성', 'Venus': '금성', 'Mars': '화성',
        'Jupiter': '목성', 'Saturn': '토성', 'Uranus': '천왕', 'Neptune': '해왕', 'Pluto': '명왕',
        'North Node': '북노드', 'South Node': '남노드', 'Chiron': '카이론', 'Fortuna': '포르투나', 'Spirit': '스피릿'
    },
    houseKeywords: [
        "자아/신체/성격", "돈/소유물/가치관", "형제/소통/여행", "가정/부모/뿌리",
        "자녀/연애/창조성", "건강/업무/봉사", "결혼/파트너/계약", "죽음/유산/변화",
        "철학/교육/여행", "경력/명성/지위", "친구/희망/공동체", "은둔/비밀/무의식"
    ],
    // Concentric Band Architecture: Zodiac -> Planets -> Houses -> Aspects
    r: {
        outer: 382,      // Degree Scale Boundary
        sign_in: 332,    // Zodiac Band Boundary
        planet_in: 252,  // Planet Field Boundary
        house_in: 202,   // House Band & Aspect Boundary
        inner: 202,      // Central Aspect Field
        planet_base: 292, // Midpoint of Planet Donut (Width: 80px)
        house_mid: 227     // Midpoint of House Donut (Width: 50px)
    },
    center: { x: 400, y: 400 },
    weights: {
        asc: 1.8,        // Refined for technical elegance
        ring: 1.2,
        house: 0.8,      // Increased for visibility
        aspect: 0.3
    },
    colors: {
        ink: '#111111',
        grey: '#888888',
        accent: '#6B1B1B', // Deep Oxblood / Muted Red
        paper: '#F9F7F1'
    },
    elementColors: {
        fire: '#D14124', earth: '#4E6E58', air: '#A88B12', water: '#2B5A82'
    },
    signElements: [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
    elementNames: ['fire', 'earth', 'air', 'water']
};

class ChartEngine {
    constructor(svgId) {
        this.svgId = svgId;
        this.svg = document.getElementById(svgId);
        this.mode = 'symbol';
        this.activePlanet = null;
        this.data = null;
        this.showFortune = false;
        this.showSpirit = false;
        this.showTerms = false;
        this.alwaysShowAspects = false;
    }

    setOption(key, val) {
        this[key] = val;
        if (this.data) this.render(this.data);
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
        return `<line x1="${p1.x}" y1="${p1.y}" x2="${p2.x}" y2="${p2.y}" stroke="${color}" stroke-width="${width}" stroke-dasharray="${dash}" stroke-linecap="round" />`;
    }

    // Advanced Text Helper with dy correction
    text(pos, content, size, color, align = "middle", weight = "normal", family = "'Noto Serif KR', serif", dy = "0em") {
        return `<text x="${pos.x}" y="${pos.y}" dy="${dy}" text-anchor="${align}" dominant-baseline="central" 
                font-size="${size}" font-weight="${weight}" fill="${color}" style="font-family: ${family}; font-variant-numeric: tabular-nums; pointer-events:none;">${content}</text>`;
    }

    highlight(planetName) {
        if (this.activePlanet === planetName) return;
        this.activePlanet = planetName;
        if (this.data) this.render(this.data);
    }

    render(data) {
        if (!data) return;
        this.data = data;

        // Ensure SVG is available (retry if it wasn't there at construction)
        if (!this.svg) this.svg = document.getElementById(this.svgId);
        if (!this.svg) {
            console.error("SVG Element not found: " + this.svgId);
            return;
        }

        this.clear();

        const asc = data.ascendant.position;
        const mc = data.midheaven.position;
        const isEdu = (this.mode === 'text');
        const { r, weights: w, colors: c } = CHART_CONFIG;

        let html = `<rect width="800" height="800" fill="transparent" />`;

        // 1. Concentric Bands (The Framework)
        // Subtle fill for the House Band to make it distinct
        html += `<circle cx="400" cy="400" r="${r.planet_in}" fill="rgba(0,0,0,0.03)" stroke="none" />`;
        html += `<circle cx="400" cy="400" r="${r.house_in}" fill="${c.paper}" stroke="none" />`;

        html += `<circle cx="400" cy="400" r="${r.outer}" fill="none" stroke="${c.ink}" stroke-width="${w.ring}" />`;
        html += `<circle cx="400" cy="400" r="${r.sign_in}" fill="none" stroke="${c.ink}" stroke-width="${w.house}" opacity="0.6" />`;
        html += `<circle cx="400" cy="400" r="${r.planet_in}" fill="none" stroke="${c.ink}" stroke-width="${w.house}" opacity="0.4" />`;
        html += `<circle cx="400" cy="400" r="${r.house_in}" fill="none" stroke="${c.ink}" stroke-width="${w.ring}" />`;

        // 2. Technical Degree Scale (Angle Ticks) - Restored
        for (let d = 0; d < 360; d++) {
            const rot = d - asc + 180;
            let len = 3; let weight = 0.3;
            if (d % 30 === 0) continue;
            else if (d % 10 === 0) { len = 10; weight = w.house; }
            else if (d % 5 === 0) { len = 6; weight = 0.4; }
            html += this.line(this.getPos(r.outer, rot), this.getPos(r.outer - len, rot), c.ink, weight);
        }

        // 3. Primary Axes (Enhanced Symmetry)
        const horizRot = 180;
        const mcRot = (mc - asc + 180 + 360) % 360;

        // Draw the Cross of Matter (All 4 arms equal weight or balanced)
        // Horizontal Axis (ASC-DSC)
        html += this.line(this.getPos(r.inner, horizRot), this.getPos(r.outer, horizRot), c.accent, w.asc); // ASC
        html += this.line(this.getPos(r.inner, 0), this.getPos(r.outer, 0), c.accent, w.asc);         // DSC (promoted)

        // Vertical Axis (MC-IC)
        html += this.line(this.getPos(r.inner, mcRot), this.getPos(r.outer, mcRot), c.accent, w.asc * 0.8);      // MC
        html += this.line(this.getPos(r.inner, mcRot + 180), this.getPos(r.outer, mcRot + 180), c.accent, w.asc * 0.8); // IC (promoted)

        // 4. Central Metadata Anchor
        const mX = 400; const mY = 400;
        const mCol = "rgba(0,0,0,0.5)";
        html += this.text({ x: mX, y: mY - 52 }, data.name || "NATAL CHART", 18, mCol, "middle", "900", "'Inter'");
        html += this.text({ x: mX, y: mY - 22 }, data.birth_date || "", 13, mCol, "middle", "700", "'Inter'");
        html += this.text({ x: mX, y: mY + 4 }, data.birth_time || "", 13, mCol, "middle", "700", "'Inter'");
        html += this.text({ x: mX, y: mY + 30 }, data.place_name || "", 11, mCol, "middle", "500", "'Noto Serif KR'");
        if (data.latitude !== undefined && data.longitude !== undefined) {
            const coordStr = `${Math.abs(data.latitude).toFixed(2)}${data.latitude >= 0 ? 'N' : 'S'} · ${Math.abs(data.longitude).toFixed(2)}${data.longitude >= 0 ? 'E' : 'W'}`;
            html += this.text({ x: mX, y: mY + 50 }, coordStr, 9, "rgba(0,0,0,0.35)", "middle", "600", "'Inter'");
        }

        // 5. Aspects (Drawn behind planets to avoid text overlap)
        data.aspects.forEach(asp => {
            if (["Conjunction", "Opposition", "Trine", "Square", "Sextile"].includes(asp.type) && asp.orb < 8) {
                const isHovered = (this.activePlanet === asp.planet1 || this.activePlanet === asp.planet2);
                const shouldDraw = this.alwaysShowAspects || (this.activePlanet && isHovered);

                if (!shouldDraw) return;

                const p1 = data.planets.find(p => p.name === asp.planet1);
                const p2 = data.planets.find(p => p.name === asp.planet2);
                if (p1 && p2) {
                    const rot1 = p1.position - asc + 180;
                    const rot2 = p2.position - asc + 180;
                    const pos1 = this.getPos(r.inner, rot1);
                    const pos2 = this.getPos(r.inner, rot2);

                    // Adjusted visibility for Always Show mode
                    let aCol = isHovered ? "rgba(0,0,0,0.8)" : (this.alwaysShowAspects ? "rgba(0,0,0,0.6)" : "rgba(0,0,0,0.1)");
                    if (asp.type === "Square" || asp.type === "Opposition") {
                        if (isHovered) aCol = c.accent;
                        else if (this.alwaysShowAspects) aCol = "rgba(107,27,27,0.6)";
                    }

                    // Main Connection Line
                    html += this.line(pos1, pos2, aCol, isHovered ? 1.5 : (this.alwaysShowAspects ? 0.8 : w.aspect), asp.type === "Sextile" ? "6,6" : "");

                    // Radial Rays to Protractor
                    if (isHovered) {
                        html += this.line(pos1, this.getPos(r.outer, rot1), aCol, 0.4, "4,4");
                        html += this.line(pos2, this.getPos(r.outer, rot2), aCol, 0.4, "4,4");
                    }
                }
            }
        });

        // 6. Band-Specific Content (Zodiac & Houses)
        for (let i = 0; i < 12; i++) {
            const rot = (i * 30) - asc + 180;
            const mid = rot + 15;

            // House Lines - Confined to Planet + House + Scale range
            html += this.line(this.getPos(r.inner, rot), this.getPos(r.outer, rot), c.ink, w.house);

            // Zodiac Symbols (Outer Band: 332-382)
            const sPos = this.getPos((r.outer + r.sign_in) / 2, mid);
            const eIdx = CHART_CONFIG.signElements[i];
            const eCol = CHART_CONFIG.elementColors[CHART_CONFIG.elementNames[eIdx]];
            if (isEdu) {
                html += this.text(sPos, CHART_CONFIG.signNames[i], 15, eCol, "middle", "900");
            } else {
                html += this.text(sPos, CHART_CONFIG.signSymbols[i], 36, eCol, "middle", "normal", "'Segoe UI Symbol'");
            }

            // House Indicators (Inner Band: 202-252)
            const hNumIdx = (i - Math.floor(asc / 30) + 12) % 12;
            const hPos = this.getPos(r.house_mid, mid);
            if (isEdu) {
                html += this.text(hPos, hNumIdx + 1, 15, c.grey, "middle", "900", "'Playfair Display'", "-0.6em");
                html += this.text(hPos, CHART_CONFIG.houseKeywords[hNumIdx], 8.5, "#666", "middle", "700", "'Noto Serif KR'", "1.0em");
            } else {
                html += this.text(hPos, hNumIdx + 1, 18, c.grey, "middle", "700", "'Playfair Display'");
            }
        }

        // 6. Planets (Middle Band: 252-332)
        const pList = [...data.planets];
        if (this.showFortune && data.fortuna && data.fortuna.position !== undefined) {
            pList.push({ name: 'Fortuna', symbol: '⊗', position: data.fortuna.position, degree_formatted: data.fortuna.degree_formatted });
        }
        if (this.showSpirit && data.spirit && data.spirit.position !== undefined) {
            pList.push({ name: 'Spirit', symbol: '◈', position: data.spirit.position, degree_formatted: data.spirit.degree_formatted });
        }
        const sorted = pList.filter(p => p.position !== undefined).sort((a, b) => a.position - b.position);

        sorted.forEach((p, i) => {
            p.level = 0;
            if (i > 0) {
                let diff = p.position - sorted[i - 1].position;
                if (diff < 0) diff += 360;
                if (diff < 12) p.level = (sorted[i - 1].level + 1) % 3; // Tightened levels to fit mid-band
            }
        });

        sorted.forEach(p => {
            const pRot = p.position - asc + 180;
            const pRad = r.planet_base - (p.level * 28); // Offset inside the 80px donut
            const pos = this.getPos(pRad, pRot);
            const active = (this.activePlanet === p.name);
            const pCol = (p.name === 'Fortuna' || active) ? c.accent : c.ink;

            html += `<g transform="translate(${pos.x}, ${pos.y})" style="cursor:pointer;" onmouseenter="highlightPlanet('${p.name}')" onmouseleave="highlightPlanet(null)">`;
            // Pointer Line (Extends to scale when active)
            const targetR = active ? r.outer : (r.sign_in - 5);
            const tPos = this.getPos(targetR, pRot);
            html += `<line x1="0" y1="0" x2="${tPos.x - pos.x}" y2="${tPos.y - pos.y}" stroke="${active ? c.accent : '#DDD'}" stroke-width="${active ? 1.2 : 0.4}" />`;
            // Interaction Hit-area (Invisible)
            html += `<circle cx="0" cy="0" r="26" fill="rgba(0,0,0,0)" stroke="none" />`;

            const label = isEdu ? (CHART_CONFIG.planetNames[p.name] || p.name) : (CHART_CONFIG.planetSymbols[p.name] || p.symbol || '•');
            html += this.text({ x: 0, y: 0 }, label, isEdu ? 14 : 28, pCol, "middle", "900", isEdu ? "'Noto Serif KR'" : "'Segoe UI Symbol'");
            html += this.text({ x: 0, y: 20 }, p.degree_formatted, 9, "#444", "middle", "800", "'Inter'");
            html += `</g>`;
        });

        // 8. Angle Plates (Outer Labels) - Unified Style
        const angs = [
            { v: 180, l: "ASC", c: c.accent },
            { v: mcRot, l: "MC", c: c.accent },
            { v: 0, l: "DSC", c: c.accent },    // DSC promoted to accent
            { v: mcRot + 180, l: "IC", c: c.accent } // IC promoted to accent
        ];

        angs.forEach(a => {
            const pO = this.getPos(r.outer, a.v);
            const pT = this.getPos(r.outer + 30, a.v);
            // Unified thickness for outer markers
            html += this.line(pO, pT, a.c, 3);

            const bP = this.getPos(r.outer + 52, a.v);
            // Smaller, cleaner plate for a "drafting" look
            html += `<rect x="${bP.x - 22}" y="${bP.y - 12}" width="44" height="24" rx="2" fill="${c.paper}" stroke="${a.c}" stroke-width="1.2" />`;
            html += this.text(bP, a.l, 14, a.c, "middle", "900", "'Inter'");

            // Explicit Label near the Axis inside the chart for immediate clarity
            // Added DSC and IC to internal labels
            if (["ASC", "MC", "DSC", "IC"].includes(a.l)) {
                const labelPos = this.getPos(r.outer - 45, a.v + 3); // Slightly offset radially and angularly
                html += this.text(labelPos, a.l, 12, a.c, "start", "900", "'Inter'");
            }
        });

        this.svg.innerHTML = html;
    }
}

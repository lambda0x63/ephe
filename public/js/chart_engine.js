/**
 * ChartEngine v25.2 - Dynamic Aspect Beams
 * EPHE 엔진: 행성 간 직접 연결 광선 (Long-range Aspect Beams)
 */

const CHART_CONFIG = {
    signSymbols: ['♈︎', '♉︎', '♊︎', '♋︎', '♌︎', '♍︎', '♎︎', '♏︎', '♐︎', '♑︎', '♒︎', '♓︎'],
    planetSymbols: {
        'Sun': '☉︎', 'Moon': '☽︎', 'Mercury': '☿︎', 'Venus': '♀︎', 'Mars': '♂︎',
        'Jupiter': '♃︎', 'Saturn': '♄︎', 'North Node': '☊︎', 'South Node': '☋︎',
        'Fortuna': '⊗', 'Spirit': '⊕'
    },
    traditionalOrbs: {
        'Sun': 15.0, 'Moon': 12.0, 'Jupiter': 9.0, 'Saturn': 9.0,
        'Mars': 8.0, 'Venus': 7.0, 'Mercury': 7.0, 'North Node': 0,
        'South Node': 0, 'Fortuna': 0, 'Spirit': 0
    },
    colors: {
        canvasBg: '#F7F7F7',
        mainLines: '#0000FF',
        text: '#000000',
        aspects: {
            conjunction: '#000000',
            sextile: '#2E8B57',
            square: '#C3322D',
            trine: '#4169E1',
            opposition: '#B22222'
        }
    },
    r: {
        outer: 495, zodiac: 435, ticks: 425, terms: 385, faces: 345, inner: 110
    },
    center: { x: 500, y: 500 }
};

const EGYPTIAN_TERMS = {
    "Aries": [[6, "Jupiter"], [12, "Venus"], [20, "Mercury"], [25, "Mars"], [30, "Saturn"]],
    "Taurus": [[8, "Venus"], [14, "Mercury"], [22, "Jupiter"], [27, "Saturn"], [30, "Mars"]],
    "Gemini": [[6, "Mercury"], [12, "Jupiter"], [17, "Venus"], [24, "Mars"], [30, "Saturn"]],
    "Cancer": [[7, "Mars"], [13, "Venus"], [19, "Mercury"], [26, "Jupiter"], [30, "Saturn"]],
    "Leo": [[6, "Jupiter"], [11, "Venus"], [18, "Saturn"], [24, "Mercury"], [30, "Mars"]],
    "Virgo": [[7, "Mercury"], [17, "Venus"], [21, "Jupiter"], [28, "Mars"], [30, "Saturn"]],
    "Libra": [[6, "Saturn"], [14, "Venus"], [21, "Jupiter"], [28, "Mercury"], [30, "Mars"]],
    "Scorpio": [[7, "Mars"], [11, "Venus"], [19, "Mercury"], [24, "Jupiter"], [30, "Saturn"]],
    "Sagittarius": [[12, "Jupiter"], [17, "Venus"], [21, "Mercury"], [26, "Saturn"], [30, "Mars"]],
    "Capricorn": [[7, "Mercury"], [14, "Jupiter"], [22, "Venus"], [26, "Saturn"], [30, "Mars"]],
    "Aquarius": [[7, "Saturn"], [13, "Mercury"], [20, "Venus"], [25, "Jupiter"], [30, "Mars"]],
    "Pisces": [[12, "Venus"], [16, "Jupiter"], [19, "Mercury"], [28, "Mars"], [30, "Saturn"]]
};

const CHALDEAN_FACES = [
    "Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon",
    "Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars", "Sun", "Venus",
    "Mercury", "Moon", "Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"
];

class ChartEngine {
    constructor(svgId) {
        this.svgId = svgId;
        this.svg = document.getElementById(svgId);
        this.data = null;
        this.houseSystem = 'WSH';
        this.showTerms = false;
        this.showDecans = false;
        this.selectedPlanet = null;
    }

    setOption(key, val) {
        this[key] = val;
        this.selectedPlanet = null;
        if (this.data) this.render(this.data);
    }

    setHouseSystem(system) {
        this.houseSystem = system;
        this.selectedPlanet = null;
        if (this.data) this.render(this.data);
    }

    getPos(radius, deg) {
        const rad = (deg % 360) * (Math.PI / 180);
        return { x: 500 + radius * Math.cos(rad), y: 500 - radius * Math.sin(rad) };
    }

    formatPos(long) {
        const deg = Math.floor(long % 30);
        const min = Math.floor((long % 1) * 60);
        return `${deg}° ${min.toString().padStart(2, '0')}'`;
    }

    calculateAspect(p1, p2) {
        const diff = Math.abs(p1.position - p2.position);
        const angle = Math.min(diff, 360 - diff);
        const orb1 = CHART_CONFIG.traditionalOrbs[p1.name] || 0;
        const orb2 = CHART_CONFIG.traditionalOrbs[p2.name] || 0;
        const moiety = (orb1 + orb2) / 2;

        const majorAspects = [
            { type: 'conjunction', deg: 0 },
            { type: 'sextile', deg: 60 },
            { type: 'square', deg: 90 },
            { type: 'trine', deg: 120 },
            { type: 'opposition', deg: 180 }
        ];

        for (const asp of majorAspects) {
            if (Math.abs(angle - asp.deg) <= moiety) {
                const s1 = Math.floor(p1.position / 30);
                const s2 = Math.floor(p2.position / 30);
                const signDiff = Math.abs(s1 - s2);
                const signDist = Math.min(signDiff, 12 - signDiff);
                if (signDist === asp.deg / 30) return asp;
            }
        }
        return null;
    }

    selectPlanet(name) {
        this.selectedPlanet = (this.selectedPlanet === name) ? null : name;
        this.render(this.data);
    }

    render(data) {
        if (!data) return;
        this.data = data;
        const asc = data.angles.asc.position;
        const { r, colors: c } = CHART_CONFIG;
        this.svg.innerHTML = '';
        const viewRotation = 180 - asc;

        let houseCusps = [];
        if (this.houseSystem === 'WSH') {
            const ascSignStart = Math.floor(asc / 30) * 30;
            for (let i = 0; i < 12; i++) houseCusps.push((ascSignStart + i * 30) % 360);
        } else {
            houseCusps = data.porphyry_cusps;
        }

        let html = `<rect width="1000" height="1000" fill="${c.canvasBg}" />`;

        // 1. Concentric Rings
        [r.outer, r.zodiac, r.inner].forEach((radius, idx) => {
            html += `<circle cx="500" cy="500" r="${radius}" fill="none" stroke="${c.mainLines}" stroke-width="${idx === 0 ? 1.8 : 1.0}" />`;
        });
        if (this.showTerms) html += `<circle cx="500" cy="500" r="${r.terms}" fill="none" stroke="${c.mainLines}" stroke-width="0.8" opacity="0.4" />`;
        if (this.showDecans) html += `<circle cx="500" cy="500" r="${r.faces}" fill="none" stroke="${c.mainLines}" stroke-width="0.8" opacity="0.4" />`;
        html += `<circle cx="500" cy="500" r="${r.inner}" fill="#FAFAFA" stroke="${c.text}" stroke-width="1.2" />`;

        // 2. Signs
        const signNames = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];
        for (let i = 0; i < 12; i++) {
            const startLong = i * 30, startAngle = startLong + viewRotation, midAngle = startAngle + 15;
            html += `<line x1="${this.getPos(r.zodiac, startAngle).x}" y1="${this.getPos(r.zodiac, startAngle).y}" x2="${this.getPos(r.outer, startAngle).x}" y2="${this.getPos(r.outer, startAngle).y}" stroke="${c.mainLines}" stroke-width="2.2" />`;

            for (let d = 1; d < 30; d++) {
                const ta = startAngle + d, tl = (d % 10 === 0) ? 12 : ((d % 5 === 0) ? 8 : 4);
                const p1 = this.getPos(r.zodiac, ta), p2 = this.getPos(r.zodiac - tl, ta);
                html += `<line x1="${p1.x}" y1="${p1.y}" x2="${p2.x}" y2="${p2.y}" stroke="${c.mainLines}" stroke-width="0.8" opacity="0.3" />`;
            }

            const symbolPos = this.getPos((r.outer + r.zodiac) / 2, midAngle);
            html += `<text x="${symbolPos.x}" y="${symbolPos.y}" text-anchor="middle" dominant-baseline="central" font-size="40" font-weight="950">${CHART_CONFIG.signSymbols[i]}</text>`;

            if (this.showTerms) {
                const terms = EGYPTIAN_TERMS[signNames[i]];
                let curD = 0;
                terms.forEach(([endD, p]) => {
                    const b = startAngle + endD;
                    html += `<line x1="${this.getPos(r.terms, b).x}" y1="${this.getPos(r.terms, b).y}" x2="${this.getPos(r.zodiac, b).x}" y2="${this.getPos(r.zodiac, b).y}" stroke="${c.text}" stroke-width="0.8" opacity="0.2" />`;
                    const lp = this.getPos((r.terms + r.zodiac) / 2, startAngle + (curD + endD) / 2);
                    html += `<text x="${lp.x}" y="${lp.y}" text-anchor="middle" dominant-baseline="central" font-size="12" font-weight="800" fill="${c.text}">${CHART_CONFIG.planetSymbols[p] || '•'}</text>`;
                    curD = endD;
                });
            }

            if (this.showDecans) {
                for (let f = 0; f < 3; f++) {
                    const p = startAngle + (f * 10) + 5, planet = CHALDEAN_FACES[i * 3 + f];
                    const pos = this.getPos((r.faces + (this.showTerms ? r.terms : r.zodiac)) / 2, p);
                    html += `<text x="${pos.x}" y="${pos.y}" text-anchor="middle" dominant-baseline="central" font-size="11" font-weight="800" opacity="0.6" fill="${c.text}">${CHART_CONFIG.planetSymbols[planet]}</text>`;
                }
            }
        }

        // 3. Houses & Axis
        houseCusps.forEach((cup, i) => {
            const hA = cup + viewRotation, midA = hA + 15, hLimit = (this.showDecans ? r.faces : (this.showTerms ? r.terms : r.zodiac));
            html += `<line x1="${this.getPos(r.inner, hA).x}" y1="${this.getPos(r.inner, hA).y}" x2="${this.getPos(hLimit, hA).x}" y2="${this.getPos(hLimit, hA).y}" stroke="${c.mainLines}" stroke-width="1.2" opacity="0.6" />`;
            const nP = this.getPos(r.inner + 30, midA);
            html += `<text x="${nP.x}" y="${nP.y}" text-anchor="middle" dominant-baseline="central" font-size="18" font-weight="900" fill="${c.mainLines}" opacity="0.3">${i + 1}</text>`;
        });

        const mcP = data.angles.mc.position + viewRotation, icP = mcP + 180;
        [{ a: 180, t: 'ASC', w: 2.5 }, { a: 0, t: 'DSC', w: 1.2 }, { a: mcP, t: 'MC', w: 2.5 }, { a: icP, t: 'IC', w: 1.2 }].forEach(l => {
            const p1 = this.getPos(r.inner, l.a), p2 = this.getPos(r.outer + 50, l.a), labelP = this.getPos(r.outer + 75, l.a);
            html += `<line x1="${p1.x}" y1="${p1.y}" x2="${p2.x}" y2="${p2.y}" stroke="${c.text}" stroke-width="${l.w}" />`;
            html += `<text x="${labelP.x}" y="${labelP.y}" text-anchor="middle" dominant-baseline="central" font-size="22" font-weight="950" style="font-family:'JetBrains Mono'">${l.t}</text>`;
        });

        // 4. Planets Object Pre-calculation (For Aspect Lines)
        let objects = [...data.planets];
        if (data.lots) {
            ['Fortuna', 'Spirit'].forEach(k => { if (data.lots[k]) objects.push({ name: k, position: data.lots[k].position }); });
        }
        objects.sort((a, b) => a.position - b.position);

        const pRBase = (this.showDecans ? r.faces : (this.showTerms ? r.terms : r.zodiac)) - 45, levels = new Map();
        const objDrawInfo = objects.map(p => {
            const rot = (p.position + viewRotation + 360) % 360;
            let level = 0;
            for (let d = -12; d <= 12; d += 0.5) { const k = Math.round((rot + d) % 360); if (levels.has(k)) level = Math.max(level, levels.get(k) + 1); }
            levels.set(Math.round(rot), level);
            return { ...p, rot, radius: pRBase - (level * 65) };
        });

        const hLimit = (this.showDecans ? r.faces : (this.showTerms ? r.terms : r.zodiac));

        // DRAW ASPECT BEAMS FIRST (Under planets)
        if (this.selectedPlanet) {
            const ori = objDrawInfo.find(o => o.name === this.selectedPlanet);
            if (ori) {
                objDrawInfo.forEach(tar => {
                    const asp = (ori.name !== tar.name) ? this.calculateAspect(ori, tar) : null;
                    if (asp) {
                        const p1 = this.getPos(hLimit, ori.position + viewRotation);
                        const p2 = this.getPos(hLimit, tar.position + viewRotation);

                        html += `<line x1="${p1.x}" y1="${p1.y}" x2="${p2.x}" y2="${p2.y}" 
                                       stroke="${CHART_CONFIG.colors.aspects[asp.type]}" 
                                       stroke-width="1.5" opacity="0.8" />`;
                    }
                });
            }
        }

        // DRAW PLANETS
        objDrawInfo.forEach(p => {
            const pos = this.getPos(p.radius, p.rot), isS = this.selectedPlanet === p.name;

            // Morinus Style Source Marker (휠 내벽에 배치)
            if (isS) {
                const markerPos = this.getPos(hLimit, p.rot);
                html += `<circle cx="${markerPos.x}" cy="${markerPos.y}" r="5" fill="${c.mainLines}" />`;
                html += `<circle cx="${markerPos.x}" cy="${markerPos.y}" r="11" fill="none" stroke="${c.mainLines}" stroke-width="1.5" opacity="0.6" />`;
            }

            html += `<g transform="translate(${pos.x}, ${pos.y})" style="cursor:pointer" onclick="window.chartEngine.selectPlanet('${p.name}')">
                <text x="0" y="-14" text-anchor="middle" dominant-baseline="central" font-size="42" font-weight="bold" fill="${isS ? c.mainLines : c.text}">${CHART_CONFIG.planetSymbols[p.name] || '•'}</text>
                <text x="0" y="24" text-anchor="middle" font-size="14" font-weight="950" fill="${c.text}" style="font-family:'JetBrains Mono'">${this.formatPos(p.position)}</text>
                ${p.retrograde ? `<text x="40" y="-30" fill="${c.text}" font-size="18" font-weight="950">Rx</text>` : ''}
            </g>`;
        });

        const meta = [data.meta.name.toUpperCase(), data.meta.date.replace(/-/g, '.'), data.meta.time.substring(0, 5) + " LMT", this.houseSystem === 'WSH' ? "홀사인 (WSH)" : "포피리 (Porphyry)", "네이탈 (RADIX)"];
        meta.forEach((txt, i) => html += `<text x="500" y="${460 + (i * 20)}" text-anchor="middle" font-size="14" font-weight="950" style="font-family:'JetBrains Mono'; opacity:0.8;">${txt}</text>`);
        this.svg.innerHTML = html;
    }
}

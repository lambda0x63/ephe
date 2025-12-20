/**
 * ChartEngine for drawing Natal Chart SVG
 * Classic Paper Theme
 */

const CHART_CONFIG = {
    signs: ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'],
    signSymbols: ['♈\uFE0E', '♉\uFE0E', '♊\uFE0E', '♋\uFE0E', '♌\uFE0E', '♍\uFE0E', '♎\uFE0E', '♏\uFE0E', '♐\uFE0E', '♑\uFE0E', '♒\uFE0E', '♓\uFE0E'],
    elements: ['fire', 'earth', 'air', 'water', 'fire', 'earth', 'air', 'water', 'fire', 'earth', 'air', 'water'],
    radius: { outer: 360, sign: 300, planet_base: 250, planet_step: 24, house: 200, inner: 140 }
};

class ChartEngine {
    constructor(svgId) {
        this.svg = document.getElementById(svgId);
        this.center = { x: 400, y: 400 };
    }

    clear() { if (this.svg) this.svg.innerHTML = ''; }

    getSvgPos(radius, zodiacDegree, ascDegree) {
        const angleDeg = 180 - (zodiacDegree - ascDegree);
        const rad = angleDeg * (Math.PI / 180);
        return { x: this.center.x + radius * Math.cos(rad), y: this.center.y + radius * Math.sin(rad) };
    }

    createLine(x1, y1, x2, y2, color, width, dash = '', className = '') {
        return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${width}" stroke-dasharray="${dash}" class="${className}" stroke-linecap="round" />`;
    }

    createText(x, y, text, size, color, anchor = "middle", weight = "normal", className = "") {
        return `<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}" dominant-baseline="central" font-weight="${weight}" class="${className}">${text}</text>`;
    }

    createArcPath(r1, r2, startDeg, endDeg, ascDeg) {
        const startAngle = (180 - (startDeg - ascDeg)) * (Math.PI / 180);
        const endAngle = (180 - (endDeg - ascDeg)) * (Math.PI / 180);
        const x1_o = this.center.x + r1 * Math.cos(startAngle); const y1_o = this.center.y + r1 * Math.sin(startAngle);
        const x2_o = this.center.x + r1 * Math.cos(endAngle); const y2_o = this.center.y + r1 * Math.sin(endAngle);
        const x1_i = this.center.x + r2 * Math.cos(startAngle); const y1_i = this.center.y + r2 * Math.sin(startAngle);
        const x2_i = this.center.x + r2 * Math.cos(endAngle); const y2_i = this.center.y + r2 * Math.sin(endAngle);
        return `M ${x1_o} ${y1_o} A ${r1} ${r1} 0 0 0 ${x2_o} ${y2_o} L ${x2_i} ${y2_i} A ${r2} ${r2} 0 0 1 ${x1_i} ${y1_i} Z`;
    }

    resolveCollisions(planets) {
        const sorted = [...planets].filter(p => p.name !== 'Ascendant').sort((a, b) => a.position - b.position);
        sorted.forEach((p, i) => {
            p.track = 0; if (i > 0) {
                const prev = sorted[i - 1]; if (Math.abs(p.position - prev.position) < 10) {
                    if (prev.track === 0) p.track = 1; else if (prev.track === 1) p.track = 2; else p.track = 0;
                }
            }
        });
        return sorted;
    }

    highlight(planetName) {
        const all = this.svg.querySelectorAll('.planet-group');
        all.forEach(el => el.classList.remove('active'));
        if (planetName) {
            const target = this.svg.querySelector(`.planet-group[data-name="${planetName}"]`);
            if (target) target.classList.add('active');
        }
    }

    render(data) {
        if (!data) return;
        this.clear();
        let svgContent = '';
        const ascAbs = data.ascendant.position;

        // Frame
        svgContent += `<circle cx="${this.center.x}" cy="${this.center.y}" r="${CHART_CONFIG.radius.outer}" fill="#fff" stroke="#111" stroke-width="2" />`;
        svgContent += `<circle cx="${this.center.x}" cy="${this.center.y}" r="${CHART_CONFIG.radius.inner}" fill="none" stroke="#ccc" stroke-width="0.5" />`;

        // Zodiac
        for (let i = 0; i < 12; i++) {
            const startZ = i * 30; const endZ = (i + 1) * 30;
            svgContent += `<path d="${this.createArcPath(CHART_CONFIG.radius.outer, CHART_CONFIG.radius.sign, startZ, endZ, ascAbs)}" fill="none" stroke="#111" stroke-width="1" />`;
            const elemClass = `elem-${CHART_CONFIG.elements[i]}`;
            const pos = this.getSvgPos((CHART_CONFIG.radius.outer + CHART_CONFIG.radius.sign) / 2, startZ + 15, ascAbs);
            svgContent += this.createText(pos.x, pos.y, CHART_CONFIG.signSymbols[i], 28, "", "middle", "normal", `sign-glyph ${elemClass}`);
            for (let d = 5; d < 30; d += 5) {
                let len = 6; let width = 0.5; let color = "#999";
                if (d % 10 === 0) { len = 10; width = 1; color = "#666"; }
                const t1 = this.getSvgPos(CHART_CONFIG.radius.sign, startZ + d, ascAbs);
                const t2 = this.getSvgPos(CHART_CONFIG.radius.sign - len, startZ + d, ascAbs);
                svgContent += this.createLine(t1.x, t1.y, t2.x, t2.y, color, width);
            }
        }

        // Dividers
        for (let i = 0; i < 12; i++) {
            const deg = i * 30;
            const p1 = this.getSvgPos(CHART_CONFIG.radius.inner, deg, ascAbs);
            const p2 = this.getSvgPos(CHART_CONFIG.radius.sign, deg, ascAbs);
            svgContent += this.createLine(p1.x, p1.y, p2.x, p2.y, "#ddd", 1);
        }

        // Angles
        const angles = [
            { deg: data.ascendant.position, color: "var(--angle-color)", label: "ASC" },
            { deg: (data.ascendant.position + 180) % 360, color: "var(--angle-color)", label: "DSC" },
            { deg: data.midheaven.position, color: "var(--angle-color)", label: "MC" },
            { deg: (data.midheaven.position + 180) % 360, color: "var(--angle-color)", label: "IC" }
        ];
        angles.forEach(ang => {
            const p2 = this.getSvgPos(CHART_CONFIG.radius.inner, ang.deg, ascAbs);
            svgContent += this.createLine(this.center.x, this.center.y, p2.x, p2.y, ang.color, 1.5, "4,2");
            const labelPos = this.getSvgPos(CHART_CONFIG.radius.inner - 15, ang.deg, ascAbs);
            svgContent += this.createText(labelPos.x, labelPos.y, ang.label, 10, ang.color, "middle", "bold");
        });

        // Aspects (Optimization: use fragment or string builder if too heavy, but here fine)
        data.aspects.forEach(asp => {
            if (asp.orb < 8) {
                const p1 = data.planets.find(p => p.name === asp.planet1);
                const p2 = data.planets.find(p => p.name === asp.planet2);
                if (p1 && p2) {
                    const xy1 = this.getSvgPos(CHART_CONFIG.radius.inner, p1.position, ascAbs);
                    const xy2 = this.getSvgPos(CHART_CONFIG.radius.inner, p2.position, ascAbs);
                    let color = "rgba(0,0,0,0.1)"; let width = 0.5;
                    if (["Square", "Opposition"].includes(asp.type)) { color = "rgba(200, 50, 50, 0.3)"; width = 1; }
                    else if (["Trine", "Sextile"].includes(asp.type)) { color = "rgba(50, 100, 200, 0.3)"; width = 1; }
                    if (asp.orb < 3) { width += 0.5; color = color.replace("0.3", "0.6"); }
                    svgContent += this.createLine(xy1.x, xy1.y, xy2.x, xy2.y, color, width, "", "aspect-line");
                }
            }
        });

        this.svg.innerHTML = svgContent;

        // Planets
        const visiblePlanets = this.resolveCollisions(data.planets);
        visiblePlanets.forEach(p => {
            let r = CHART_CONFIG.radius.planet_base;
            if (p.track === 1) r -= CHART_CONFIG.radius.planet_step; else if (p.track === 2) r += CHART_CONFIG.radius.planet_step;
            const xy = this.getSvgPos(r, p.position, ascAbs);

            const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
            g.setAttribute("class", "planet-group");
            g.setAttribute("data-name", p.name);

            const guideEnd = this.getSvgPos(CHART_CONFIG.radius.sign - 5, p.position, ascAbs);
            g.innerHTML += this.createLine(xy.x, xy.y, guideEnd.x, guideEnd.y, "#ccc", 0.5, "2,2");
            g.innerHTML += `<circle cx="${xy.x}" cy="${xy.y}" r="16" fill="#fff" stroke="#111" stroke-width="1" />`;
            g.innerHTML += this.createText(xy.x, xy.y, p.symbol, 22, "#000", "middle", "normal", "planet-glyph");
            this.svg.appendChild(g);
        });
    }
}

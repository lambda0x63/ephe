module.exports = {
    apps: [
        {
            name: "natal-chart-backend",
            interpreter: "/var/www/natal-chart/venv/bin/python3",
            script: "-m",
            args: "uvicorn app.main:app --host 0.0.0.0 --port 8000",
            cwd: "/var/www/natal-chart",
            autorestart: true,
            watch: false,
            max_memory_restart: "1000M",
            env: {
                NODE_ENV: "production",
            },
        },
    ],
};

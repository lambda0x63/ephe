module.exports = {
    apps: [
        {
            name: "natal-chart-backend",
            script: "venv/bin/uvicorn",
            args: "app.main:app --host 0.0.0.0 --port 8000",
            cwd: "/var/www/natal-chart/backend",
            interpreter: "none",
            autorestart: true,
            watch: false,
            max_memory_restart: "1000M",
            env: {
                NODE_ENV: "production",
            },
        },
    ],
};

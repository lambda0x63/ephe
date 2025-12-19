module.exports = {
    apps: [
        {
            name: "natal-chart-backend",
            script: "python3",
            args: "-m uvicorn app.main:app --host 0.0.0.0 --port 8000",
            cwd: "/var/www/natal-fastapi",
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

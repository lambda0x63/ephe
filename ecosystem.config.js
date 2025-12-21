module.exports = {
    apps: [
        {
            name: "ephe-backend",
            script: "python3",
            args: "-m uvicorn app.main:app --host 0.0.0.0 --port 8001 --root-path /ephe",
            cwd: "/var/www/ephe",
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
rm database.db
python3 <<'EOF'
from app import db
db.create_all()
exit()
EOF

sqlite3 database.db <<'EOF'
.tables
.exit
EOF

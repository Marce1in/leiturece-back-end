{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    # Python and dependencies
    (pkgs.python3.withPackages (ps: [
      ps.alembic
      ps.asyncpg
      ps.fastapi
      ps.uvicorn
      ps.sqlalchemy
      ps.greenlet
      ps.pydantic
      ps.typer
      ps.python-dotenv
      ps.httpx
      ps.websockets
      ps.rich
      ps.jinja2
      ps.markupsafe
      ps.email-validator
    ]))

    # Required system libraries
    pkgs.stdenv.cc.cc.lib  # For libstdc++.so.6
    pkgs.postgresql        # For asyncpg's client library
  ];

  # Fixes SSL certificate issues
  SSL_CERT_FILE = "${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt";

  # Needed for finding libstdc++.so.6
  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";

  # Help Python find important paths
  PYTHONPATH = "${pkgs.python3.sitePackages}";
}
